# -*-coding:utf-8-*-
import os
import re
from time import sleep
from best_seller.libs import BestSelling


class AmazonBestSelling(BestSelling):

    def dispose_param(self, start_url, customerNo):
        self.url = start_url
        self.customerNo = customerNo
        if re.search(r"www.amazon.com", start_url):
            self.url_main = "https://www.amazon.com"
            self.ECOMMERCE_CODE = "1"
        elif re.search(r"www.amazon.co.uk", start_url):
            self.url_main = "https://www.amazon.co.uk"
            self.ECOMMERCE_CODE = "2"
        elif re.search(r"www.amazon.co.jp", start_url):
            self.url_main = "https://www.amazon.co.jp"
            self.ECOMMERCE_CODE = "3"
        elif re.search(r"www.amazon.de", start_url):
            self.url_main = "https://www.amazon.de"
            self.ECOMMERCE_CODE = "4"
        elif re.search(r"www.amazon.fr", start_url):
            self.url_main = "https://www.amazon.fr"
            self.ECOMMERCE_CODE = "5"
        else:
            print("暂不支持爬取此类网站数据")

    def product_list(self, html):
        # 获取前10产品信息(SKU_ID,ECOMMERCE_CODE,INSIDE_TYPE,排名,链接,标题,图片)
        # 主标签
        lis = html.xpath("//ol[@id='zg-ordered-list']/li")
        if lis:
            for li in lis[0:10]:
                # 判断商品是否可售
                try:
                    is_sale = li.xpath(".//span[@class='a-size-large aok-inline-block zg-item-unavailable zg-text-center-align']/text()")[0]
                    if is_sale:
                        continue
                except:
                    pass
                # try:
                #     print(is_sale[0])
                #     if is_sale[0] == "This item is no longer available":
                #         continue
                # except:
                #     pass
                # 链接
                href = self.url_main + li.xpath(".//span[@class='aok-inline-block zg-item']/a[@class='a-link-normal']/@href")[0]
                SKU_ID = re.search(r".*/dp/(\w+)", href).group(1)
                # 排名
                # sort_by = li.xpath(".//span[@class='zg-badge-text']/text()")[0]
                sort_by = "#%02d" % (lis.index(li) + 1)
                print(sort_by, href)
                # 标题
                title = li.xpath(".//div[@class='a-section a-spacing-small']/img/@alt")[0].replace("'", "")
                # title = title.replace("【", "").replace("】", "")
                # 名称
                # name = title.split(" ")[0] + " " + title.split(" ")[1] + " " + title.split(" ")[2] + " " + title.split(" ")[3]
                # 图片
                img_url = li.xpath(".//div[@class='a-section a-spacing-small']/img/@src")[0]
                # 保存图片
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                path_img = "img/{}.jpg".format(SKU_ID)
                path_img = os.path.join(BASE_DIR, path_img)
                html_img = self.parse_img_url(img_url)
                with open(path_img, 'wb') as file:
                    file.write(html_img)
                # print(href, SKU_ID, sort_by, title)
                data = {'type':'new','prodID':'','customerNo':self.customerNo,'customerType':self.INSIDE_TYPE,'prodCode':sort_by,'prodName':title,'prodDesc':title,'prodStatus':self.skuStatus,'fileName':'','GUID':''}
                prodID = self.eip_add(data, path_img)
                self.product_add(SKU_ID, prodID, href)
        else:
            divs = html.xpath("//div[@class='s-result-list s-search-results sg-row']/div")
            num = 0
            for div in divs[0:10]:
                SKU_ID = div.xpath("./@data-asin")[0]
                if not SKU_ID:
                    continue
                # 链接
                href = self.url_main + div.xpath(".//div[@class='a-section a-spacing-none']/span[@class='rush-component']//a[@class='a-link-normal']/@href")[0]
                # SKU_ID = re.search(r".*/dp/(\w+)", href).group(1)
                # 标题
                title = div.xpath(".//span[@class='a-size-medium a-color-base a-text-normal']/text()")[0].replace("'", "")
                # 图片
                img_url = div.xpath(".//div[@class='a-section aok-relative s-image-fixed-height']/img/@src")[0]
                # 排名
                num += 1
                sort_by = "#%02d" % (num)
                print(sort_by, SKU_ID)
                # 保存图片
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                path_img = "img/{}.jpg".format(SKU_ID)
                path_img = os.path.join(BASE_DIR, path_img)
                html_img = self.parse_img_url(img_url)
                with open(path_img, 'wb') as file:
                    file.write(html_img)
                data = {'type': 'new', 'prodID': '', 'customerNo': self.customerNo, 'customerType': self.INSIDE_TYPE,
                        'prodCode': sort_by, 'prodName': title, 'prodDesc': title, 'prodStatus': self.skuStatus,
                        'fileName': '', 'GUID': ''}
                prodID = self.eip_add(data, path_img)
                self.product_add(SKU_ID, prodID, href)

    def run(self, url, customerNo):
        self.dispose_param(url, customerNo)
        # self.clean_img()
        self.update_review()
        self.delete_sku_detail()
        self.clean_sku_master()
        sleep(2)
        html = self.parse_url()
        self.product_list(html)


if __name__ == '__main__':
    from best_seller.seller_urls import amazon_urls
    list_amazon = amazon_urls()
    for tuple1 in list_amazon:
        AmazonBestSelling().run(*tuple1)
