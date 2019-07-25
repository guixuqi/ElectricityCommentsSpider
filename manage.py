import re
import threading
import time
from datetime import datetime
from JD import jd_review, new_jd
from TMALL import tmall_review, new_tmall
from amazon import amazon_review, new_amazon
from bestbuy import bestbuy_review, new_bestbuy
from biccamera import bicc_review, new_bicc
from earphone import earphone_review, new_ear
from kakaku import kakaku_review, new_kakaku
from utils import log_info, get_urls, close_db, select_count
from yodobashi import yodo_review, new_yodo


def list_split(urls):
    tms = []
    jds = []
    bys = []
    ams = []
    yos = []
    bis = []
    eas = []
    kas = []
    for u in urls:
        if u == None:
            continue
        if re.search(r"tmall.com", u):
            tms.append(u)
        elif re.search(r"jd.com", u):
            jds.append(u)
        elif re.search(r".bestbuy.", u):
            bys.append(u)
        elif re.search(r".amazon.", u):
            ams.append(u)
        elif re.search(r".yodobashi.", u):
            yos.append(u)
        elif re.search(r".biccamera.", u):
            bis.append(u)
        elif re.search(r".e-earphone.", u):
            eas.append(u)
        elif re.search(r"kakaku.", u):
            kas.append(u)
        else:
            log_info("暂不支持此类网站数据抓取")
    return tms, jds, bys, ams, yos, bis, eas, kas


def run_new(urls):  # 新url调用接口
    tms, jds, bys, ams, yos, bis, eas, kas = list_split(urls)
    amazon_review.run(ams)
    bestbuy_review.run(bys)
    jd_review.run(jds)
    tmall_review.run(tms)
    yodo_review.run(yos)
    bicc_review.run(bis)
    earphone_review.run(eas)
    kakaku_review.run(kas)

    # amazon = threading.Thread(target=amazon_review.run, args=(ams,))
    # bestbuy = threading.Thread(target=bestbuy_review.run, args=(bys,))
    # jd = threading.Thread(target=jd_review.run, args=(jds,))
    # tmall = threading.Thread(target=tmall_review.run, args=(tms,))
    # amazon.start()
    # bestbuy.start()
    # jd.start()
    # tmall.start()
    # amazon.join()
    # bestbuy.join()
    # jd.join()
    # tmall.join()


def run_today(urls):  # 抓取每天新评论接口
    tms, jds, bys, ams, yos, bis, eas, kas = list_split(urls)
    new_amazon.main(ams)
    new_bestbuy.main(bys)
    new_jd.main(jds)
    new_tmall.main(tms)
    new_yodo.main(yos)
    new_bicc.main(bis)
    new_ear.main(eas)
    new_kakaku.main(kas)

    # amazon = threading.Thread(target=new_amazon.main, args=(ams,))
    # bestbuy = threading.Thread(target=new_bestbuy.main, args=(bys,))
    # jd = threading.Thread(target=new_jd.main, args=(jds,))
    # tmall = threading.Thread(target=new_tmall.main, args=(tms,))
    # amazon.start()
    # bestbuy.start()
    # jd.start()
    # tmall.start()
    # amazon.join()
    # bestbuy.join()
    # jd.join()
    # tmall.join()


# 主逻辑
def main():
    # 1.从数据库取出所有urls,skus
    results = get_urls()
    list1 = []
    list2 = []
    # 2.遍历
    for result in results:
        url = result[0]
        sku_detail_id = result[1]
        # 3.以sku_detail_id作为条件查询数据库评论count
        count = select_count(sku_detail_id)
        # 4.数量为0,list1.append加入到调用新url接口的列表
        if count == 0:
            list1.append(url)
        # 5.不为0,list2.append加入到调用抓取每天评论接口的列表
        else:
            list2.append(url)
    # print(list1, list2)
    if list1:
        # 调用新url接口
        run_new(list1)
    if list2:
        # 调用抓取每天的评论接口
        run_today(list2)
    # 关闭数据库
    close_db()


# 定时运行
def running(h, m):
    while True:
        now = datetime.now()
        if now.hour == h and now.minute == m:
            main()
        time.sleep(60)


# 运行入口
if __name__ == '__main__':
    # running(18, 10)
    main()