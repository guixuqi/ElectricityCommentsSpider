import cx_Oracle
import os
import queue
import sys
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, ""))
from datetime import datetime
import requests
import re, json
import time
from utils import review_split, save_json, get_ua, save_review, save_score, log_info, logger as jd_log, SKU_DETAIL_ID, max_date
from retrying import retry
from utils import close_db

dsnStr = cx_Oracle.makedsn("192.168.110.205", 1521, "EIP")
conn = cx_Oracle.connect("EIP", "EIP", dsnStr, threaded=True)
sem = threading.Semaphore(40)  # 限制线程的最大数量


class JDReview:

    def __init__(self):
        self.name = "JD"
        self.commentList = []
        self.num = 0
        self.url = 'https://sclub.jd.com/comment/productPageComments.action'
        self.ECOMMERCE_CODE = "7"
        self.SKU_DETAIL_ID = ""
        self.max_date = None

    @retry(stop_max_attempt_number=5)
    def getHtml(self, data, jd_url):
        # 设置请求头
        headers = {
            # 'User-Agent': get_ua(),
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            'Referer': jd_url
        }
        try:
            resp = requests.get(self.url, headers=headers, params=data, timeout=20)
            return resp.text
        except Exception as e:
            # print(e, '请求失败')
            jd_log(jd_url, "请求失败")
            return False

    def getComment(self, comm_dict, productId):  # 获得一页的评论

        try:
            commentSummary = comm_dict['comments']  # 得到包含评论的字典组成的列表
        except:
            jd_log(self.name, productId, "评论列表获取失败")
            return
        if len(commentSummary) < 1:
            return
        for comment in commentSummary:  # 遍历每个包含评论的字典，获得评论和打分
            commentDict = {}
            commentDict["SKU_ID"] = productId  # SKU_ID
            try:
                commentDict["REVIEW_ID"] = comment['guid']  # 评论ID
                commentDict["REVIEW_DATE"] = comment['creationTime']  # 评论时间
                commentDict["content"] = ''.join(
                    comment['content'].split())  # 获得评论,由于有的评论有换行，这里用split（）去空格，换行，并用join（）连接起来形成一整段评论，便于存储
                commentDict["score"] = comment['score']  # 用户打分
                commentDict["nickname"] = comment['nickname']  # 用户名
            except Exception as e:
                jd_log(self.name, productId)
                continue
            if commentDict:
                self.commentList.append(commentDict)
        # print(len(commentSummary))
        # 通过一页评论数量判断是不是最后一页评论
        if len(commentSummary) < 10:
            # print("最后一页")
            return True

    # json转python
    def js2py(self, html, productId):
        try:
            i = json.dumps(html)  # 将页面内容编码成json数据
            j = json.loads(i)  # 将json数据解码为Python对象
            comment = re.findall(r'{"productAttr":.*}', j)  # 网页内容筛选
            comm_dict = json.loads(comment[0])  # 将json对象obj解码为对应的字典dict
        except:
            jd_log(self.name, productId)
            comm_dict = {}
        return comm_dict

    def conments(self, jd_url):  # url主体和爬取网页的数量
        try:
            productId = re.search(r"(\d+).html", jd_url).group(1)
        except:
            jd_log(self.name, jd_url, "网址格式不正确")
            return True
        # 'callback': '{}'.format(callback),
        data = {
            'productId': productId,
            'score': 0,
            'sortType': 6,  # 以时间排序
            'page': 0,
            'pageSize': 10,
            'isShadowSku': 0,
            'rid': 0,
            'fold': 1
        }
        html = self.getHtml(data, jd_url)
        time.sleep(5)
        comm_dict = self.js2py(html, productId)
        # 好评度
        try:
            productCommentSummary = comm_dict['productCommentSummary']
            score = productCommentSummary['goodRateShow']
            score = float(score)
        except:
            jd_log(self.name, productId, "无总评分数据")
            score = 0
        # 以SKU_ID和ECOMMERCE_CODE联合查询ECOMMERCE_SKU_DETAIL表SKU_DETAIL_ID的值
        # if not SKU_DETAIL_ID(productId, self.ECOMMERCE_CODE):
        #     return True
        # self.SKU_DETAIL_ID = SKU_DETAIL_ID(productId, self.ECOMMERCE_CODE)
        # 保存总评分
        save_score(productId, score, self.name, self.SKU_DETAIL_ID, conn)

        # 京东最多只返回100页数据
        for i in range(100):
            try:  # 防止网页提取失败，使爬取终断，直接跳过失败页，继续爬取
                data['page'] = i
                html = self.getHtml(data, jd_url)
                if not html:
                    continue
                comm_dict = self.js2py(html, productId)
                finish = self.getComment(comm_dict, productId)
                if finish:
                    break
            except Exception as e:
                # print(e)
                jd_log(self.name, productId)
                continue
            time.sleep(2)
            if i % 10 == 0:
                time.sleep(5)

    def save_data(self):
        # print(len(commentList))
        for comment in self.commentList:
            REVIEW_ID = self.SKU_DETAIL_ID + "_" + comment["REVIEW_ID"]
            SKU_ID = comment["SKU_ID"]
            REVIEW_STAR = comment["score"]
            REVIEW_NAME = comment["nickname"]
            REVIEW_TEXT = comment["content"]
            # print(REVIEW_TEXT)
            REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_TEXT5 = review_split(REVIEW_TEXT)
            REVIEW_TEXT5 += "  from_JD"
            REVIEW_DATE = comment["REVIEW_DATE"].replace("-", "/")
            CREATE_TIME = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            # 数据库保存
            sql = "INSERT INTO ECOMMERCE_REVIEW_P(REVIEW_ID, SKU_ID, REVIEW_STAR, REVIEW_NAME, REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_DATE, CREATE_TIME, REVIEW_TEXT5, SKU_DETAIL_ID) VALUES('{}', '{}', {}, '{}', '{}', '{}', '{}', '{}', to_date('{}','yyyy/MM/dd HH24:mi:ss'), to_date('{}','yyyy/MM/dd HH24:mi:ss'),'{}', '{}')".format(
                REVIEW_ID, SKU_ID, REVIEW_STAR, REVIEW_NAME.replace("'", ""),
                REVIEW_TEXT1.replace("'", ""),
                REVIEW_TEXT2.replace("'", ""), REVIEW_TEXT3.replace("'", ""), REVIEW_TEXT4.replace("'", ""),
                REVIEW_DATE, CREATE_TIME, REVIEW_TEXT5.replace("'", ""), self.SKU_DETAIL_ID)
            try:
                c = conn.cursor()
                c.execute(sql)
                conn.commit()
                self.num += 1
            except Exception as e:
                # print(e, "第{}条评论保存失败".format(self.num))
                # print(REVIEW_ID)
                jd_log(self.name, SKU_ID, "数据库保存/更新失败")
                conn.rollback()

    def run(self, start_url):
        with sem:
            jd_url = start_url.split("$$$")[0]
            self.SKU_DETAIL_ID = start_url.split("$$$")[1]
            if self.conments(jd_url):
                return
            # 保存数据
            if len(self.commentList) > 0:
                self.save_data()
            else:
                self.num = 0
            log_info("JD,{}共更新了{}条,".format(jd_url, self.num))
            print("JD,{}共更新了{}条,".format(jd_url, self.num))
            # print(self.num)


def run(urls):
    # start = time.time()
    print(len(urls))
    if len(urls) < 1 or isinstance(urls, list) is False:
        # print("无url信息或传入参数格式不是列表")
        log_info("JD,无url信息或传入参数格式不是列表")
        return True
    # for url in urls:
    #     jd = JDReview()
    #     jd.run(url)
    q = queue.Queue()
    for url in urls:
        t = threading.Thread(target=JDReview().run, args=(url,))
        q.put(t)
    while not q.empty():
        t = q.get()
        q.task_done()
        t.start()
    q.join()
    # 关闭数据库
    # close_db()
    # end = time.time()
    # log_info("JD,耗时%s秒" % (end - start))
    # print('耗时%s秒' % (end - start))


if __name__ == '__main__':
    from urls import jd_urls
    urls = jd_urls()
    run(urls)
