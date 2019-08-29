# -*-coding:utf-8-*-
import cx_Oracle
import os
import sys
from multiprocessing.dummy import Pool
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, ""))
import re
from datetime import datetime
import time
import requests
from lxml import etree
from utils import get_ua, save_review, review_split, save_score, close_db, logger, log_info, SKU_DETAIL_ID, max_date, update_score
from retrying import retry
import locale

# 数据库配置
dsnStr = cx_Oracle.makedsn("192.168.110.214", 1521, "HORNEIP")  # 测试库
conn = cx_Oracle.connect("EIP", "EIP", dsnStr, threaded=True)
c = conn.cursor()


class AmazonReview:
    def __init__(self):
        self.name = "Amazon"
        self.amazon_url = ""
        self.headers = {'User-Agent': get_ua()}
        self.dict = {}
        self.comments_list = []
        self.comment_num = 0
        self.review_num = 0
        self.SKU_ID = ""
        self.ECOMMERCE_CODE = ""
        self.SKU_DETAIL_ID = ""
        self.max_d = None

    @retry(stop_max_attempt_number=5)
    def parse_url(self, url, kw=None):
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        s = requests.session()
        s.keep_alive = False  # 关闭多余连接
        resp = s.get(url, headers=self.headers, params=kw, timeout=100)
        print(resp.url)
        html = etree.HTML(resp.content.decode())
        return html

    def get_urls(self, start_url):
        # 拼接生成评论页面的url
        review_url = start_url.replace("/dp/", "/product-reviews/")
        kw = {"filterByLanguage": "en_US", "sortBy": "recent"}
        if re.search(r".de", review_url) or re.search(r".fr", review_url):
            kw = {"sortBy": "recent"}
        elif re.search(r".co.jp", review_url):
            kw = {"sortBy": "recent", "language": "zh_CN"}
        html = self.parse_url(review_url, kw)
        return html

    def next_url(self, html):
        next_url = html.xpath("//li[@class='a-last']/a/@href")
        if len(next_url) > 0:
            next_url = self.amazon_url + next_url[0]
        else:
            next_url = None
        return next_url

    def get_score(self, html, sku_id):
        try:
            total_score = html.xpath("//span[@class='arp-rating-out-of-text']/text()")
            score = re.match(r"(\S+)", total_score[0]).group(1).replace(",", ".")
            score = float(score)
        except Exception as e:
            # print(e, "无总评分数据")
            logger(self.name, sku_id, "无总评分数据")
            score = 0
        print(score)

    def comment_datas(self, html):
        # 提取保存总评分
        if self.get_score(html, self.SKU_ID):
            return True
        # 提取评论数据
        if self.comment_data(html):
            return True
        # 提取下一页url
        next_url = self.next_url(html)
        # 翻页
        nn = 0
        while next_url:
            try:
                if re.search(r".co.jp", next_url):
                    kw = {"language": "zh_CN"}
                    next_html = self.parse_url(next_url, kw)
                else:
                    next_html = self.parse_url(next_url)
            except Exception as e:
                print(e, "请求{}失败".format(next_url))
                # logger(self.name, start_url, "请求失败")
                continue
            # time.sleep(1)
            if self.comment_data(next_html):
                return True
            next_url = self.next_url(next_html)
            nn += 1
            print(self.SKU_ID, nn)

    def comment_data(self, html):
        comments_divs = html.xpath("//div[@id='cm_cr-review_list']/div")
        if len(comments_divs) < 1:
            # print("获取评论主标签失败")
            log_info("{}({})获取评论主标签失败".format(self.name, self.SKU_ID))
            return True
        for div in comments_divs:
            self.review_num += 1
            comment_dict = {}
            comment_dict['num'] = self.comment_num
            # 评论ID
            if len(div.xpath("./@id")) > 0:
                REVIEW_ID = self.SKU_DETAIL_ID + "_" + div.xpath("./@id")[0]
            else:
                continue
            # 评论标题
            comment_title = div.xpath(
                ".//a[@data-hook='review-title']/span/text()")
            comment_dict['comment_title'] = comment_title[0] if len(comment_title) > 0 else ""
            # print(comment_dict['comment_title'])
            # 评论时间
            comment_time = div.xpath(".//span[@data-hook='review-date']/text()")
            comment_dict['comment_time'] = comment_time[0] if len(comment_time) > 0 else ""
            if comment_dict['comment_time']:
                flag = comment_dict['comment_time']
                # print(flag)
                timeList = flag.split(" ")
                # 拼接时间字符串
                if re.search(r".com", self.amazon_url):
                    dataStr = timeList[0] + "/" + timeList[1].replace(",", "") + "/" + timeList[2]
                    locale.setlocale(locale.LC_ALL, 'en_US')
                    re_date = datetime.strptime(dataStr, "%B/%d/%Y")
                elif re.search(r".co.uk", self.amazon_url):
                    dataStr = timeList[1] + "/" + timeList[0] + "/" + timeList[2]
                    locale.setlocale(locale.LC_ALL, 'en_US')
                    re_date = datetime.strptime(dataStr, "%B/%d/%Y")
                elif re.search(r".de", self.amazon_url):
                    dataStr = timeList[1] + "/" + timeList[0].replace(".", "") + "/" + timeList[2]
                    # 设置本地时间格式为德语
                    locale.setlocale(locale.LC_ALL, 'de_DE')
                    re_date = datetime.strptime(dataStr, "%B/%d/%Y")
                elif re.search(r".fr", self.amazon_url):
                    dataStr = timeList[1] + "/" + timeList[0].replace(".", "") + "/" + timeList[2]
                    # 设置本地时间格式为法语
                    locale.setlocale(locale.LC_ALL, 'fr_FR')
                    re_date = datetime.strptime(dataStr, "%B/%d/%Y")
                elif re.search(r".co.jp", self.amazon_url):
                    dataStr = re.search(r"(\d+)\D+(\d+)\D+(\d+)", flag)
                    dataStr = dataStr.group(1) + "/" + dataStr.group(2) + "/" + dataStr.group(3)
                    re_date = datetime.strptime(dataStr, "%Y/%m/%d")
                    # print(dataStr)
                else:
                    return True
                locale.setlocale(locale.LC_ALL, "C")
                REVIEW_DATE = re_date.strftime('%Y/%m/%d')
            else:
                REVIEW_DATE = datetime.now().strftime('%Y/%m/%d')
            # 评论用户
            comment_user = div.xpath(
                ".//span[@class='a-profile-name']/text()")
            comment_dict['comment_user'] = comment_user[0] if len(comment_user) > 0 else ""
            # 评论星级
            score = div.xpath(".//span[@class='a-icon-alt']/text()")[0].split(" ")[0].replace(",", ".")
            score = float(score)
            # print(score)
            # 评论内容
            comment_dict['comment_content'] = " ".join(div.xpath(".//span[@data-hook='review-body']/span/text()"))
            self.comments_list.append(comment_dict)
            REVIEW_TEXT = comment_dict['comment_content']
            if not REVIEW_TEXT:
                log_info("第{}条无内容".format(self.review_num))
                continue
            # 评论内容分拆
            REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_TEXT5 = review_split(REVIEW_TEXT)
            REVIEW_TEXT5 += "  from_amazon"
            # 保存到数据库
            sql = save_review(REVIEW_ID, self.SKU_ID, score, comment_dict['comment_user'], comment_dict['comment_title'], REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_DATE, REVIEW_TEXT5, self.SKU_DETAIL_ID)
            try:
                c.execute(sql)
                conn.commit()
                self.comment_num += 1
            except Exception as e:
                print(e, "{}({})保存失败".format(self.name, self.SKU_ID))
                logger(self.name, self.SKU_ID, "保存失败")
                conn.rollback()

    def run(self, url):
        start_url = url.split("$$$")[0]
        self.SKU_DETAIL_ID = url.split("$$$")[1]
        try:
            self.SKU_ID = re.search(r".*/dp/(\w+)", start_url).group(1)
        except Exception as e:
            # print(e, "url格式不对")
            logger(self.name, start_url, "url格式不对")
            return []
        # 判断美国,英国,德国网站
        if re.search(r".com", start_url):
            self.amazon_url = "https://www.amazon.com"
            self.ECOMMERCE_CODE = "1"
        elif re.search(r".co.uk", start_url):
            self.amazon_url = "https://www.amazon.co.uk"
            self.ECOMMERCE_CODE = "2"
        elif re.search(r".de", start_url):
            self.amazon_url = "https://www.amazon.de"
            self.ECOMMERCE_CODE = "4"
        elif re.search(r".co.jp", start_url):
            self.amazon_url = "https://www.amazon.co.jp"
            self.ECOMMERCE_CODE = "3"
        elif re.search(r".fr", start_url):
            self.amazon_url = "https://www.amazon.fr"
            self.ECOMMERCE_CODE = "5"
        else:
            log_info("暂不支持爬取此类网站数据")
            return True
        try:
            # 把start_url转为评论url
            review_html = self.get_urls(start_url)
        except Exception as e:
            # print(e, "请求{}失败".format(start_url))
            logger(self.name, start_url, "请求失败")
            return
        if self.comment_datas(review_html):
            print("amazon,{}共更新了{}条,".format(self.SKU_ID, self.comment_num))
            log_info("amazon,{}共更新了{}条,".format(self.SKU_ID, self.comment_num))
            return
        print(len(self.comments_list))
        print("amazon,{}共抓取了{}条,".format(self.SKU_ID, self.comment_num))


def run(urls):
    import threading
    import queue
    start = time.time()
    if len(urls) < 1 or isinstance(urls, list) is False:
        # print("无url信息或传入参数格式不是列表")
        log_info("Amazon,无url信息或传入参数格式不是列表")
        return True
    q = queue.Queue()
    for url in urls:
        # amazon = AmazonReview()
        # amazon.run(url)
        # time.sleep(3)
        t = threading.Thread(target=AmazonReview().run, args=(url,))
        q.put(t)
    while not q.empty():
        t = q.get()
        q.task_done()
        t.start()
    q.join()
    # 关闭数据库
    # close_db()
    end = time.time()
    print('amazon_end,耗时%s秒' % (end - start))


if __name__ == '__main__':
    # from urls import amazon_urls
    # urls = amazon_urls()
    start_url0 = "https://www.amazon.com/Zolo-True-Wireless-Headphones-Technology-Calls-Upgraded/dp/B07GKHYVM8/ref=sxbs_sxwds-stvp"+"$$$"+"0000"
    start_url1 = "https://www.amazon.com/ASTRO-Gaming-A10-Headset-Black-Red/dp/B071S9RGB1/ref=sr_1_1"+"$$$"+"1111"
    urls = [start_url0, start_url1]
    run(urls)
