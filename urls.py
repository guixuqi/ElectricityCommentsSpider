from datetime import datetime
import re
from utils import log_info, logger
from utils import conn, c

# JD
jd_url0 = "https://item.jd.com/100002361195.html"  # 录音笔C1
jd_url1 = "https://item.jd.com/100005152874.html"  # KUGOU X5
jd_url2 = "https://item.jd.com/46066831853.html"  # KUGOU X5
jd_url3 = "https://item.jd.com/2245024.html"  # 叮咚 Q1
jd_url4 = "https://item.jd.com/11463583653.html"  # 晓雅MINI
jd_url5 = "https://item.jd.com/7438547.html"
# jd_url13 = "https://item.jd.com/7224868.html"  # 晓雅MINI 5与13几乎一样的评论
jd_url6 = "https://item.jd.com/24818305875.html"  # 雷蛇（RAZER）
jd_url7 = "https://item.jd.com/100002501954.html"  # JBL UA FLASH ******已更新网站https://item.jd.com/41014808466.html
jd_url14 = "https://item.jd.com/41014808466.html"
jd_url8 = "https://item.jd.com/27115314210.html"  # Huawei/华为 AM185
jd_url9 = "https://item.jd.com/8031600.html"  # JBL V150NC
jd_url10 = "https://item.jd.com/100001470134.html"  # FlyPods Pro
jd_url11 = "https://item.jd.com/34326476497.html"  # O-Free
jd_url12 = "https://item.jd.com/100001667527.html"  # Freebuds 2
jd_url15 = "https://item.jd.com/4298564.html"  # Razer Kraken 7.1 Chroma

# BestBuy
bestBuy_url0 = "https://www.bestbuy.com/site/astro-gaming-a10-wired-stereo-gaming-headset-for-xbox-one-green-black/5892993.p?skuId=5892993&intl=nosplash"  # A10
bestBuy_url1 = "https://www.bestbuy.com/site/astro-gaming-a50-wireless-dolby-7-1-surround-sound-gaming-headset-for-xbox-one-and-windows-black-and-green/5368400.p?skuId=5368400"
bestBuy_url2 = "https://www.bestbuy.com/site/astro-gaming-astro-a50-base-station-rf-wireless-over-the-ear-headphones-black/6349969.p?skuId=6349969"  # A50

# Amazon
start_url0 = "https://www.amazon.com/Zolo-True-Wireless-Headphones-Technology-Calls-Upgraded/dp/B07GKHYVM8/ref=sxbs_sxwds-stvp"
start_url1 = "https://www.amazon.com/ASTRO-Gaming-A10-Headset-Black-Red/dp/B071S9RGB1/ref=sr_1_1"
# Razer Nari Wireless
start_url2 = "https://www.amazon.com/Razer-Nari-Wireless-Gel-Infused-Cushions/dp/B07G5RKF3W/ref=sr_1_1"
# HyperX Cloud Alpha Gaming Headset
start_url3 = "https://www.amazon.com/HyperX-Cloud-Stinger-Gaming-Headset/dp/B01L2ZRYVE/ref=sr_1_1_sspa"
# HyperX Cloud II Gaming Headset
start_url4 = "https://www.amazon.com/HyperX-Cloud-Gaming-Headset-KHX-HSCP-RD/dp/B00SAYCXWG/ref=sr_1_2"
# Anker SoundBuds Life Wireless Lightweight Neckband Headphones
start_url5 = "https://www.amazon.com/Anker-Lightweight-Headphones-Professional-Cancelling/dp/B06XGBPW3D/ref=sr_1_1"
# Corsair RGB
start_url6 = "https://www.amazon.com/CORSAIR-Glaive-Pro-Comfortable-Interchangeable/dp/B07PWJ43MB/ref=sr_1_1_sspa"
# HyperX Cloud Alpha
start_url7 = "https://www.amazon.com/HyperX-Cloud-Alpha-Gaming-Headset/dp/B074NBSF9N/ref=sr_1_2"
# Razer Kraken 7.1 Chroma
start_url8 = "https://www.amazon.com/Razer-Kraken-Chroma-Gaming-Headset/dp/B072DRCM1Q/ref=sr_1_2"
start_url9 = "https://www.amazon.com/Razer-Kraken-Chroma-Gaming-Headset/dp/B00MTWV0RO/ref=sr_1_4"
# Razer Kraken Pro V2
start_url10 = "https://www.amazon.com/Razer-Kraken-Pro-Lightweight-Line/dp/B06Y3YN2C8/ref=sr_1_1"
# Apple AirPods
start_url11 = "https://www.amazon.com/dp/B01MQWUXZS/ref=us_comp_a_airpods_13011"
# Soundcore Truly-Wireless Earbuds
start_url13 = "https://www.amazon.co.uk/Soundcore-Truly-Wireless-Headphones-Graphene-Enhanced-Waterproof/dp/B07MCGZK3B/ref=sr_1_1"
# Soundcore Life NC
start_url14 = "https://www.amazon.com/Headphones-Cancellation-Transparency-Multi-Device-Connection/dp/B07H314BYH/ref=sr_1_1"

# Razer Kraken Pro V2
start_url19 = "https://www.amazon.co.uk/ZOLO-Total-Wireless-Technology-Sweatproof-Refurbished/dp/B01N3AJ0ID/ref=sr_1_1"
# Astro A10
start_url23 = "https://www.amazon.co.uk/ASTROGAMING-939-001508-Astro-A10-Headset/dp/B071S9RGB1/ref=sr_1_2"
# Razer Kraken Pro V2
start_url24 = "https://www.amazon.com/Razer-Kraken-Tournament-Gel-Infused-Cushions/dp/B06Y3YNSMJ/ref=sr_1_1"
# Astro Gaming A50
start_url26 = "https://www.amazon.com/ASTRO-Gaming-A50-Wireless-Dolby-Headset/dp/B01G3WBCQY/ref=sr_1_1"
# PowerPort Wireless 5 Pad
start_url27 = "https://www.amazon.com/Anker-Qi-Certified-Ultra-Slim-Compatible-PowerPort/dp/B0756Z8X82/ref=sr_1_1"
# PowerPort Wireless 5 Stand
start_url28 = "https://www.amazon.com/Anker-Wireless-Qi-Certified-Compatible-PowerPort/dp/B0753Z4PGC/ref=sr_1_1"
# Anker PowerWave 7.5 Pad
start_url29 = "https://www.amazon.com/Anker-PowerWave-Wireless-Qi-Certified-Compatible/dp/B078WRCW35/ref=sr_1_1"
# Anker Wireless Charger Charging Pad
start_url30 = "https://www.amazon.com/Anker-PowerWave-Wireless-Qi-Certified-Compatible/dp/B00Y839YMU/ref=sr_1_1"
# Anker 10W Wireless Charger
start_url31 = "https://www.amazon.com/Anker-Qi-Certified-Compatible-Fast-Charging-PowerWave/dp/B01KJL4XNY/ref=sr_1_1"
# Razer Kraken Pro V2
# start_url25 = "https://www.amazon.de/Razer-Thresher-Xbox-Ohrumschließendes-undirektionales/dp/B075YDD1P2/ref=sr_1_1"
# Razer Kraken Tournament  B07G4KD8WW
start_url32 = "https://www.amazon.co.uk/Razer-Kraken-Tournament-Headset-Controller/dp/B07G4KD8WW/ref=sr_1_1"
# # Corsair RGB   B0749BX1X3 与 B0749CW8X6评论相同
# start_url33 = "https://www.amazon.co.uk/Corsair-Customisable-Optimised-Unidirectional-Microphone/dp/B0749BX1X3/ref=sr_1_1"
start_url22 = "https://www.amazon.de/Gaming-Headset-PS4Xbox-OneMobile-PlayStation/dp/B0711V7BV6/ref=sr_1_1"
start_url25 = "https://www.amazon.de/Razer-Thresher-Xbox-Ohrumschließendes-undirektionales/dp/B075YDD1P2/ref=sr_1_1"
# Corsair Void Pro Surround Gaming Headset
start_url12 = "https://www.amazon.co.uk/Corsair-Compatible-Microfibre-Unidirectional-Microphone/dp/B0749CW8X6/ref=sr_1_1"
# Corsair RGB
start_url15 = "https://www.amazon.com/Element-Headset-Virtual-Surround-illumination/dp/B0748K7JW6"
# Anker TWS
start_url16 = "https://www.amazon.com/Zolo-Z2000-Liberty-Wireless-Headphones/dp/B075JBP2P7/ref=sr_1_2"
# Anker TWS
start_url17 = "https://www.amazon.de/ZOLO-Bluetooth-Technologie-Schweißfest-unterstützt-Schwarz/dp/B075JBP2P7/ref=sr_1_1"
# Anker TWS
start_url18 = "https://www.amazon.co.uk/ZOLO-Total-Wireless-Technology-Sweatproof-Refurbished/dp/B075JBP2P7/ref=sr_1_1"
start_url21 = "https://www.amazon.de/Corsair-WIRELESS-Headset-Wireless-schwarz/dp/B0749BX1X3/ref=sr_1_1"

# B07N6NRS8Q
amazon_url34 = "https://www.amazon.co.jp/Zero-Audio-TWZ-1000-%E5%AE%8C%E5%85%A8%E3%83%AF%E3%82%A4%E3%83%A4%E3%83%AC%E3%82%B9%E3%82%B9%E3%83%86%E3%83%AC%E3%82%AA%E3%83%98%E3%83%83%E3%83%89%E3%83%9B%E3%83%B3/dp/B07N6NRS8Q/ref=sr_1_1"
# B075SSLKDB
amazon_url35 = "https://www.amazon.co.jp/Liberty-Bluetooth-%E5%AE%8C%E5%85%A8%E3%83%AF%E3%82%A4%E3%83%A4%E3%83%AC%E3%82%B9%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3-%E3%80%90%E6%9C%80%E5%A4%A724%E6%99%82%E9%96%93%E9%9F%B3%E6%A5%BD%E5%86%8D%E7%94%9F-IPX5%E9%98%B2%E6%B0%B4%E8%A6%8F%E6%A0%BC%E3%80%91/dp/B075SSLKDB/ref=sr_1_1"
# B07KNK8XCP
amazon_url36 = "https://www.amazon.co.jp/%E3%82%BD%E3%83%95%E3%83%88%E3%83%90%E3%83%B3%E3%82%AF%E3%82%BB%E3%83%AC%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3-Bluetooth%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3%EF%BC%88%E3%83%96%E3%83%A9%E3%83%83%E3%82%AF%EF%BC%89SoftBank-GLIDiC-SB-WS72-MRTW-BK/dp/B07KNK8XCP/ref=sr_1_1"

# Tmall
tmall_url1 = "https://detail.tmall.com/item.htm?id=590865770191"  # KUGOU X5
tmall_url2 = "https://detail.tmall.com/item.htm?id=528515320283"  # 华为 AM185
tmall_url3 = "https://detail.tmall.com/item.htm?id=565187422922"  # HyperX Cloud Alpha
tmall_url4 = "https://detail.tmall.com/item.htm?id=552634156539"  # HyperX Cloud II
tmall_url5 = "https://detail.tmall.com/item.htm?id=580233296207"  # FlyPods Pro
tmall_url6 = "https://detail.tmall.com/item.htm?id=574870586003"  # O-Free

def tmall_urls():
    url_list = []
    url_list.append(tmall_url3)
    url_list.append(tmall_url4)
    url_list.append(tmall_url5)
    url_list.append(tmall_url6)
    url_list.append(tmall_url1)
    url_list.append(tmall_url2)


    return url_list

def jd_urls():
    url_list = []
    url_list.append(jd_url0)
    url_list.append(jd_url1)
    url_list.append(jd_url2)
    url_list.append(jd_url3)
    url_list.append(jd_url4)
    url_list.append(jd_url5)
    url_list.append(jd_url6)
    url_list.append(jd_url7)
    url_list.append(jd_url8)
    url_list.append(jd_url9)
    url_list.append(jd_url10)
    url_list.append(jd_url11)
    url_list.append(jd_url12)
    url_list.append(jd_url14)
    url_list.append(jd_url15)

    return url_list

def bestbuy_urls():
    bestbuy_urls = []
    bestbuy_urls.append(bestBuy_url0)
    bestbuy_urls.append(bestBuy_url1)
    bestbuy_urls.append(bestBuy_url2)

    return bestbuy_urls

def amazon_urls():
    url_list = []
    # url_list.append(start_url0)
    # url_list.append(start_url1)
    # url_list.append(start_url2)
    # url_list.append(start_url3)
    # url_list.append(start_url4)
    # url_list.append(start_url5)
    # url_list.append(start_url6)
    # url_list.append(start_url7)
    # url_list.append(start_url8)
    # url_list.append(start_url9)
    # url_list.append(start_url10)
    # url_list.append(start_url11)
    # url_list.append(start_url12)
    # url_list.append(start_url13)
    # url_list.append(start_url14)
    # url_list.append(start_url15)
    # url_list.append(start_url16)
    # url_list.append(start_url17)
    # url_list.append(start_url18)
    # url_list.append(start_url19)
    # url_list.append(start_url21)
    # url_list.append(start_url22)
    # url_list.append(start_url23)
    # url_list.append(start_url24)
    # url_list.append(start_url25)
    # url_list.append(start_url26)
    # url_list.append(start_url27)
    # url_list.append(start_url28)
    # url_list.append(start_url29)
    # url_list.append(start_url30)
    # url_list.append(start_url31)
    # url_list.append(start_url32)
    url_list.append(amazon_url34)
    url_list.append(amazon_url35)
    url_list.append(amazon_url36)

    return url_list

# 数据库插入urls
# def insert(urls, role):
#     for url in urls:
#         create_time = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
#         sku_id = re.search(r"{}".format(role), url).group(1)
#         sql = "insert into ECOMMERCE_REVIEW_URL(sku_id,review_url,create_time) values('{}', '{}', to_date('{}','yyyy/MM/dd HH24:mi:ss'))".format(sku_id, url, create_time)
#         try:
#             c.execute(sql)
#             conn.commit()
#         except Exception as e:
#             # print(e, "{}保存失败".format(url))
#             # log_info("{}保存数据库失败".format(url))
#             conn.rollback()

