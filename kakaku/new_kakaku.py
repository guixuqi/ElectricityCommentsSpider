# -*- coding: utf-8 -*-
from datetime import datetime
from kakaku.kakaku_review import KakakuReview
import time
import re
from utils import save_score, SKU_DETAIL_ID, review_split, save_review, c, conn, close_db, update_score, max_date, newReview


class KakakuNewReview(KakakuReview):

    def parse_score(self, html):
        # self.SKU_DETAIL_ID = SKU_DETAIL_ID(self.sku_id, self.ECOMMERCE_CODE)
        # if not self.SKU_DETAIL_ID:
        #     print(self.sku_id+"查询不到SKU_DETAIL_ID")
        #     return True
        self.max_date = max_date(self.SKU_DETAIL_ID)
        # 总评分
        try:
            total_score = html.xpath("//div[@class='revstar']/span[@class='impact01']/text()")
            total_score = float(total_score[0])
        except Exception as e:
            print(self.sku_id+"获取总评分失败", e)
            total_score = 0
        # 更新评分
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
                re_date = datetime.strptime(date, "%Y/%m/%d")
                if newReview(self.max_date, re_date):
                    return True
                # 评论标题
                title = div.xpath(".//div[@class='reviewTitle']/span/a/text()")[0]
                # 评论内容
                text = div.xpath(".//p[@class='revEntryCont']/text()")
                text = "".join(text).replace("\n", "\t")
                REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_TEXT5 = review_split(text.replace("\n", "\t"))
                REVIEW_TEXT5 += "  from_Kakaku"
            except Exception as e:
                print(self.sku_id+str(self.num)+"提取评论信息失败", e)
                continue
            # print(review_id, score, name, date, title, text)
            sql = save_review(review_id, self.sku_id, score, name, title, REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, date, REVIEW_TEXT5, self.SKU_DETAIL_ID)
            try:
                c.execute(sql)
                conn.commit()
                self.num += 1
            except Exception as e:
                print(e, "{}({})保存失败".format(self.sku_id, self.num))
                # logger(self.name, self.sku_id, "保存失败")
                conn.rollback()


def main(urls):
    start = time.time()
    if len(urls) < 1 or isinstance(urls, list) is False:
        return True
    for url in urls:
        ka = KakakuNewReview()
        ka.run(url)
        # time.sleep(3)
    end = time.time()
    print("kakaku_end,%s" % (end - start))
    # log_info("ear_end,%s" % (end - start))


if __name__ == '__main__':
    from urls import kakaku_urls
    us = kakaku_urls()
    # us = ["https://kakaku.com/item/J0000030671/"]
    main(us)
