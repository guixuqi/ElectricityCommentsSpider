# # # # # # # # -*-coding:utf-8-*-
# # # # # # # import urllib.request
# # # # # # # import requests
# # # # # # # from selenium import webdriver
# # # # # # # from selenium.webdriver.support.ui import WebDriverWait
# # # # # # # from selenium.webdriver.support import expected_conditions as EC
# # # # # # # from selenium.webdriver.common.by import By
# # # # # # # from selenium.webdriver.common.action_chains import ActionChains
# # # # # # #
# # # # # # #
# # # # # # # # my_ip = urllib.request.urlopen('http://ip.42.pl/raw').read()
# # # # # # # # print('ip.42.pl', my_ip)
# # # # # # # # my_ip = urllib.request.urlopen('http://103.36.115.203:88/open?user_name=ly_74104617_2500&timestamp=1554706833&md5=94a19c9473b12e492966a2daa281c4c6&pattern=json&number=1&special=0&fmt=0').read()
# # # # # # # # print('ip.42.pl', my_ip)
# # # # # # #
# # # # # # # # options = webdriver.ChromeOptions()  # ���ùȸ��������һЩѡ��
# # # # # # # # # proxy ���� options ѡ��
# # # # # # # # options.add_argument(r'--proxy-server=http:\\103.36.115.203:11450')
# # # # # # # # driver = webdriver.Chrome(options=options)
# # # # # # # driver = webdriver.Chrome()
# # # # # # # # url = "https://www.baidu.com/"
# # # # # # # # url = 'https://detail.tmall.com/item.htm?id=574870586003'
# # # # # # # url = 'https://www.amazon.co.jp/Zero-Audio-TWZ-1000-%E5%AE%8C%E5%85%A8%E3%83%AF%E3%82%A4%E3%83%A4%E3%83%AC%E3%82%B9%E3%82%B9%E3%83%86%E3%83%AC%E3%82%AA%E3%83%98%E3%83%83%E3%83%89%E3%83%9B%E3%83%B3/product-reviews/B07N6NRS8Q/ref=sr_1_1?sortBy=recent'
# # # # # # # # url_ip = "http://ip.dobel.cn/current-ip"
# # # # # # # set_ip = "http://103.36.115.203:88/open?user_name=ly_74104617_2500&timestamp=1554706833&md5=94a19c9473b12e492966a2daa281c4c6&pattern=json&number=1&special=0&fmt=0"
# # # # # # #
# # # # # # # # driver.get(set_ip)
# # # # # # # driver.get(url)
# # # # # # #
# # # # # # #
# # # # # # # import cx_Oracle
# # # # # # # from datetime import datetime
# # # # # # #
# # # # # # # CREATE_TIME = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
# # # # # # # REVIEW_ID = "view_product_rating--226570"
# # # # # # # SKU_ID = "Cage-p16427"
# # # # # # # score = 4
# # # # # # # REVIEW_NAME = "Martin K"
# # # # # # # REVIEW_TITLE = "Tolles Headset mit kleinen Designschwächen"
# # # # # # # REVIEW_TEXT1 = "Zuerst das Positive: - toller Klang - hervorragende Verarbeitung - guter Tragekomfort Die einzigen Kritikpunkte für mich: - Das Mikrofon ist aufgrund der Platzierung des Ports und dem starren Kunststoff direkt am Stecker leider nicht vollständig aus dem Sichtfeld zu bekommen, was etwas gewöhnungsbedürftig ist. - Die bereits mehrfach geübte Kritik bezüglich des relativ starren stoffummantelte USB-Kabels ist leider nicht übertrieben - man hört leider jede Kopfbewegung. Habe es durch ein weicheres Kabel mit normaler Kunststoffummantelung ersetzt, was deutliche Besserung gebracht hat."
# # # # # # # REVIEW_TEXT2 = ""
# # # # # # # REVIEW_TEXT3 = ""
# # # # # # # REVIEW_TEXT4 = ""
# # # # # # # REVIEW_TEXT5 = ""
# # # # # # # REVIEW_DATE = datetime(2019, 7, 7)
# # # # # # # SKU_DETAIL_ID = "Cage-p16427"
# # # # # # # sql = "INSERT INTO ECOMMERCE_REVIEW_P(REVIEW_ID, SKU_ID, REVIEW_STAR, REVIEW_NAME, REVIEW_TITLE, REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_DATE, CREATE_TIME, REVIEW_TEXT5, SKU_DETAIL_ID) VALUES('{}', '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', to_date('{}','yyyy/MM/dd'), to_date('{}','yyyy/MM/dd HH24:mi:ss'), '{}', '{}')".format(
# # # # # # #     REVIEW_ID, SKU_ID, score, REVIEW_NAME.replace("'", ""),
# # # # # # #     REVIEW_TITLE.replace("'", ""), REVIEW_TEXT1.replace("'", ""),
# # # # # # #     REVIEW_TEXT2.replace("'", ""), REVIEW_TEXT3.replace("'", ""), REVIEW_TEXT4.replace("'", ""),
# # # # # # #     REVIEW_DATE, CREATE_TIME, REVIEW_TEXT5.replace("'", ""), SKU_DETAIL_ID)
# # # # # # #
# # # # # # # dsnStr = cx_Oracle.makedsn("192.168.110.205", 1521, "EIP")
# # # # # # # # dsnStr = cx_Oracle.makedsn("192.168.110.214", 1521, "HORNEIP")  # 测试库
# # # # # # # conn = cx_Oracle.connect("EIP", "EIP", dsnStr)
# # # # # # # c = conn.cursor()
# # # # # # # c.execute(sql)
# # # # # # # c.commit()
# # # # # #
# # # # # # import os
# # # # # # import re
# # # # # #
# # # # # # # logs = "C:\\Users\\hhh\\Desktop\\Demo\\reviews\\Logs\\All_Logs"
# # # # # # logs = "C:\\Users\\hhh\\Desktop\\Demo\\reviews\\Logs\\Error_Logs"
# # # # # # fs = os.listdir(logs)
# # # # # #
# # # # # # for f in fs:
# # # # # #     if re.search(r".log", f):
# # # # # #         ff = os.path.join(logs, f)
# # # # # #         # print(ff)
# # # # # #         os.remove(ff)
# # # # # #
# # # # #
# # # # # # s1 = "32"
# # # # # # s2 = "3"
# # # # # # s3 = "23"
# # # # # # import re
# # # # # # r1 = re.search(r"^3.*", s1).group()
# # # # # # r2 = re.search(r"^3.*", s2).group()
# # # # # # r3 = re.search(r"^3.*", s3)
# # # # # # print(r1, r2, r3)
# # # # # #
# # # # # # import requests
# # # # # # from lxml import etree
# # # # # #
# # # # # # url = "https://www.yodobashi.com/community/product/100000001003703441/review.html"
# # # # # # headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"}
# # # # # # resp = requests.get(url, headers=headers)
# # # # # # html = etree.HTML(resp.content.decode())
# # # # # # divs = html.xpath("//div[@class='comWallBlock']/div")
# # # # # # print(len(divs))
# # # # # # html.xpath("//a[@class='js_afterPost']")
# # # # # # divs0 = html.xpath("//div[@class='comWallBlock']/div")
# # # # # # print(len(divs0))
# # # # # import cx_Oracle
# # # # #
# # # # # dsnStr = cx_Oracle.makedsn("192.168.110.205", 1521, "EIP")
# # # # # # dsnStr = cx_Oracle.makedsn("192.168.110.214", 1521, "HORNEIP")  # 测试库
# # # # # conn = cx_Oracle.connect("EIP", "EIP", dsnStr)
# # # # # c = conn.cursor()
# # # # # sql = "select max(review_date) from ECOMMERCE_REVIEW_P where sku_id='{}'".format("000000245037")
# # # # # max_date = c.execute(sql).fetchone()[0]
# # # # # print(max_date)
# # # #
# # # #
# # # # # -*- coding: utf-8 -*-
# # # # import time
# # # # from time import sleep
# # # # import requests
# # # # from lxml import etree
# # # # import re
# # # # from retrying import retry
# # # # from utils import save_score, SKU_DETAIL_ID, review_split, save_review, c, conn, close_db, update_score
# # # #
# # # #
# # # # class KakakuReview:
# # # #
# # # #     def __init__(self):
# # # #         self.url = "https://review.kakaku.com/review/{}/#tab"
# # # #         self.headers = {
# # # #             'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"}
# # # #         self.sku_id = ""
# # # #         self.num = 0
# # # #         self.name = "kakaku"
# # # #         self.SKU_DETAIL_ID = ""
# # # #         self.ECOMMERCE_CODE = "33"
# # # #         self.max_date = None
# # # #
# # # #     def get_url(self, url):
# # # #         try:
# # # #             self.sku_id = re.search(r"item/(\w+)", url).group(1)
# # # #         except:
# # # #             print(url + "格式不对")
# # # #             return True
# # # #         self.url = self.url.format(self.sku_id)
# # # #
# # # #     @retry(stop_max_attempt_number=5)
# # # #     def parse_url(self):
# # # #         resp = requests.get(self.url, headers=self.headers, timeout=10)
# # # #         sleep(3)
# # # #         if resp.status_code != 200:
# # # #             raise Exception
# # # #         html = etree.HTML(resp.text)
# # # #         return html
# # # #
# # # #     def parse_score(self, html):
# # # #         self.SKU_DETAIL_ID = SKU_DETAIL_ID(self.sku_id, self.ECOMMERCE_CODE)
# # # #         if not self.SKU_DETAIL_ID:
# # # #             print(self.sku_id+"查询不到SKU_DETAIL_ID")
# # # #             return True
# # # #         # 总评分
# # # #         try:
# # # #             total_score = html.xpath("//div[@class='revstar']/span[@class='impact01']/text()")
# # # #             total_score = float(total_score[0])
# # # #         except Exception as e:
# # # #             print(self.sku_id+"获取总评分失败", e)
# # # #             total_score = 0
# # # #         print(total_score)
# # # #
# # # #     def parse_review(self, html):
# # # #         divs = html.xpath("//div[@class='reviewBox ver2013 boxGr']")
# # # #         print(len(divs))
# # # #         if len(divs) < 1:
# # # #             print(self.sku_id+"评论主标签获取失败")
# # # #             return True
# # # #         for div in divs:
# # # #             try:
# # # #                 # 评论ID preceding-sibling::a[1]
# # # #                 review_id = self.SKU_DETAIL_ID + "_" + div.xpath("./preceding-sibling::div[1]/@id")[0]
# # # #                 # 评论星级
# # # #                 score = div.xpath(".//div[@class='revRateBox type2']/table[@class='total']/tbody/tr/td/text()")[0]
# # # #                 # 评论人
# # # #                 name = div.xpath(".//span[@class='userName']/a/text()")
# # # #                 if not name:
# # # #                     name = div.xpath(".//span[@class='userName']/a//span[@itemprop='name']/text()")
# # # #                     date = div.xpath(".//p[@class='entryDate clearfix']/span/@content")[0].replace("-", "/")
# # # #                 else:
# # # #                     # 评论时间  2019年7月20日 10:23 [1243163-2]
# # # #                     date = div.xpath(".//p[@class='entryDate clearfix']/text()")[0].split(" ")[0]
# # # #                     dataStr = re.search(r"(\d+)\D+(\d+)\D+(\d+)", date)
# # # #                     date = dataStr.group(1) + "/" + dataStr.group(2) + "/" + dataStr.group(3)
# # # #                 name = name[0]
# # # #                 # 评论标题
# # # #                 title = div.xpath(".//div[@class='reviewTitle']/span/a/text()")[0]
# # # #                 # 评论内容
# # # #                 text = div.xpath(".//p[@class='revEntryCont']/text()")[0].replace("\n", "\t")
# # # #             except Exception as e:
# # # #                 print(self.sku_id+str(self.num)+"提取评论信息失败", e)
# # # #                 continue
# # # #             print(review_id, score, name, date, title, text)
# # # #
# # # #     def run(self, url):
# # # #         self.get_url(url)
# # # #         html = self.parse_url()
# # # #         if self.parse_score(html):
# # # #             return
# # # #         if self.parse_review(html):
# # # #             print("kakaku,{}共更新了{}条,".format(self.sku_id, self.num))
# # # #             # log_info("kakaku,{}更新了{}条,".format(self.SKU_ID, self.num))
# # # #             return
# # # #         print("ear,{}共抓取了{}条,".format(self.sku_id, self.num))
# # # #
# # # #
# # # # def run(urls):
# # # #     start = time.time()
# # # #     if len(urls) < 1 or isinstance(urls, list) is False:
# # # #         return True
# # # #     for url in urls:
# # # #         ka = KakakuReview()
# # # #         ka.run(url)
# # # #         # time.sleep(3)
# # # #     close_db()
# # # #     end = time.time()
# # # #     print("ear_end,%s" % (end - start))
# # # #     # log_info("ear_end,%s" % (end - start))
# # # #
# # # #
# # # # if __name__ == '__main__':
# # # #     us = ["https://kakaku.com/item/J0000030671/"]
# # # #     run(us)
# # #
# # #
# # # # str = "\x81"
# # # # print(str)
# # # # print('\u00bb')
# # #
# # # #
# # # # import io
# # # # import sys
# # # # import urllib.request
# # # # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')  # 改变标准输出的默认编码
# # # # # res=urllib.request.urlopen('http://www.baidu.com')
# # # # # htmlBytes=res.read()
# # # # # print(htmlBytes.decode('utf-8'))
# # # #
# # # # str = "個性的なイヤホン、なかなか良いです"
# # # # print(str)
# # # # print('\u00bb')
# # # #
# # #
# # # # n = []
# # # # while n:
# # # #     print(2)
# # # #     n -= 1
# # # #
# # # # h = open("C:\\Windows\\Help\\Windows\\help.txt", "r")
# # # # hh = h.readlines()
# # # # print(hh)
# # # # print(hh[0].strip())
# # # # print(hh[1].strip())
# # # # print(hh[2].strip())
# # #
# # # # import os
# # # # print(os.path.abspath(__file__))
# # #
# # # # lis = ['q','w','e',1,23,5,61,15,6,40,90]
# # # # for li in lis:
# # # #     sort_by = "#%02d" % (lis.index(li) + 1)
# # # #     print(sort_by)
# # #
# # #
# # # from multiprocessing import Pool
# # # import os, time, random
# # #
# # #
# # # def worker(msg):
# # #     t_start = time.time()
# # #     print("%s开始执行,进程号为%d" % (msg, os.getpid()))
# # #     # random.random()随机生成0~1之间的浮点数
# # #     time.sleep(random.random() * 2)
# # #     t_stop = time.time()
# # #     print(msg, "执行完毕，耗时%0.2f" % (t_stop - t_start))
# # #
# # #
# # # po = Pool(3)  # 定义一个进程池，最大进程数3
# # # n = 0
# # # for i in range(0, 10):
# # #     # Pool().apply_async(要调用的目标,(传递给目标的参数元祖,))
# # #     # 每次循环将会用空闲出来的子进程去调用目标
# # #     po.apply_async(worker, (i,))
# # #     n += 1
# # #
# # # # print("----start----")
# # # # po.close()  # 关闭进程池，关闭后po不再接收新的请求
# # # # po.join()  # 等待po进程池中所有子进程执行完成，必须放在close语句之后
# # # # print("-----end-----")
# # # # while True:
# # # #     if n >= 10:
# # # #         break
# #
# # # def r(a,b):
# # #     print(a + b)
# # #
# # # r(*(1,2))
# # import threading
# # import time
# # import queue
# # from datetime import datetime
# #
# #
# # def foo(a):
# #     time.sleep(5)
# #     print(a+1)
# #
# # start = time.time()
# # # l = []
# # q = queue.Queue()
# # for i in range(5):
# #     t = threading.Thread(target=foo, args=(i,))
# #     # l.append(t)
# #     q.put(t)
# #
# # # for t in l:
# # while not q.empty():
# #     t = q.get()
# #     # print(q.qsize())
# #     q.task_done()
# #     t.start()
# # q.join()
# # # for i in range(5):
# # #     foo(i)
# # end = time.time()
# # print("共耗时:", end-start)
# #
# # d = 1
# # def foo():
# #     d =2
# #     print(d)
# #
# # foo()
# import queue
# import threading
# from time import sleep
#
# q = queue.Queue()
#
# def foo(n):
#     sleep(5)
#     print(n)
#     q.task_done()
#
# for i in range(10):
#     t = threading.Thread(target=foo, args=(i,))
#     q.put(t)
#
# while not q.empty():
#     t = q.get()
#     # t.daemon = True
#     t.start()
#     # t.join()
# q.join()
# print("END!")
#
# import threading
# import time
#
# sem = threading.Semaphore(8)  # 限制线程的最大数量为4个
#
#
# def gothread(n):
#     with sem:  # 锁定线程的最大数量
#         time.sleep(2)
#         print(n)
#         # for i in range(8):
#         #     print(threading.current_thread().name, i)
#         #     time.sleep(1)
#
#
# for i in range(20):
#     threading.Thread(target=gothread, args=(i,)).start()
#
from time import sleep
import pyautogui

pyautogui.click(1325, 669, clicks=2, button='left')
sleep(1)
pyautogui.click(1325, 669, clicks=2, button='left')