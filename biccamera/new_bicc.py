# -*-coding:utf-8-*-
import os
import sys
from biccamera.bicc_review import BiccReview
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, ""))
import re
from datetime import datetime
from selenium import webdriver
import time
from retrying import retry
from utils import review_split, c, conn, close_db, logger, log_info, save_score, SKU_DETAIL_ID, save_review, max_date, update_score, newReview
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BiccNewReview(BiccReview):

    def get_score(self):
        self.SKU_DETAIL_ID = SKU_DETAIL_ID(self.SKU_ID, self.ECOMMERCE_CODE)
        if not self.SKU_DETAIL_ID:
            return True
        self.max_date = max_date(self.SKU_DETAIL_ID)
        try:
            self.score = WebDriverWait(self.driver, 10).until(
                lambda driver: self.driver.find_element_by_xpath("//div[@class='bcs_box1']/p[@class='bcs_star']/span")).text
            self.score = float(self.score)
            update_score(self.score, self.SKU_ID, self.name, self.SKU_DETAIL_ID)
        except:
            logger(self.name, self.SKU_ID, "总评分获取失败")


    def get_content_list(self):
        dr = self.driver
        try:
            tr_list = WebDriverWait(dr, 10).until(lambda driver: dr.find_elements_by_xpath("//div[@class='reviewBox']/div[@class='bcs_item']"))
            # print(len(tr_list))
        except Exception as e:
            logger(self.name, self.SKU_ID, "获取评论主标签失败")
            return True
        for tr in tr_list:
            try:
                REVIEW_NAME = WebDriverWait(tr, 10).until(
                    lambda driver: tr.find_element_by_xpath(".//p[@class='bcs_contributor']/span")).text.strip()
                REVIEW_TITLE = WebDriverWait(tr, 10).until(
                    lambda driver: tr.find_element_by_xpath("./div[@class='bcs_inner']/dl/dd")).text.strip()
                REVIEW_TEXT = WebDriverWait(tr, 10).until(
                    lambda driver: tr.find_element_by_xpath("./div[@class='bcs_inner']/p[1]")).text.strip()
                REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_TEXT5 = review_split(REVIEW_TEXT.replace("\n", "\t"))
                REVIEW_TEXT5 += "  from_Bicc"
                REVIEW_DATE = WebDriverWait(tr, 10).until(
                    lambda driver: tr.find_element_by_xpath("./div[@class='bcs_inner']/p[@class='bcs_date']")).text
                # 投稿日：2019/7/18
                REVIEW_DATE = REVIEW_DATE.split("：")[1].strip()
            except Exception as e:
                logger(self.name, self.SKU_ID)
                continue
            re_date = datetime.strptime(REVIEW_DATE, "%Y/%m/%d")
            if newReview(self.max_date, re_date):
                print("yodo,{}更新了{}条,".format(self.SKU_ID, self.num))
                log_info("yodo,{}更新了{}条,".format(self.SKU_ID, self.num))
                return True
            CREATE_TIME = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            REVIEW_ID = WebDriverWait(tr, 10).until(
                    lambda driver: tr.find_element_by_xpath("./div[@class='bcs_right']/div[1]")).get_attribute("class")
            REVIEW_ID = self.SKU_DETAIL_ID + "_" + REVIEW_ID
            REVIEW_SCORE = WebDriverWait(tr, 10).until(
                    lambda driver: tr.find_element_by_xpath("./div[@class='bcs_inner']/dl/dt/img")).get_attribute("src")  # /bc/resources4/common/img/star_l_5.png
            REVIEW_SCORE = float(re.search(r"star_l_(\d).png", REVIEW_SCORE).group(1))
            # print(REVIEW_NAME, REVIEW_Title, REVIEW_TEXT, REVIEW_DATE, REVIEW_ID, REVIEW_SCORE)
            sql_review = "INSERT INTO ECOMMERCE_REVIEW_P(REVIEW_ID, SKU_ID, REVIEW_STAR, REVIEW_NAME, REVIEW_TITLE, REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_DATE, CREATE_TIME, REVIEW_TEXT5, SKU_DETAIL_ID) VALUES('{}', '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', to_date('{}','yyyy/MM/dd'), to_date('{}','yyyy/MM/dd HH24:mi:ss'),'{}', '{}')".format(
                REVIEW_ID, self.SKU_ID, REVIEW_SCORE, REVIEW_NAME.replace("'", ""), REVIEW_TITLE.replace("'", ""),
                REVIEW_TEXT1.replace("'", ""),
                REVIEW_TEXT2.replace("'", ""), REVIEW_TEXT3.replace("'", ""), REVIEW_TEXT4.replace("'", ""),
                REVIEW_DATE, CREATE_TIME, REVIEW_TEXT5.replace("'", ""), self.SKU_DETAIL_ID)
            try:
                c.execute(sql_review)
                conn.commit()
                self.num += 1
            except Exception as e:
                conn.rollback()
                print(e, self.SKU_ID, self.num, "保存失败")


def main(urls):
    start = time.time()
    if len(urls) < 1 or isinstance(urls, list) is False:
        return True
    for url in urls:
        bicc = BiccNewReview()
        bicc.run(url)
    end = time.time()
    print("yodo_end,%s" % (end - start))
    log_info("yodo_end,%s" % (end - start))


if __name__ == '__main__':
    from urls import bicc_urls
    urls = bicc_urls()
    # urls = ["https://www.biccamera.com/bc/item/4668927/"]
    main(urls)