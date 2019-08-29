# -*-coding:utf-8-*-
import os
import re
from best_seller.libs import BestSelling


class JDBestSelling(BestSelling):
    def __init__(self, url, customerNo):
        super(JDBestSelling, self).__init__()
        self.url = url
        self.url_main = "https:"
        self.ECOMMERCE_CODE = "7"  # 网站代码
        self.customerNo = customerNo

    def product_list(self, html):
        # 获取前10产品信息(SKU_ID,ECOMMERCE_CODE,INSIDE_TYPE,排名,链接,标题,图片)
        # 主标签
        lis = html.xpath("//ul[@class='gl-warp clearfix']/li[@class='gl-item']")
        # print(len(lis))
        for li in lis[0:10]:
            # 链接
            href = self.url_main + li.xpath(".//div[@class='p-img']/a/@href")[0]
            # SKU_ID
            SKU_ID = re.search(r"(\d+).html", href).group(1)
            # 排名
            sort_by = "#%02d" % (lis.index(li) + 1)
            print(sort_by, href)
            # 标题
            try:
                title = li.xpath(".//div[@class='p-name']/a/em/text()")[0].replace("'", "").strip()
            except:
                title = li.xpath(".//div[@class='p-name p-name-type-2']/a/em/text()")[0].replace("'", "").replace("\n", "").strip()
            # 名称
            # name = title.split(" ")[0] + " " + title.split(" ")[1]
            # 图片
            try:
                img_url = self.url_main + li.xpath(".//div[@class='p-img']/a/img/@src")[0]
            except:
                img_url = self.url_main + li.xpath(".//div[@class='p-img']/a/img/@source-data-lazy-img")[0]
            # 保存图片
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            path_img = "img/{}.jpg".format(SKU_ID)
            path_img = os.path.join(BASE_DIR, path_img)
            html_img = self.parse_img_url(img_url)
            with open(path_img, 'wb') as file:
                file.write(html_img)
            # print(href, SKU_ID, sort_by, title, img_url)
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
    from best_seller.seller_urls import jd_urls
    list_jd = jd_urls()
    for tuple2 in list_jd:
        JDBestSelling(*tuple2).run()