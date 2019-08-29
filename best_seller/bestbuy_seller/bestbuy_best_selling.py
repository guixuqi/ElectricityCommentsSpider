# -*-coding:utf-8-*-
import os
import re
from best_seller.libs import BestSelling


class BestBuyBestSelling(BestSelling):
    def __init__(self, url, customerNo):
        super(BestBuyBestSelling, self).__init__()
        self.url = url
        self.url_main = "https://www.bestbuy.com"
        self.ECOMMERCE_CODE = "100"  # 网站代码
        self.customerNo = customerNo

    def product_list(self, html):
        # 获取前10产品信息(SKU_ID,ECOMMERCE_CODE,INSIDE_TYPE,排名,链接,标题,图片)
        # 主标签
        lis = html.xpath("//ol[@class='sku-item-list']/li[@class='sku-item']")
        for li in lis[0:10]:
            # 链接
            href = self.url_main + li.xpath(".//a[@class='image-link']/@href")[0]
            SKU_ID = re.search(r"skuId=(\d+)", href).group(1)
            # 排名
            sort_by = "#%02d" % (lis.index(li) + 1)
            print(sort_by, href)
            # 标题 product-image
            title = li.xpath(".//h4[@class='sku-header']/a/text()")[0].replace("'", "")
            # 名称
            # name = title.split(" ")[0] + " " + title.split(" ")[1]
            # 图片
            img_url = li.xpath(".//a[@class='image-link']/img/@src")[0]
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

    def run(self):
        # self.clean_img()
        self.update_review()
        self.delete_sku_detail()
        self.clean_sku_master()
        html = self.parse_url()
        self.product_list(html)


if __name__ == '__main__':
    from best_seller.seller_urls import bestbuy_urls
    list_bestbuy = bestbuy_urls()
    for tuple2 in list_bestbuy:
        BestBuyBestSelling(*tuple2).run()