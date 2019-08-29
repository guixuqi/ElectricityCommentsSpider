# -*- coding: utf-8 -*-
# import io
# import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
import time
from time import sleep
import requests
from lxml import etree
import re
from retrying import retry
from utils import save_score, SKU_DETAIL_ID, review_split, save_review, c, conn, close_db, update_score


class KakakuReview:

    def __init__(self):
        self.url = "https://review.kakaku.com"
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
        self.sku_id = ""
        self.num = 0
        self.name = "kakaku"
        self.SKU_DETAIL_ID = ""
        self.ECOMMERCE_CODE = "33"
        self.max_date = None

    def get_url(self, url):
        try:
            self.sku_id = re.search(r"item/(\w+)", url).group(1)
        except:
            print(url + "格式不对")
            return False
        return "https://review.kakaku.com/review/{}/#tab".format(self.sku_id)

    @retry(stop_max_attempt_number=5)
    def parse_url(self, review_url):
        resp = requests.get(review_url, headers=self.headers, timeout=20)
        sleep(5)
        if resp.status_code != 200:
            raise Exception
        resp.encoding = "shift_jis"
        html = etree.HTML(resp.text)
        return html

    def parse_score(self, html):
        # self.SKU_DETAIL_ID = SKU_DETAIL_ID(self.sku_id, self.ECOMMERCE_CODE)
        # if not self.SKU_DETAIL_ID:
        #     print(self.sku_id+"查询不到SKU_DETAIL_ID")
        #     return True
        # 总评分
        try:
            total_score = html.xpath("//div[@class='revstar']/span[@class='impact01']/text()")
            total_score = float(total_score[0])
        except Exception as e:
            print(self.sku_id+"获取总评分失败", e)
            total_score = 0
        # print(total_score)
        # 保存评分
        if save_score(self.sku_id, total_score, self.name, self.SKU_DETAIL_ID, conn):
            update_score(total_score, self.sku_id, self.name, self.SKU_DETAIL_ID, conn)

    def parse_review(self, html):
        divs = html.xpath("//div[@class='reviewBox ver2013 boxGr']")
        # print(len(divs))
        if len(divs) < 1:
            print(self.sku_id+"评论主标签获取失败")
            return True
        for div in divs:
            try:
                # 评论ID preceding-sibling::a[1]
                review_id = self.SKU_DETAIL_ID + "_" + div.xpath("./preceding-sibling::div[1]/@id")[0]
                # 评论星级
                score = div.xpath(".//div[@class='revRateBox type2']/table[@class='total']/tbody/tr/td/text()")[0]
                # 评论人
                name = div.xpath(".//span[@class='userName']/a/text()")
                if not name:
                    name = div.xpath(".//span[@class='userName']/a//span[@itemprop='name']/text()")
                    date = div.xpath(".//p[@class='entryDate clearfix']/span/@content")[0].replace("-", "/")
                else:
                    # 评论时间  2019年7月20日 10:23 [1243163-2]
                    date = div.xpath(".//p[@class='entryDate clearfix']/text()")[0].split(" ")[0]
                    dataStr = re.search(r"(\d+)\D+(\d+)\D+(\d+)", date)
                    date = dataStr.group(1) + "/" + dataStr.group(2) + "/" + dataStr.group(3)
                name = name[0]
                # 评论标题
                title = div.xpath(".//div[@class='reviewTitle']/span/a/text()")[0]
                # 评论内容
                text = div.xpath(".//p[@class='revEntryCont']/text()")
                text = "".join(text).replace("\n", "\t")
                REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_TEXT5 = review_split(
                    text.replace("\n", "\t"))
                REVIEW_TEXT5 += "  from_Kakaku"
            except Exception as e:
                print(self.sku_id+str(self.num)+"提取评论信息失败", e)
                continue
            print(review_id, score, name, date, title, text)
            sql = save_review(review_id, self.sku_id, score, name, title, REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, date, REVIEW_TEXT5, self.SKU_DETAIL_ID)
            try:
                c.execute(sql)
                conn.commit()
                self.num += 1
            except Exception as e:
                print(e, "{}({})保存失败".format(self.name, self.sku_id))
                # logger(self.name, self.sku_id, "保存失败")
                conn.rollback()

    def run(self, start_url):
        url = start_url.split("$$$")[0]
        self.SKU_DETAIL_ID = start_url.split("$$$")[1]
        review_url = self.get_url(url)
        if not review_url:
            return
        html = self.parse_url(review_url)
        if self.parse_score(html):
            return
        if self.parse_review(html):
            print("kakaku,{}共更新了{}条,".format(self.sku_id, self.num))
            # log_info("kakaku,{}更新了{}条,".format(self.SKU_ID, self.num))
            return
        next_url = html.xpath("//a[text()='次のページへ']/@href")
        while next_url:
            next_html = self.parse_url(self.url + next_url[0])
            if self.parse_review(next_html):
                print("kakaku,{}共更新了{}条,".format(self.sku_id, self.num))
                # log_info("kakaku,{}更新了{}条,".format(self.SKU_ID, self.num))
                return
            next_url = next_html.xpath("//a[text()='次のページへ']/@href")
        print("kakaku,{}共抓取了{}条,".format(self.sku_id, self.num))


def run(urls):
    start = time.time()
    if len(urls) < 1 or isinstance(urls, list) is False:
        return True
    for url in urls:
        ka = KakakuReview()
        ka.run(url)
        # time.sleep(3)
    # close_db()
    end = time.time()
    print("kakaku_end,%s" % (end - start))
    # log_info("ear_end,%s" % (end - start))


if __name__ == '__main__':
    from urls import kakaku_urls
    us = kakaku_urls()
    # us = ["https://kakaku.com/item/J0000030671/"]
    run(us)
