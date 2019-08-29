import time
from time import sleep
import requests
from lxml import etree
import re
from retrying import retry
from utils import save_score, SKU_DETAIL_ID, review_split, save_review, c, conn, close_db, update_score


class EarphoneReview:

    def __init__(self):
        self.url_star = "https://timemachine2016.jp/detail/detail_set.php"
        self.url_review = "https://timemachine2016.jp/review/review_ajax.php"
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
        self.sku_id = ""
        self.num = 0
        self.name = "e-earphone"
        self.SKU_DETAIL_ID = ""
        self.ECOMMERCE_CODE = "34"
        self.max_date = None

    @retry(stop_max_attempt_number=5)
    def parse_url(self, url, data):
        resp = requests.post(url, headers=self.headers, data=data, timeout=10)
        sleep(3)
        if resp.status_code != 200:
            raise Exception
        # html = etree.HTML(resp.content.decode("EUC-JP"))  # charset=EUC-JP
        html = etree.HTML(resp.text)
        return html

    def parse_score(self, url):
        # sku_id
        try:
            self.sku_id = re.search(r"shopdetail/(\d+)", url).group(1)
        except:
            print(url + "格式不对")
            return True
        data = {"webno": self.sku_id}
        try:
            html = self.parse_url(self.url_star, data)
        except Exception as e:
            print(self.sku_id+self.url_star+"请求失败", e)
            return True
        # self.SKU_DETAIL_ID = SKU_DETAIL_ID(self.sku_id, self.ECOMMERCE_CODE)
        # if not self.SKU_DETAIL_ID:
        #     print(self.sku_id+"查询不到SKU_DETAIL_ID")
        #     return True
        # 总评分
        try:
            total_score = html.xpath(
                "//li[@class='detail_status_level_top']//div[@class='detail_status_level_point']/p/text()")
            total_score = float(total_score[0])
        except Exception as e:
            print(self.sku_id+"获取总评分失败", e)
            total_score = 0
        # print(total_score)
        # 保存评分
        if save_score(self.sku_id, total_score, self.name, self.SKU_DETAIL_ID, conn):
            update_score(total_score, self.sku_id, self.name, self.SKU_DETAIL_ID, conn)

    def parse_review(self):
        data = {"webno": self.sku_id, "fstaff": 0}
        try:
            html = self.parse_url(self.url_review, data)
        except Exception as e:
            print(self.sku_id+self.url_review+"请求失败", e)
            return True
        # if not html:
        #     print(self.sku_id+"无评论数据")
        #     return True
        divs = html.xpath("//div[@class='cnt-review']")
        # print(len(divs))
        if len(divs) < 1:
            print(self.sku_id+"评论主标签获取失败")
            return True
        for div in divs:
            try:
                # 评论ID
                review_id = self.SKU_DETAIL_ID + "_" + div.xpath("./div[@class='review-right']/span[@class='cnt-su']/@id")[0]
                # 评论星级
                score = div.xpath(".//div[@class='star-det']//div[@class='h-point']/text()")[0]
                # 评论人
                name = div.xpath(".//div[@class='name']/text()")[0]
                # 评论时间  [2019/05/02 23:27]
                date = div.xpath(".//div[@class='day']/text()")[0]
                try:
                    date = re.search(r"\[(.*)\]", date).group(1).split(" ")[0]
                except:
                    print(self.sku_id + str(self.num) + "网页评论时间格式有变")
                    continue
                # 评论标题
                title = div.xpath(".//div[@class='title']/text()")[0]
                # 评论内容
                text = div.xpath("./div[@class='review-right']/div[@class='review']/div/text()")[0].replace("\n", "\t")
            except Exception as e:
                print(self.sku_id+str(self.num)+"提取评论信息失败", e)
                continue
            # print(id, score, name, date, title, text)
            REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_TEXT5 = review_split(
                text.replace("\n", "\t"))
            REVIEW_TEXT5 += "  from_Earphone"
            sql = save_review(review_id, self.sku_id, score, name, title, REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, date, REVIEW_TEXT5, self.SKU_DETAIL_ID)
            try:
                c.execute(sql)
                conn.commit()
                self.num += 1
            except Exception as e:
                print(e, "{}({})保存失败".format(self.name, self.sku_id))
                # logger(self.name, self.sku_id, "保存失败")
                conn.rollback()
        print(self.num)

    def run(self, start_url):
        url = start_url.split("$$$")[0]
        self.SKU_DETAIL_ID = start_url.split("$$$")[1]
        if self.parse_score(url):
            return
        if self.parse_review():
            print("ear,{}共更新了{}条,".format(self.sku_id, self.num))
            # log_info("ear,{}更新了{}条,".format(self.SKU_ID, self.num))
            return
        print("ear,{}共抓取了{}条,".format(self.sku_id, self.num))


def run(urls):
    start = time.time()
    if len(urls) < 1 or isinstance(urls, list) is False:
        return True
    for url in urls:
        ear = EarphoneReview()
        ear.run(url)
        # time.sleep(3)
    end = time.time()
    print("ear_end,%s" % (end - start))
    # log_info("ear_end,%s" % (end - start))


if __name__ == '__main__':
    from urls import e_ear_urls
    us = e_ear_urls()
    # us = ["https://www.e-earphone.jp/shopdetail/000000206585"]
    run(us)
