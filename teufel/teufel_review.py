import locale
import re
from datetime import datetime
from time import sleep

from retrying import retry
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils import wait, save_score, save_review, review_split, close_db, c, conn, SKU_DETAIL_ID, max_date
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


class TeufulReview:

    def __init__(self):
        self.url = "https://www.teufel.de/?ac_type=warenkorb&ac_name=update&rf_set_country=1&vw_type=artikel&vw_name=detail&vw_id=16427&delivery_country=48#section_tests"
        self.num = 0
        user_ag = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent=%s' % user_ag)
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('blink-settings=imagesEnabled=false')
        self.dr = webdriver.Chrome(chrome_options=options)
        self.dr.set_page_load_timeout(60)
        self.dr.set_script_timeout(60)
        self.sku_id = ""
        self.name = "Teuful"
        self.ECOMMERCE_CODE = "8"
        self.SKU_DETAIL_ID = ""
        self.max_date = None

    @retry(stop_max_attempt_number=5)
    def parse_url(self):
        self.dr.maximize_window()
        self.dr.get(self.url)
        self.dr.execute_script('window.scrollBy(0,600)')

    def get_reviews(self):
        dr = self.dr
        # 总评分
        score = WebDriverWait(dr, wait).until(
            lambda driver: dr.find_element_by_xpath(
                "//div[@class='view_product_rating_summary__average_text']/span[1]")).text
        # print(score)
        # 保存评分
        locale.setlocale(locale.LC_ALL, 'C')
        # 以SKU_ID和ECOMMERCE_CODE联合查询ECOMMERCE_SKU_DETAIL表SKU_DETAIL_ID的值
        if not SKU_DETAIL_ID(self.sku_id, self.ECOMMERCE_CODE):
            return True
        self.SKU_DETAIL_ID = SKU_DETAIL_ID(self.sku_id, self.ECOMMERCE_CODE)
        # print(self.SKU_DETAIL_ID)
        # 保存总评分
        save_score(self.sku_id, score, self.name, self.SKU_DETAIL_ID, conn)

        # 提取评论
        self.get_review()
        # 点击下一页
        while True:
            try:
                lis = WebDriverWait(dr, wait).until(
                    lambda driver: dr.find_elements_by_xpath(
                        "//ul[@class='uk-pagination view_product_ratings__pagination']/li"))
                WebDriverWait(lis[-1], wait).until(EC.element_to_be_clickable((By.XPATH, "./a"))).click()
                sleep(5)
                self.get_review()
            except:
                break
        # print(self.num)

    def get_review(self):
        dr = self.dr
        divs = WebDriverWait(dr, wait).until(
            lambda driver: dr.find_elements_by_xpath(
                "//div[@class='view_product_ratings__container spinner_height']/div[@class='view_product_rating origin']"))
        for d in divs:
            # 评论星级
            star = d.get_attribute("data-stars")
            # 评论ID
            REVIEW_ID = self.SKU_DETAIL_ID + "_" + d.get_attribute("id")
            # 评论用户,时间
            author_time = WebDriverWait(d, wait).until(
                lambda driver: d.find_element_by_xpath(
                    ".//div[@class='uk-width-1-2 view_product_rating__name_and_date']")).text
            author = author_time.split(". /")[0]
            time = author_time.split(". /")[1].strip().replace(".", "/")
            REVIEW_DATE = datetime.strptime(time, "%d/%m/%Y").strftime('%Y/%m/%d')
            print(REVIEW_DATE)
            # 评论标题
            title = WebDriverWait(d, wait).until(
                lambda driver: d.find_element_by_xpath(".//cite")).text
            # print(title)
            # 评论内容
            # 点击更多显示全部评论
            try:
                d.find_element_by_xpath(".//div[@class='uk-width-1-1']/a").click()
                cont = WebDriverWait(d, wait).until(lambda driver: d.find_element_by_xpath(".//span[@class='uk-width-1-1']/q[@class='view_product_rating__text']")).text
            except:
                cont = WebDriverWait(d, wait).until(lambda driver: d.find_element_by_xpath(".//div[@class='uk-width-1-1']/div[@class='view_product_rating__text']")).text
            REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_TEXT5 = review_split(cont.replace("\n", "\t"))
            REVIEW_TEXT5 += "  from_Teufel"
            # 保存数据
            sql = save_review(REVIEW_ID, self.sku_id, star, author, title, REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_DATE, REVIEW_TEXT5, self.SKU_DETAIL_ID)
            try:
                c.execute(sql)
                conn.commit()
                self.num += 1
            except Exception as e:
                print(e, "{}({})保存失败".format(self.name, self.sku_id))
                conn.rollback()

    def run(self, url):
        # sku_id
        self.sku_id = re.search(r"(.*)/(.*).html", url).group(2)
        # 发送请求
        self.parse_url()
        sleep(60)
        # 提取评论数据
        if self.get_reviews():
            self.dr.close()
            print("今日更新{}条".format(self.num))
            return
        self.dr.close()


if __name__ == '__main__':
    url = "https://www.teufelaudio.nl/koptelefoons/Cage-p16427.html"
    tf = TeufulReview()
    tf.run(url)
    close_db()