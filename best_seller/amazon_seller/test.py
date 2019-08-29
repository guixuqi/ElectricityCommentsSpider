# -*-coding:utf-8-*-
import os
import re
from best_seller.libs import BestSelling


class AmazonBestSelling(BestSelling):
    # def __init__(self, url, customerNo):
    #     super(AmazonBestSelling, self).__init__()
    #     self.url = url
    #     self.url_main = "https://www.amazon.de"
    #     self.ECOMMERCE_CODE = "1"  # 网站代码
    #     self.customerNo = customerNo

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
        for li in lis[0:10]:
            # 判断商品是否可售
            # is_sale = li.xpath(".//span[@class='a-size-large aok-inline-block zg-item-unavailable zg-text-center-align']/text()")
            # try:
            #     # print(is_sale[0])
            #     if is_sale[0] == "This item is no longer available":
            #         continue
            # except:
            #     pass
            # 链接
            href = self.url_main + li.xpath(".//span[@class='aok-inline-block zg-item']/a[@class='a-link-normal']/@href")[0]
            print(lis.index(li), href)
            SKU_ID = re.search(r".*/dp/(\w+)", href).group(1)
            # 排名
            # sort_by = li.xpath(".//span[@class='zg-badge-text']/text()")[0]
            sort_by = "#%02d" % (lis.index(li) + 1)
            # 标题
            title = li.xpath(".//div[@class='a-section a-spacing-small']/img/@alt")[0].replace("'", "")
            # 名称
            name = title.split(" ")[0] + " " + title.split(" ")[1]
            # print(sort_by, title)
            # 图片
            img_url = li.xpath(".//div[@class='a-section a-spacing-small']/img/@src")[0]
            # 保存图片

    def run(self, url, customerNo):
        self.dispose_param(url, customerNo)
        html = self.parse_url()
        self.product_list(html)


if __name__ == '__main__':
    # list_amazon = [("https://www.amazon.co.jp/gp/bestsellers/electronics/171351011/ref=zg_bs_nav_e_2_16462081", "AMAZON_DE0")]
    from best_seller.seller_urls import amazon_urls
    list_amazon = amazon_urls()
    for param in list_amazon:
        AmazonBestSelling().run(*param)
