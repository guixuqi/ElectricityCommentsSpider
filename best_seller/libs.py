# -*-coding:utf-8-*-
import cx_Oracle
import json
import os
import re
import requests
from lxml import etree
from retrying import retry


# 数据库配置
dsnStr = cx_Oracle.makedsn("192.168.110.205", 1521, "EIP")
# dsnStr = cx_Oracle.makedsn("192.168.110.214", 1521, "HORNEIP")  # 测试库
conn = cx_Oracle.connect("EIP", "EIP", dsnStr)
c = conn.cursor()


class BestSelling:
    def __init__(self):
        self.url = ""
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'}
        self.url_main = ""
        self.ECOMMERCE_CODE = ""  # 网站代码
        self.INSIDE_TYPE = "3"  # 热销产品
        self.skuStatus = "0"   # 开启爬虫
        self.customerNo = ""

    @retry(stop_max_attempt_number=5)
    def parse_url(self):
        resp = requests.get(self.url, headers=self.headers, timeout=30)
        try:
            html = etree.HTML(resp.content.decode())
        except:
            html = etree.HTML(resp.content.decode("gbk"))
        return html

    @retry(stop_max_attempt_number=5)
    def parse_img_url(self, url):
        resp = requests.get(url, headers=self.headers, timeout=30)
        return resp.content

    def eip_add(self, data, path_img):
        # eip新增产品配置
        add_url = "http://192.168.110.205:8087/ReportCenter/NewReport/Interface/ECommerce.asmx/EditSkuMasterData"
        resp = requests.post(add_url, headers=self.headers, json=data).text
        resp = json.loads(resp)
        # 新增图片配置
        save_img = "http://192.168.110.205:8087/ReportCenter/NewReport/Interface/ECommerceUpload.ashx"
        files = {'input-b9[]': open(path_img, 'rb')}
        resp1 = requests.post(save_img, headers=self.headers, files=files).text
        # print(resp1)
        resp1 = json.loads(resp1)
        # 上传服务器图片
        data["type"] = "edit"
        prodID = resp["d"].split("#")[0]
        # print(prodID)
        data["prodID"] = prodID
        data["fileName"] = resp1["fileName"]
        data["GUID"] = resp1["GUID"]
        # print(data)
        resp2 = requests.post(add_url, headers=self.headers, json=data)
        # print(resp2.status_code)
        return prodID

    def product_add(self, SKU_ID, prodID, href):
        # 新增产品明细
        data = {'type': 'new', 'skuID': '', 'skuCode': SKU_ID, 'ecommerceCode': self.ECOMMERCE_CODE, 'prodID': prodID, 'skuStatus': self.skuStatus, 'skuUrl': href, 'field': '', 'newValue': '', 'oldValue': ''}
        pro_url = "http://192.168.110.205:8087/ReportCenter/NewReport/Interface/ECommerce.asmx/EditSkuDetailData"
        resp = requests.post(pro_url, headers=self.headers, json=data).text
        resp = json.loads(resp)
        sku_detail_id = ("SKU" + resp["d"].split("SKU")[1]).split(SKU_ID)[0]
        # print(sku_detail_id)

    def delete_sku_detail(self):
        select_sql = "select PROD_ID from ECOMMERCE_SKU_MASTER where CUSTOMER_NO='{}'".format(self.customerNo)
        results = c.execute(select_sql).fetchall()
        for prodID in results:
            del_sql = "delete from ECOMMERCE_SKU_DETAIL where PROD_ID='{}'".format(prodID[0])
            c.execute(del_sql)
            conn.commit()

    def clean_sku_master(self):
        sql = "delete from ECOMMERCE_SKU_MASTER where CUSTOMER_NO='{}'".format(self.customerNo)
        c.execute(sql)
        conn.commit()

    def update_review(self):
        # 删除客户代码AMAZON的所有评论,评分
        customer_sql = "select PROD_ID from ECOMMERCE_SKU_MASTER where CUSTOMER_NO='{}'".format(self.customerNo)
        results = c.execute(customer_sql).fetchall()
        for prodID in results:
            prodID_sql = "select SKU_ID from ECOMMERCE_SKU_DETAIL where PROD_ID='{}'".format(prodID[0])
            sku = c.execute(prodID_sql).fetchone()[0]
            sku_sql = "delete from ECOMMERCE_REVIEW_P where SKU_DETAIL_ID='{}'".format(sku)
            c.execute(sku_sql)
            conn.commit()
            score_sql = "delete from ECOMMERCE_SKU_STAR_S where SKU_DETAIL_ID='{}'".format(sku)
            c.execute(score_sql)
            conn.commit()

    def clean_img(self):
        rootdir = "C:/Users/hhh/Desktop/Demo/reviews/best_seller/bestbuy_seller/img"
        filelist = os.listdir(rootdir)  # 列出该目录下的所有文件名
        for f in filelist:
            if re.search(".*.jpg", f):
                filepath = os.path.join(rootdir, f)
                os.remove(filepath)

