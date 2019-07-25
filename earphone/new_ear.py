import time
from datetime import datetime
from time import sleep
import requests
from lxml import etree
import re
from retrying import retry
from earphone.earphone_review import EarphoneReview
from utils import save_score, SKU_DETAIL_ID, review_split, save_review, c, conn, close_db, update_score, max_date, newReview


class EarphoneNewReview(EarphoneReview):

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
        self.SKU_DETAIL_ID = SKU_DETAIL_ID(self.sku_id, self.ECOMMERCE_CODE)
        if not self.SKU_DETAIL_ID:
            print(self.sku_id+"查询不到SKU_DETAIL_ID")
            return True
        self.max_date = max_date(self.SKU_DETAIL_ID)
        # 总评分
        try:
            total_score = html.xpath(
                "//li[@class='detail_status_level_top']//div[@class='detail_status_level_point']/p/text()")
            total_score = float(total_score[0])
        except Exception as e:
            print(self.sku_id+"获取总评分失败", e)
            total_score = 0
        # print(total_score)
        # 更新评分
        update_score(total_score, self.sku_id, self.name, self.SKU_DETAIL_ID)

    def parse_review(self):
        data = {"webno": self.sku_id, "fstaff": 0}
        try:
            html = self.parse_url(self.url_review, data)
        except Exception as e:
            print(self.sku_id+self.url_review+"请求失败", e)
            return True
        if not html:
            print(self.sku_id+"无评论数据")
            return True
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
                re_date = datetime.strptime(date, "%Y/%m/%d")
                if newReview(self.max_date, re_date):
                    return True
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
            REVIEW_TEXT5 += "  from_Bicc"
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


def main(urls):
    start = time.time()
    if len(urls) < 1 or isinstance(urls, list) is False:
        return True
    for url in urls:
        ear = EarphoneNewReview()
        ear.run(url)
        # time.sleep(3)
    close_db()
    end = time.time()
    print("ear_end,%s" % (end - start))
    # log_info("ear_end,%s" % (end - start))


if __name__ == '__main__':
    from urls import e_ear_urls
    us = e_ear_urls()
    # us = ["https://www.e-earphone.jp/shopdetail/000000206585"]
    main(us)
