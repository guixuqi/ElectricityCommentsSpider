import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, ""))
import re
import time
from datetime import datetime
from bestbuy.bestbuy_review import BestBuyReview
from urls import bestbuy_urls
from utils import update_score, save_review, review_split, newReview, logger, log_info, c, conn, SKU_DETAIL_ID


class BestBuyNewReview(BestBuyReview):

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
        # 更新数据库评分
        if not SKU_DETAIL_ID(self.sku_id, self.ECOMMERCE_CODE):
            return True
        self.SKU_DETAIL_ID = SKU_DETAIL_ID(self.sku_id, self.ECOMMERCE_CODE)
        update_score(score, self.sku_id, self.name, self.SKU_DETAIL_ID)
        for number in reversed(range(1, 6)):
            self.comments_list = []
            if number < 5:
                try:
                    html = self.parse_url(number)
                except:
                    print("{}星级{}请求失败".format(self.sku_id, number))
                    continue
            star_num = "star_{}".format(number)
            if self.comment_datas(html, number):
                continue
            self.dict[star_num] = self.comments_list

    def comment_data(self, html, number):
        comments_lis = html.xpath("//ul[@class='reviews-list']/li")
        if len(comments_lis) < 1:
            log_info("{}({})获取评论主标签失败".format(self.name, self.sku_id))
            return True
        n = 0
        for li in comments_lis:
            comment_dict = {}
            comment_dict['num'] = self.comment_num
            try:
                # 评论时间
                comment_dict['comment_time'] = li.xpath(".//time[@class='submission-date']/@title")[0]
                # print(comment_dict['comment_time'])
                flag = comment_dict['comment_time']
                timeStr = flag.split(" ")
                # 拼接时间字符串
                dataStr = timeStr[0] + "/" + timeStr[1].replace(",", "") + "/" + timeStr[2]
                import locale
                locale.setlocale(locale.LC_ALL, 'en_US')
                re_date = datetime.strptime(dataStr, "%b/%d/%Y")
                REVIEW_DATE = re_date.strftime('%Y/%m/%d')
                locale.setlocale(locale.LC_ALL, 'C')
                # print(REVIEW_DATE0)
                # 只爬取新的评论
                if newReview(self.max_date, re_date):
                    n += 1
                    if n < 3:
                        continue
                    else:
                        return True
                # 评论标题
                comment_dict['comment_title'] = li.xpath(
                    ".//h3[@class='ugc-review-title c-section-title heading-5 v-fw-medium  ']/text()")[0]
                # 评论用户
                comment_dict['comment_user'] = li.xpath(
                    ".//div[@class='visible-xs visible-sm ugc-author v-fw-medium body-copy-lg']/text()")[0]
                # 评论内容
                comment_dict['comment_content'] = li.xpath(".//p[@class='pre-white-space']/text()")[0]
                self.comments_list.append(comment_dict)
                # 评论ID
                REVIEW_ID = li.xpath(".//h3[@class='ugc-review-title c-section-title heading-5 v-fw-medium  ']/@id")
                REVIEW_ID = self.SKU_DETAIL_ID + "_" + re.match(r"review-id-(.*)", REVIEW_ID[0]).group(1)
                REVIEW_TEXT = comment_dict['comment_content']
                # 评论内容分拆
                REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_TEXT5 = review_split(REVIEW_TEXT)
                REVIEW_TEXT5 += "  from_BestBuy"
            except Exception as e:
                # print("提取内容失败,原因:{}".format(e))
                logger(self.name, self.sku_id, "提取内容失败")
                continue
            # 保存数据库
            sql = save_review(REVIEW_ID, self.sku_id, number, comment_dict['comment_user'],
                              comment_dict['comment_title'], REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4,
                              REVIEW_DATE, REVIEW_TEXT5, self.SKU_DETAIL_ID)
            try:
                c.execute(sql)
                conn.commit()
                self.comment_num += 1
            except Exception as e:
                # print(e, "{}({})保存失败".format(self.name, self.sku_id))
                logger(self.name, self.sku_id)
                conn.rollback()


def main(urls):
    if len(urls) < 1 or isinstance(urls, list) is False:
        # print("无url信息或传入参数格式不是列表")
        log_info("BestBuy,无url信息或传入参数格式不是列表")
        return True
    start = time.time()
    for url in urls:
        best = BestBuyNewReview()
        best.run(url)
    end = time.time()
    log_info("BestBuy_end,耗时%s秒" % (end - start))
    print("BestBuy_end,耗时%s秒" % (end - start))


# 定时运行
def bestbuy_run(urls, h, m):
    while True:
        now = datetime.now()
        if now.hour == h and now.minute == m:
            r = main(urls)
            if r:
                break
        time.sleep(60)


if __name__ == '__main__':
    urls = bestbuy_urls()
    # bestbuy_run(urls, 9, 30)
    main(urls)
