import locale
from datetime import datetime
from time import sleep
from teufel.teufel_review import TeufulReview
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from utils import wait, update_score, newReview, review_split, save_review, close_db, SKU_DETAIL_ID, c, conn, max_date


class TeufulNewReview(TeufulReview):

    def get_reviews(self):
        dr = self.dr
        header = WebDriverWait(dr, wait).until(
            lambda driver: dr.find_element_by_xpath(
                "//header[@class='view_product__block_headline']"))
        dr.execute_script("arguments[0].focus();", header)
        score = WebDriverWait(dr, wait).until(lambda driver: dr.find_element_by_xpath("//div[@class='view_product_rating_summary__average_text']/span[1]")).text
        score = float(score)
        # print(score)
        locale.setlocale(locale.LC_ALL, 'C')
        # 更新总评分
        if not SKU_DETAIL_ID(self.sku_id, self.ECOMMERCE_CODE):
            return True
        self.SKU_DETAIL_ID = SKU_DETAIL_ID(self.sku_id, self.ECOMMERCE_CODE)
        self.max_date = max_date(self.SKU_DETAIL_ID)
        update_score(score, self.sku_id, self.name, self.SKU_DETAIL_ID, conn)

        if self.get_review():
            return True
        while True:
            try:
                lis = WebDriverWait(dr, wait).until(
                    lambda driver: dr.find_elements_by_xpath(
                        "//ul[@class='uk-pagination view_product_ratings__pagination']/li"))
                WebDriverWait(lis[-1], wait).until(EC.element_to_be_clickable((By.XPATH, "./a"))).click()
                sleep(5)
                if self.get_review():
                    return True
            except:
                break
        print("teufel更新了{}条".format(self.num))

    def get_review(self):
        dr = self.dr
        divs = WebDriverWait(dr, wait).until(
            lambda driver: dr.find_elements_by_xpath(
                "//div[@class='view_product_ratings__container spinner_height']/div[@class='view_product_rating origin']"))
        n = 0
        for d in divs:
            author_time = WebDriverWait(d, wait).until(lambda driver: d.find_element_by_xpath(".//div[@class='uk-width-1-1 uk-width-medium-1-2 uk-width-large-1-2 uk-width-small-1-1 view_product_rating__name_and_date']")).text
            author = author_time.split(". /")[0]
            time = author_time.split(". /")[1].strip().replace(".", "/")
            date = datetime.strptime(time, "%d/%m/%Y")
            if newReview(self.max_date, date):
                n += 1
                if n < 3:
                    continue
                else:
                    return True
            REVIEW_DATE = date.strftime('%Y/%m/%d')
            print(REVIEW_DATE)
            star = d.get_attribute("data-stars")
            REVIEW_ID = self.SKU_DETAIL_ID + "_" + d.get_attribute("id")
            title = WebDriverWait(d, wait).until(
                lambda driver: d.find_element_by_xpath(".//cite")).text
            # print(title)
            try:
                d.find_element_by_xpath(".//div[@class='uk-width-1-1']/a").click()
                cont = WebDriverWait(d, wait).until(lambda driver: d.find_element_by_xpath(".//span[@class='uk-width-1-1']/q[@class='view_product_rating__text']")).text
            except:
                cont = WebDriverWait(d, wait).until(lambda driver: d.find_element_by_xpath(".//div[@class='uk-width-1-1']/div[@class='view_product_rating__text']")).text
            REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_TEXT5 = review_split(cont)
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


if __name__ == '__main__':
    url = "https://www.teufelaudio.nl/koptelefoons/Cage-p16427.html"
    tf = TeufulNewReview()
    tf.run(url)
    close_db()