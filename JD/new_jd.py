from datetime import datetime
import re
import time
from JD.jd_review import JDReview
from utils import update_score, newReview, logger as jd_log, log_info, SKU_DETAIL_ID, max_date, conn, c


class JDNewReview(JDReview):

    def getComment(self, comm_dict, productId):  # 获得一页的评论

        try:
            commentSummary = comm_dict['comments']  # 得到包含评论的字典组成的列表
        except:
            jd_log(self.name, productId, "评论列表获取失败")
            return
        if len(commentSummary) < 1:
            return
        n = 0
        for comment in commentSummary:  # 遍历每个包含评论的字典，获得评论和打分
            commentDict = {}
            commentDict["SKU_ID"] = productId  # SKU_ID
            try:
                commentDict["REVIEW_ID"] = comment['guid']  # 评论ID
                commentDict["REVIEW_DATE"] = comment['creationTime']  # 评论时间
                date_str = commentDict["REVIEW_DATE"]
                re_date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                # 根据数据库评论最晚时间续爬
                if newReview(self.max_date, re_date):
                    # 防止有些评论没有按时间排序
                    n += 1
                    if n < 3:
                        continue
                    else:
                        return True
                commentDict["content"] = ''.join(
                    comment['content'].split())
                commentDict["score"] = comment['score']  # 用户打分
                commentDict["nickname"] = comment['nickname']  # 用户名
            except Exception as e:
                jd_log(self.name, productId, "提取数据失败")
                continue
            if commentDict:
                self.commentList.append(commentDict)
        # 通过一页评论数量判断是不是最后一页评论
        if len(commentSummary) < 10:
            return True

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
        if not html:
            return True
        comm_dict = self.js2py(html, jd_url)
        # 好评度
        try:
            productCommentSummary = comm_dict['productCommentSummary']
            score = productCommentSummary['goodRateShow']
            score = float(score)
        except:
            jd_log(self.name, productId, "无总评分数据")
            score = 0
        # 更新数据库总评分
        # update_score(score, productId, self.name)
        # if not SKU_DETAIL_ID(productId, self.ECOMMERCE_CODE):
        #     return True
        # self.SKU_DETAIL_ID = SKU_DETAIL_ID(productId, self.ECOMMERCE_CODE)
        # 查询数据库评论最晚日期
        self.max_date = max_date(self.SKU_DETAIL_ID)
        if score != 0:
            update_score(score, productId, self.name, self.SKU_DETAIL_ID, conn)
        # 京东最多只返回100页数据
        for i in range(100):
            try:  # 防止网页提取失败，使爬取终断，直接跳过失败页，继续爬取
                data['page'] = i
                html = self.getHtml(data, jd_url)
                if not html:
                    continue
                comm_dict = self.js2py(html, productId)
                if not comm_dict:
                    continue
                finish = self.getComment(comm_dict, productId)
                if finish:
                    break
            except Exception as e:
                jd_log(self.name, productId)
                continue
            time.sleep(2)
            if i % 10 == 0:
                time.sleep(5)


def main(urls):
    start = time.time()
    if len(urls) < 1 or isinstance(urls, list) is False:
        log_info("JD,无url信息或传入参数格式不是列表")
        return True
    for url in urls:
        today = JDNewReview()
        today.run(url)
    end = time.time()
    log_info("JD,耗时%s秒" % (end - start))
    print("JD_end,耗时%s秒" % (end - start))


# 定时运行
def jd_run(urls, h, m):
    while True:
        now = datetime.now()
        if now.hour == h and now.minute == m:
            r = main(urls)
            if r:
                break
        time.sleep(60)


if __name__ == '__main__':
    from urls import jd_urls
    urls = jd_urls()
    # jd_run(urls, 9, 9)
    main(urls)
