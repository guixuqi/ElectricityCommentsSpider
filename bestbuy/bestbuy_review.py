import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, ""))
import re
from datetime import datetime
import time
import requests
from lxml import etree
from retrying import retry
from utils import close_db, get_ua, review_split, save_score, save_review, logger, log_info, SKU_DETAIL_ID, c, conn, \
    max_date


class BestBuyReview:

    def __init__(self):
        self.name = "BestBuy"
        self.header = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
        self.dict = {}
        self.comments_list = []
        self.comment_num = 0
        self.sku_id = ""
        self.url = ""
        self.ECOMMERCE_CODE = "100"
        self.SKU_DETAIL_ID = ""
        self.max_date = None

    def get_url(self, url):
        s1 = re.search(r".*(\.p\?.*)", url)
        self.url = url.replace("site/", "site/reviews/")
        self.url = self.url.replace(s1.group(1), "")
        # SKU_ID
        self.sku_id = re.search(r"/site/reviews/.*/(\d+)", self.url).group(1)
        # 查询数据库评论最晚日期
        self.max_date = max_date(self.sku_id)

    @retry(stop_max_attempt_number=5)
    def parse_url(self, number=5):
        kw = {"page": 1, "rating": number, "sort": "MOST_RECENT"}
        try:
            resp = requests.get(self.url, headers=self.header, params=kw, timeout=60)
            # print(resp.url)
            html = etree.HTML(resp.content.decode())
        except:
            logger(self.name, self.url, "请求失败")
            html = False
        return html

    @retry(stop_max_attempt_number=5)
    def parse_next_url(self, next_url):
        next_resp = requests.get(next_url, headers=self.header, timeout=10)
        next_html = etree.HTML(next_resp.content.decode())
        return next_html

    def get_content_list(self, html):
        # 总评分
        total_score_list = html.xpath("//span[@class='overall-rating']/text()")
        if total_score_list:
            self.dict["total_score"] = "".join(total_score_list).strip()
            score = self.dict["total_score"]
            score = float(score)
        else:
            log_info("{}无总评分数据".format(self.sku_id))
            score = 0
        # 保存
        # 以SKU_ID和ECOMMERCE_CODE联合查询ECOMMERCE_SKU_DETAIL表SKU_DETAIL_ID的值
        if not SKU_DETAIL_ID(self.sku_id, self.ECOMMERCE_CODE):
            return True
        self.SKU_DETAIL_ID = SKU_DETAIL_ID(self.sku_id, self.ECOMMERCE_CODE)
        # 保存总评分
        save_score(self.sku_id, score, self.name, self.SKU_DETAIL_ID)
        # 评论内容(以评论星级分类(1-5)爬取)
        for number in reversed(range(1, 6)):
            self.comments_list = []
            if number > 1:
                html = self.parse_url(number)
            if self.comment_datas(html, number):
                continue

    def next_url(self, html):
        next_url = html.xpath("//li[@class='page next']/a/@href")
        if len(next_url) > 0:
            next_url = "https://www.bestbuy.com" + next_url[0]
        else:
            next_url = None
        return next_url

    def comment_datas(self, html, number):
        if self.comment_data(html, number):
            return True
        next_url = self.next_url(html)
        # 翻页
        while next_url:
            next_html = self.parse_next_url(next_url)
            # time.sleep(5)
            if self.comment_data(next_html, number):
                return True
            next_url = self.next_url(next_html)
        log_info("BestBuy,{}共更新了{}条,".format(self.sku_id, self.comment_num))

    def comment_data(self, html, number):
        comments_lis = html.xpath("//ul[@class='reviews-list']/li")
        if len(comments_lis) < 1:
            log_info("{}({})获取评论主标签失败".format(self.name, self.sku_id))
            return True
        for li in comments_lis:
            comment_dict = {}
            comment_dict['num'] = self.comment_num
            try:
                # 评论标题
                comment_dict['comment_title'] = li.xpath(
                    ".//h3[@class='ugc-review-title c-section-title heading-5 v-fw-medium  ']/text()")[0]
                # 评论时间
                comment_dict['comment_time'] = li.xpath(".//time[@class='submission-date']/@title")[0]
                # print(comment_dict['comment_time'])
                flag = comment_dict['comment_time']
                timeStr = flag.split(" ")
                # 拼接时间字符串
                dataStr = timeStr[0] + "/" + timeStr[1].replace(",", "") + "/" + timeStr[2]
                # print(dataStr)
                import locale
                locale.setlocale(locale.LC_ALL, 'en_US')
                REVIEW_DATE = datetime.strptime(dataStr, "%b/%d/%Y").strftime('%Y/%m/%d')
                locale.setlocale(locale.LC_ALL, 'C')
                # print(REVIEW_DATE)
                # 评论用户
                comment_dict['comment_user'] = li.xpath(
                    ".//div[@class='visible-xs visible-sm ugc-author v-fw-medium body-copy-lg']/text()")[0]
                # print(comment_dict['comment_user'])
                # 评论内容
                comment_dict['comment_content'] = li.xpath(".//p[@class='pre-white-space']/text()")[0]
                self.comments_list.append(comment_dict)
                # 评论ID
                REVIEW_ID = li.xpath(".//h3[@class='ugc-review-title c-section-title heading-5 v-fw-medium  ']/@id")
                REVIEW_ID = re.match(r"review-id-(.*)", REVIEW_ID[0]).group(1)
                REVIEW_TEXT = comment_dict['comment_content']
                # 评论内容分拆
                REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_TEXT5 = review_split(REVIEW_TEXT)
                REVIEW_TEXT5 += "  from_BestBuy"
            except Exception as e:
                # print("提取内容失败,原因:{}".format(e))
                logger(self.name, self.sku_id, "提取内容失败")
                continue
            # 保存数据库
            sql = save_review(REVIEW_ID, self.sku_id, number, comment_dict['comment_user'], comment_dict['comment_title'], REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_DATE, REVIEW_TEXT5, self.SKU_DETAIL_ID)
            try:
                c.execute(sql)
                conn.commit()
                self.comment_num += 1
            except Exception as e:
                # print(e, "{}({})保存失败".format(self.name, self.sku_id))
                logger(self.name, self.sku_id)
                conn.rollback()

    def star_percent(self, html, num):
        rating_bars = html.xpath("//button[@data-track='Summary: Bar Graph: {} Star']".format(num))[0]
        star = rating_bars.xpath(".//span[@class='star']/text()")[0]
        percent = rating_bars.xpath(".//span[@class='percent']/text()")
        return star, percent

    def run(self, url):
        try:
            self.get_url(url)
        except Exception as e:
            logger(self.name, self.sku_id, "url格式不符合要求")
            return
        html_str = self.parse_url()
        if html_str is False:
            return
        self.get_content_list(html_str)


def run(urls):
    start = time.time()
    if len(urls) < 1 or isinstance(urls, list) is False:
        # print("无url信息或传入参数格式不是列表")
        log_info("BestBuy,无url信息或传入参数格式不是列表")
        return True
    for url in urls:
        b = BestBuyReview()
        b.run(url)
    # 关闭数据库
    # close_db()
    end = time.time()
    print('BestBuy_end,耗时%s秒' % (end - start))
    log_info("BestBuy_end,耗时%s秒" % (end - start))


if __name__ == '__main__':
    from urls import bestbuy_urls
    urls = bestbuy_urls()
    run(urls)