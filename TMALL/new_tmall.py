import time
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from xpinyin import Pinyin

from TMALL.tmall_review import TMALLReview
from utils import review_split, c, logger, log_info, conn, review_days, SKU_DETAIL_ID, update_score, newReview


class TMALLNewReview(TMALLReview):

    def get_content_list(self):
        dr = self.driver
        try:
            dr.find_element_by_xpath("//*[text()='访问验证']")
            log_info("{},弹出访问验证输入框,被限制访问".format(self.name))
            return True
        except:
            pass
        try:
            # 定位评论标签tr
            tr_list = WebDriverWait(dr, 20).until(
                lambda driver: dr.find_elements_by_xpath("//div[@class='rate-grid']//tr"))
        except Exception as e:
            logger(self.name, self.SKU_ID, "定位评论内容主标签失败,原因:标签修改或网络异常")
            return True
        n = 0
        for tr in tr_list:
            # 生成不重复的评论ID
            # 查询数据库总数量
            # REVIEW_ID = self.SKU_ID + "_" + str(self.count)
            try:
                REVIEW_DATE = WebDriverWait(tr, 20).until(
                    lambda driver: tr.find_element_by_xpath(
                        ".//td[@class='tm-col-master']//div[@class='tm-rate-date']")).text
                date_list = REVIEW_DATE.split(".")
                now = datetime.now()
                now_str = now.strftime("%Y/%m/%d")
                now_year = now_str[0:4]
                if len(date_list) == 2:
                    date_list.insert(0, now_year)
                    REVIEW_DATE = "/".join(date_list)
                elif REVIEW_DATE == "今天":
                    REVIEW_DATE = now_str
                else:
                    REVIEW_DATE = REVIEW_DATE.replace(".", "/")
                review_date = datetime.strptime(REVIEW_DATE, "%Y/%m/%d")
                if newReview(self.max_date, review_date):
                    n += 1
                    if n < 3:
                        continue
                    else:
                        return True
                # if (now - review_date).days > review_days:
                #     # print(review_date)
                #     return True
                REVIEW_NAME = WebDriverWait(tr, 20).until(
                    lambda driver: tr.find_element_by_xpath(".//div[@class='rate-user-info']")).text
                REVIEW_TEXT = WebDriverWait(tr, 20).until(
                    lambda driver: tr.find_element_by_xpath(
                        ".//td[@class='tm-col-master']//div[@class='tm-rate-fulltxt']")).text
                REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_TEXT5 = review_split(REVIEW_TEXT)
                REVIEW_TEXT5 += "  from_TMALL"
            except Exception as e:
                logger(self.name, self.SKU_ID, "第{}条提取内容失败".format(self.num))
                continue
            # 生成评论ID
            REVIEW_ID = REVIEW_DATE.replace("/", "") + str(len(REVIEW_TEXT)) + str(Pinyin().get_pinyin(REVIEW_NAME.replace("*", "")).replace("-", ""))
            # print(REVIEW_ID)
            CREATE_TIME = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            # 保存ECOMMERCE_REVIEW_P数据库
            sql_review = "INSERT INTO ECOMMERCE_REVIEW_P(REVIEW_ID, SKU_ID, REVIEW_NAME, REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_DATE, CREATE_TIME, REVIEW_TEXT5, SKU_DETAIL_ID) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', to_date('{}','yyyy/MM/dd'), to_date('{}','yyyy/MM/dd HH24:mi:ss'),'{}', '{}')".format(
                REVIEW_ID, self.SKU_ID, REVIEW_NAME.replace("'", ""),
                REVIEW_TEXT1.replace("'", ""),
                REVIEW_TEXT2.replace("'", ""), REVIEW_TEXT3.replace("'", ""), REVIEW_TEXT4.replace("'", ""),
                REVIEW_DATE, CREATE_TIME, REVIEW_TEXT5.replace("'", ""), self.SKU_DETAIL_ID)
            try:
                c.execute(sql_review)
                conn.commit()
                # self.count += 1
                self.num += 1
            except Exception as e:
                # print(e, "第{}条评论保存失败".format(self.num))
                logger(self.name, self.SKU_ID, "第{}条评论保存失败".format(self.num))
                conn.rollback()

    def save_star(self):
        # 更新总评分
        if not SKU_DETAIL_ID(self.SKU_ID, self.ECOMMERCE_CODE):
            return True
        self.SKU_DETAIL_ID = SKU_DETAIL_ID(self.SKU_ID, self.ECOMMERCE_CODE)
        update_score(self.score, self.SKU_ID, self.name, self.SKU_DETAIL_ID)


def main(url_list):
    start = time.time()
    if len(url_list) < 1 or isinstance(url_list, list) is False:
        log_info("Tmall,无url信息或传入参数格式不是列表")
        return True
    for url in url_list:
        today = TMALLNewReview(url)
        today.run()
    end = time.time()
    log_info("tmall_end,耗时%s秒" % (end - start))


# 定时运行
def tmall_run(urls, h, m):
    while True:
        now = datetime.now()
        if now.hour == h and now.minute == m:
            r = main(urls)
            if r:
                break
        time.sleep(60)


if __name__ == '__main__':
    from urls import tmall_urls
    urls = tmall_urls()
    # tmall_run(urls, 16, 20)
    main(urls)