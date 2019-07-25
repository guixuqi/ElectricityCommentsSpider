# -*-coding:utf-8-*-
import os
import sys
from yodobashi.yodo_review import YodoReview
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


class YodoNewReview(YodoReview):

    def get_score(self):
        self.SKU_DETAIL_ID = SKU_DETAIL_ID(self.SKU_ID, self.ECOMMERCE_CODE)
        if not self.SKU_DETAIL_ID:
            return True
        self.max_date = max_date(self.SKU_DETAIL_ID)
        try:
            self.score = WebDriverWait(self.driver, 10).until(
                lambda driver: self.driver.find_element_by_xpath("//strong[@class='fs16 red alignM ml10']")).text
            self.score = float(self.score)
        except:
            self.score = 0
            logger(self.name, self.SKU_ID, "无总评分信息")
        print(self.score)
        update_score(self.score, self.SKU_ID, self.name, self.SKU_DETAIL_ID)

    def get_content_list(self):
        dr = self.driver
        try:
            tr_list = WebDriverWait(dr, 10).until(
                lambda driver: dr.find_elements_by_xpath("//div[@class='comWallBlock']/div"))
        except Exception as e:
            logger(self.name, self.SKU_ID)
            return True
        for tr in tr_list:
            try:
                REVIEW_NAME = WebDriverWait(tr, 10).until(
                    lambda driver: tr.find_element_by_xpath("./div/table/tbody/tr/td[2]/div[1]/ul/li[1]/div/ul/li/div/a/strong")).text
                # //*[@id="js_feeds"]/div[2]/div/table/tbody/tr/td[2]/div[1]/ul/li[1]/div/ul/li/div/a/strong
                REVIEW_TEXT = WebDriverWait(tr, 10).until(
                    lambda driver: tr.find_element_by_xpath(
                        "./div/table/tbody/tr/td[2]/div[@class='cntrbtTxt']")).text
                REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_TEXT5 = review_split(REVIEW_TEXT.replace("\n", "\t"))
                REVIEW_TEXT5 += "  from_Yodo"
                REVIEW_DATE = WebDriverWait(tr, 10).until(
                    lambda driver: tr.find_element_by_xpath(
                        "./div/table/tbody/tr/td[2]/div[@class='liMt10']//div[@class='fs11 gray']")).text
            except Exception as e:
                logger(self.name, self.SKU_ID)
                continue
            dataStr = re.search(r"(\d+)\D+(\d+)\D+(\d+)", REVIEW_DATE)
            REVIEW_DATE = dataStr.group(1) + "/" + dataStr.group(2) + "/" + dataStr.group(3)
            re_date = datetime.strptime(REVIEW_DATE, "%Y/%m/%d")
            if newReview(self.max_date, re_date):
                return True
            CREATE_TIME = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            REVIEW_ID = tr.get_attribute("data-comm-contentid")
            REVIEW_ID = self.SKU_DETAIL_ID + "_" + REVIEW_ID
            REVIEW_SCORE = WebDriverWait(tr, 10).until(lambda driver: tr.find_element_by_xpath(".//div[@class='valueAvg']/span")).get_attribute("class")
            REVIEW_SCORE = float(re.search(r"iconStarM rate(\d)_0", REVIEW_SCORE).group(1))
            # print(REVIEW_NAME, REVIEW_DATE, REVIEW_ID, REVIEW_SCORE)
            sql_review = "INSERT INTO ECOMMERCE_REVIEW_P(REVIEW_ID, SKU_ID, REVIEW_STAR, REVIEW_NAME, REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_DATE, CREATE_TIME, REVIEW_TEXT5, SKU_DETAIL_ID) VALUES('{}', '{}', {}, '{}', '{}', '{}', '{}', '{}', to_date('{}','yyyy/MM/dd'), to_date('{}','yyyy/MM/dd HH24:mi:ss'),'{}', '{}')".format(
                REVIEW_ID, self.SKU_ID, REVIEW_SCORE, REVIEW_NAME.replace("'", ""),
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
        yodo = YodoNewReview()
        yodo.run(url)
        # time.sleep(3)
    end = time.time()
    print("yodo_end,%s" % (end - start))
    log_info("yodo_end,%s" % (end - start))


if __name__ == '__main__':
    from urls import yodo_urls
    urls = yodo_urls()
    # urls = ["https://www.yodobashi.com/product/100000001000978961/"]
    main(urls)