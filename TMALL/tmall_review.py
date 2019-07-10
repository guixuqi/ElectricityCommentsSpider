import os
import sys

from IP_proxy.ip_proxy import proxy_auth_plugin_path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, ""))
import re
from datetime import datetime
from selenium import webdriver
import time
from retrying import retry
# from TMALL.selenium_status import getHttpStatus
from utils import review_split, c, conn, close_db, logger, log_info, save_score, SKU_DETAIL_ID, save_review, max_date
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from xpinyin import Pinyin


class TMALLReview:

    def __init__(self, url):
        self.name = "tmall"
        self.start_url = url
        self.driver = webdriver.Chrome()
        # 使用多贝云IP代理
        # options = webdriver.ChromeOptions()
        # options.add_extension(proxy_auth_plugin_path)
        # self.driver = webdriver.Chrome(chrome_options=options)
        # 评论序号
        self.num = 0
        # 从url中提取SKU_ID
        self.SKU_ID = re.search(r"id=(\d+)", url).group(1)
        # 总评分
        self.score = ""
        self.ECOMMERCE_CODE = "6"
        self.SKU_DETAIL_ID = ""
        # 查询数据库评论最晚日期
        self.max_date = max_date(self.SKU_ID)

    @retry(stop_max_attempt_number=5)
    def parse_url(self):  # 发送请求,点击进入评论页面
        # 页面最大化
        self.driver.maximize_window()
        # self.driver.get("http://ip.dobel.cn/switch-ip")
        # 发送请求，获取响应
        self.driver.get(self.start_url)


    def enter_review(self):
        # 发送请求
        self.parse_url()
        time.sleep(3)
        # 关闭弹窗
        self.close_alter()
        time.sleep(5)
        # 点击累计评论
        self.click_review()
        # 等待二维码消失
        time.sleep(15)
        # 点击按时间排序
        self.order_time()
        time.sleep(5)
        # 总评分
        try:
            self.score = WebDriverWait(self.driver, 20).until(
                lambda driver: self.driver.find_element_by_xpath("//div[@class='rate-score']/strong")).text
            self.score = float(self.score)
        except:
            self.score = 0
            logger(self.name, self.SKU_ID, "无总评分数据")

        self.save_star()

    def close_alter(self):
        try:
            # 关闭登录弹框
            close_login = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'sufei-dialog-close')))
            self.driver.execute_script("arguments[0].click()", close_login)
        except:
            # 未出现登录弹框
            pass

    def click_review(self):
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='J_TabBarBox']//a[text()='累计评价 ']"))).click()

    def order_time(self):
        # 鼠标悬停按默认
        # self.driver.execute_script("window.scrollBy(0, 500)")
        # time.sleep(1)
        elements = WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_element_by_xpath("//span[@class='tm-current']"))
        actions = ActionChains(self.driver)
        actions.move_to_element(elements).perform()
        # time.sleep(1)
        # 点击按时间排序
        element_artist = WebDriverWait(self.driver, 20).until(
            lambda driver: self.driver.find_elements_by_tag_name('a"'))
        element_artist[1].click()

    def get_content_list(self):  # 提取数据
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
        for tr in tr_list:
            try:
                REVIEW_NAME = WebDriverWait(tr, 20).until(
                    lambda driver: tr.find_element_by_xpath(".//div[@class='rate-user-info']")).text
                REVIEW_TEXT = WebDriverWait(tr, 20).until(
                    lambda driver: tr.find_element_by_xpath(
                        ".//td[@class='tm-col-master']//div[@class='tm-rate-fulltxt']")).text
                REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_TEXT5 = review_split(REVIEW_TEXT)
                REVIEW_TEXT5 += "  from_TMALL"
                REVIEW_DATE = WebDriverWait(tr, 20).until(
                    lambda driver: tr.find_element_by_xpath(
                        ".//td[@class='tm-col-master']//div[@class='tm-rate-date']")).text
            except Exception as e:
                logger(self.name, self.SKU_ID, "第{}条提取内容失败".format(self.num))
                continue
            # 时间格式转换
            list = REVIEW_DATE.split(".")
            now = datetime.now()
            now_str = now.strftime("%Y/%m/%d")
            now_year = now_str[0:4]
            if len(list) == 2:
                list.insert(0, now_year)
                REVIEW_DATE = "/".join(list)
            elif REVIEW_DATE == '今天':
                REVIEW_DATE = now_str
            else:
                REVIEW_DATE = REVIEW_DATE.replace(".", "/")
            CREATE_TIME = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
            # 评论ID
            # REVIEW_ID = self.SKU_ID + "_" + str(self.num)
            REVIEW_ID = REVIEW_DATE.replace("/", "") + str(len(REVIEW_TEXT)) + Pinyin().get_pinyin(REVIEW_NAME).replace("-", "")
            # print(REVIEW_ID)
            # 保存ECOMMERCE_REVIEW_P数据库
            sql_review = "INSERT INTO ECOMMERCE_REVIEW_P(REVIEW_ID, SKU_ID, REVIEW_NAME, REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_DATE, CREATE_TIME, REVIEW_TEXT5, SKU_DETAIL_ID) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}', to_date('{}','yyyy/MM/dd'), to_date('{}','yyyy/MM/dd HH24:mi:ss'),'{}', '{}')".format(
                REVIEW_ID, self.SKU_ID, REVIEW_NAME.replace("'", ""),
                REVIEW_TEXT1.replace("'", ""),
                REVIEW_TEXT2.replace("'", ""), REVIEW_TEXT3.replace("'", ""), REVIEW_TEXT4.replace("'", ""),
                REVIEW_DATE, CREATE_TIME, REVIEW_TEXT5.replace("'", ""), self.SKU_DETAIL_ID)
            try:
                c.execute(sql_review)
                conn.commit()
                self.num += 1
            except Exception as e:
                logger(self.name, self.SKU_ID, "第{}条评论保存失败".format(self.num))
                conn.rollback()

    def save(self, sql):
        try:
            c.execute(sql)
            conn.commit()
        except Exception as e:
            logger(self.name, self.SKU_ID, "评论总评分保存失败")
            conn.rollback()

    def save_star(self):
        # 以SKU_ID和ECOMMERCE_CODE联合查询ECOMMERCE_SKU_DETAIL表SKU_DETAIL_ID的值
        if not SKU_DETAIL_ID(self.SKU_ID, self.ECOMMERCE_CODE):
            return True
        self.SKU_DETAIL_ID = SKU_DETAIL_ID(self.SKU_ID, self.ECOMMERCE_CODE)
        # 保存总评分
        save_score(self.SKU_ID, self.score, self.name, self.SKU_DETAIL_ID)

    def next_click(self):
        dr = self.driver
        try:
            next_url = WebDriverWait(dr, 20).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "下一页>>")))
            dr.execute_script("arguments[0].focus();", next_url)
            next_url.click()
            time.sleep(2)
        except:
            next_url = None
        return next_url

    def run(self):  # 实现主要逻辑
        # self.proxy()
        # resp = self.parse_url()
        # if resp == {}:
        #     print("e")
        #     return
        try:
            self.enter_review()  # 发送请求,进入评论页面
        except Exception as e:
            logger(self.name, self.SKU_ID, "发送请求,进入评论页面失败")
            self.driver.close()
            return
        # 提取保存数据
        if self.get_content_list():
            log_info("Tmall,{}共更新了{}条,".format(self.SKU_ID, self.num))
            print("Tmall,{}共更新了{}条,".format(self.SKU_ID, self.num))
            self.driver.close()
            return
        # 点击下一页
        next_url = self.next_click()
        i = 0
        while next_url:
            i += 1
            # 因为Tmall限制,只抓取前7页评论
            if self.get_content_list() or i == 7:
                break
            next_url = self.next_click()
                # self.proxy()
                # ip = self.get_ip()
                # self.driver = self.request(ip)
                # time.sleep(20)
            if i % 10 == 0:
                time.sleep(5)
            # if i == 16:
            #     break
        log_info("Tmall,{}共更新了{}条,".format(self.SKU_ID, self.num))
        # 关闭浏览器
        self.driver.close()


def run(urls):
    start = time.time()
    if len(urls) < 1 or isinstance(urls, list) is False:
        log_info("Tmall,无url信息或传入参数格式不是列表")
        return True
    for url in urls:
        tmall = TMALLReview(url)
        tmall.run()
        time.sleep(10)
    # 关闭数据库
    close_db()
    end = time.time()
    log_info("tmall_end,耗时%s秒" % (end - start))
    print("tmall_end,耗时%s秒" % (end - start))


if __name__ == '__main__':
    from urls import tmall_urls
    urls = tmall_urls()
    run(urls)