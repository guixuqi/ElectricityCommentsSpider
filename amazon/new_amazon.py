import re
import time
from datetime import datetime
from Logs.log import log1
from amazon.amazon_review import AmazonReview
from utils import update_score, save_review, review_split, close_db, newReview, log_info, logger, conn, c, SKU_DETAIL_ID, max_date
import locale


class AmazonNewReview(AmazonReview):

    def comment_data(self, html):
        comments_divs = html.xpath("//div[@id='cm_cr-review_list']/div")
        if len(comments_divs) < 1:
            # print("获取评论主标签失败")
            log_info("{}({})获取评论主标签失败".format(self.name, self.SKU_ID))
            return True
        n = 0
        for div in comments_divs:
            try:
                comment_dict = {}
                comment_dict['num'] = self.comment_num
                # 评论时间
                comment_time = div.xpath(".//span[@data-hook='review-date']/text()")
                comment_dict['comment_time'] = comment_time[0] if len(comment_time) > 0 else ""
                if comment_dict['comment_time']:
                    flag = comment_dict['comment_time']
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
                    else:
                        return True
                    locale.setlocale(locale.LC_ALL, "C")
                    REVIEW_DATE = re_date.strftime('%Y/%m/%d')
                    # 只爬取新的评论
                    # print(re_date)
                    # if newReview(re_date):
                    #     return True
                    # 查询数据库评论最晚日期
                    if newReview(self.max_d, re_date):
                        n += 1
                        if n < 3:
                            continue
                        else:
                            return True
                else:
                    REVIEW_DATE = datetime.now().strftime('%Y/%m/%d')
                # 评论ID
                if len(div.xpath("./@id")) > 0:
                    REVIEW_ID = self.SKU_DETAIL_ID + "_" + div.xpath("./@id")[0]
                else:
                    continue
                # 评论星级
                score = div.xpath(".//span[@class='a-icon-alt']/text()")[0].split(" ")[0].replace(",", ".")
                score = float(score)
                # 评论标题
                comment_title = div.xpath(
                    ".//a[@data-hook='review-title']/span/text()")
                comment_dict['comment_title'] = comment_title[0] if len(comment_title) > 0 else ""
                # 评论用户
                comment_user = div.xpath(
                    ".//span[@class='a-profile-name']/text()")
                comment_dict['comment_user'] = comment_user[0] if len(comment_user) > 0 else ""
                # 评论内容
                comment_dict['comment_content'] = " ".join(div.xpath(".//span[@data-hook='review-body']/span/text()"))
                self.comments_list.append(comment_dict)
                REVIEW_TEXT = comment_dict['comment_content']
                # 评论内容分拆
                REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_TEXT5 = review_split(REVIEW_TEXT)
                REVIEW_TEXT5 += "  from_amazon"
            except:
                # print("提取内容失败")
                logger(self.name, self.SKU_ID, "提取内容失败")
                continue
            # 保存到数据库
            sql = save_review(REVIEW_ID, self.SKU_ID, score, comment_dict['comment_user'], comment_dict['comment_title'], REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_DATE, REVIEW_TEXT5, self.SKU_DETAIL_ID)
            try:
                c.execute(sql)
                conn.commit()
                self.comment_num += 1
            except Exception as e:
                # print(e, "{}({})保存失败".format(self.name, self.SKU_ID))
                logger(self.name, self.SKU_ID)
                conn.rollback()

    def get_score(self, html, sku_id):
        try:
            total_score = html.xpath("//span[@class='arp-rating-out-of-text']/text()")
            score = re.match(r"(\S+)", total_score[0]).group(1).replace(",", ".")
        except Exception as e:
            # print(e)
            logger(self.name, sku_id, "无总评分数据")
            # score = "0"
            return
        # 更新总评分
        # if not SKU_DETAIL_ID(self.SKU_ID, self.ECOMMERCE_CODE):
        #     return True
        # self.SKU_DETAIL_ID = SKU_DETAIL_ID(self.SKU_ID, self.ECOMMERCE_CODE)
        self.max_d = max_date(self.SKU_DETAIL_ID)
        update_score(score, self.SKU_ID, self.name, self.SKU_DETAIL_ID, conn)


def main(urls):
    if len(urls) < 1 or isinstance(urls, list) is False:
        log_info("Amazon,无url信息或传入参数格式不是列表")
        return True
    start = time.time()
    for url in urls:
        amazon = AmazonNewReview()
        amazon.run(url)
    end = time.time()
    print("Amazon_end,耗时%s秒" % (end - start))
    log_info("Amazon_end,耗时%s秒" % (end - start))


# 定时运行
def amazon_run(urls, h, m):
    while True:
        now = datetime.now()
        if now.hour == h and now.minute == m:
            r = main(urls)
            if r:
                break
        time.sleep(60)


if __name__ == '__main__':
    # from urls import amazon_urls
    # urls = amazon_urls()
    urls = ["https://www.amazon.de/UNBREAKcable-Kabelloses-Qi-zertifizierte-Ladestation-Unterst%C3%BCtzt/dp/B07PN288W7/ref=sr_1_89?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&keywords=UNBREAKcable&qid=1563439003&s=gateway&sr=8-89$$$SKU-62788d49-3468-4ff2-a98d-477e1242dbec"]
    # amazon_run(urls, 11, 32)
    main(urls)
