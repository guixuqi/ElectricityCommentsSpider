from datetime import datetime
import re
from utils import log_info, logger

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
# Razer Kraken 7.1 Chroma
bestBuy_url3 = "https://www.bestbuy.com/site/razer-kraken-7-1-v2-wired-surround-sound-gaming-headset-for-pc-mac-ps4-black/6136302.p?skuId=6136302"
# Razer Kraken Pro V2
bestBuy_url4 = "https://www.bestbuy.com/site/razer-kraken-pro-v2-wired-stereo-gaming-headset-for-pc-mac-xbox-one-ps4-mobile-devices-black/6136303.p?skuId=6136303"
# logitech-g-pro
bestBuy_url5 = "https://www.bestbuy.com/site/logitech-g-pro-wired-stereo-gaming-headset-for-windows-black/6352842.p?skuId=6352842"
bestBuy_url6 = "https://www.bestbuy.com/site/razer-kraken-wired-stereo-gaming-headset-black/6330450.p?skuId=6330450"
# Soundcore Life NC
bestBuy_url7 = "https://www.bestbuy.com/site/anker-soundcore-life-wireless-in-ear-headphones-black/6253426.p?skuId=6253426"
# Corsair RGB
bestBuy_url8 = "https://www.bestbuy.com/site/corsair-void-pro-rgb-wireless-dolby-7-1-channel-surround-sound-gaming-headset-for-pc-white/6006602.p?skuId=6006602"
# Corsair Void Pro Surround Gaming Headset
bestBuy_url9 = "https://www.bestbuy.com/site/corsair-gaming-void-pro-rgb-usb-wired-dolby-7-1-surround-sound-gaming-headset-carbon-black/6006603.p?skuId=6006603"
# Razer Kraken Tournament
bestBuy_url10 = "https://www.bestbuy.com/site/razer-kraken-tournament-edition-wired-stereo-gaming-headset-for-pc-mac-xbox-one-switch-ps4-mobile-devices-black/6263312.p?skuId=6263312"
# Razer Nari Wireless
bestBuy_url11 = "https://www.bestbuy.com/site/razer-nari-ultimate-wireless-thx-spatial-audio-gaming-headset-for-pc-and-playstation-4-gunmetal/6298660.p?skuId=6298660"
# AirPods
bestBuy_url12 = "https://www.bestbuy.com/site/apple-airpods-with-charging-case-latest-model-white/6084400.p?skuId=6084400"
# HyperX Cloud Alpha
bestBuy_url13 = "https://www.bestbuy.com/site/hyperx-cloud-alpha-wired-stereo-gaming-headset-for-pc-ps4-xbox-one-and-nintendo-switch-red-black/6100109.p?skuId=6100109"
# HyperX Cloud II
bestBuy_url14 = "https://www.bestbuy.com/site/hyperx-cloud-ii-pro-wired-gaming-headset-red/4505300.p?skuId=4505300"


# Amazon
start_url0 = "https://www.amazon.com/Zolo-True-Wireless-Headphones-Technology-Calls-Upgraded/dp/B07GKHYVM8/ref=sxbs_sxwds-stvp"
start_url1 = "https://www.amazon.com/ASTRO-Gaming-A10-Headset-Black-Red/dp/B071S9RGB1/ref=sr_1_1"
# Razer Nari Wireless
start_url2 = "https://www.amazon.com/Razer-Nari-Wireless-Gel-Infused-Cushions/dp/B07G5RKF3W/ref=sr_1_1"
# HyperX Cloud Alpha Gaming Headset
# start_url3 = "https://www.amazon.com/HyperX-Cloud-Stinger-Gaming-Headset/dp/B01L2ZRYVE/ref=sr_1_1_sspa"
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
start_url30 = "https://www.amazon.com/Anker-PowerWave-Wireless-Qi-Certified-Compatible/dp/B00Y839YMU/ref=sr_1_1"  # 链接失效
# Anker 10W Wireless Charger
start_url31 = "https://www.amazon.com/Anker-Qi-Certified-Compatible-Fast-Charging-PowerWave/dp/B01KJL4XNY/ref=sr_1_1"
# Razer Kraken Pro V2
# start_url25 = "https://www.amazon.de/Razer-Thresher-Xbox-Ohrumschließendes-undirektionales/dp/B075YDD1P2/ref=sr_1_1"
# Razer Kraken Tournament  B07G4KD8WW
start_url32 = "https://www.amazon.co.uk/Razer-Kraken-Tournament-Headset-Controller/dp/B07G4KD8WW/ref=sr_1_1"
start_url37 = "https://www.amazon.co.uk/Razer-Headset-Drivers-Playstation-Earcups/dp/B0713QM36X"
# # Corsair RGB   B0749BX1X3 与 B0749CW8X6评论相同
start_url33 = "https://www.amazon.co.uk/Corsair-Customisable-Optimised-Unidirectional-Microphone/dp/B0749BX1X3/ref=sr_1_1"
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
amazon_url34 = "https://www.amazon.co.uk/UNBREAKcable-Wireless-Charger-Qi-Certified-Charging-Black/dp/B07PN288W7/ref=sr_1_55"
amazon_url35 = "https://www.amazon.de/UNBREAKcable-Kabelloses-Qi-zertifizierte-Ladestation-Unterst%C3%BCtzt/dp/B07PN288W7/ref=sr_1_89"
amazon_url36 = "https://www.amazon.fr/UNBREAKcable-Wireless-Charger-Black-1Pack/dp/B07PN288W7/ref=sr_1_75"
# Logitech G Pro
amazon_url_1_0 = "https://www.amazon.com/Logitech-G-Pro-Gaming-Headset/dp/B07PHML2XB/ref=sxbs_sxwds-stvp"

# Anker 10W Wireless Charger
amazon_url_2_0 = "https://www.amazon.co.uk/Anker-Wireless-Qi-Certified-Charging-Fast-Charging/dp/B01KJL4XNY/ref=sr_1_7"
# Anker PowerWave 7.5 Pad
amazon_url_2_1 = "https://www.amazon.co.uk/Anker-PowerWave-Wireless-Charging-Qi-Certified/dp/B0791CPWBG/ref=sr_1_2"
# HyperX Cloud Ⅱ
amazon_url_2_2 = "https://www.amazon.co.uk/HyperX-Cloud-Gaming-Headset-Mobile/dp/B00SAYCXWG/ref=sr_1_1"
# Razer Kraken 7.1 Chroma
amazon_url_2_3 = "https://www.amazon.co.uk/Razer-Surround-Retractable-Microphone-Lighting/dp/B00MVT7BAA/ref=sr_1_3"
# Razer Nari Wireless
amazon_url_2_4 = "https://www.amazon.co.uk/Razer-Virtual-Surround-Wireless-Headset/dp/B07G1Y2K5F/ref=sr_1_4"
# True-Wireless Headphones, zolo liberty
amazon_url_2_5 = "https://www.amazon.co.uk/ZOLO-True-Wireless-Headphones-Technology-Calls-Upgraded/dp/B07GKHYVM8/ref=sr_1_3"
# AirPods
amazon_url_2_6 = "https://www.amazon.co.uk/Apple-Air-Pods-previous-model/dp/B01MCW7EOW/ref=sr_1_21"

amazon_url_4_0 = "https://www.amazon.de/Anker-Qi-Zertifiziertes-Kabelloses-Leistungsstarkes-Induktives/dp/B01KJL4XNY/ref=sr_1_5"
# Anker PowerWave 7.5 Pad
amazon_url_4_1 = "https://www.amazon.de/Anker-PowerWave-Kabelloses-Ladegerät-enthalten/dp/B07917M2M9/ref=sr_1_2"
# HyperX Cloud Ⅱ
amazon_url_4_2 = "https://www.amazon.de/Kingston-HyperX-Cloud-Gaming-Kopfhörer/dp/B00SAYCXWG/ref=sr_1_2"
# HyperX Cloud Alpha
amazon_url_4_3 = "https://www.amazon.de/Cloud-Pro-Gaming-Headset-HyperX-HX-HSCA-RD-EM-Rot/dp/B076GT6XJ9/ref=sr_1_2_sspa"
# PowerPort Wireless 5 Pad
amazon_url_4_4 = "https://www.amazon.de/Anker-PowerPort-Induktive-Ladestation-Qi-fähigen-Schwarz/dp/B0756Z8X82/ref=sr_1_5"
# Razer Kraken pro v2
amazon_url_4_5 = "https://www.amazon.de/Razer-Kraken-Pro-Oval-Unibody-Rahmen/dp/B01MF4V3LO/ref=sr_1_3"
# Razer Kraken Tournament
amazon_url_4_6 = "https://www.amazon.de/Razer-Kraken-Tournament-Black-Kabelgebundenes/dp/B07G4KD8WW/ref=sr_1_2"
# Razer Nari Wireless
amazon_url_4_7 = "https://www.amazon.de/Razer-Nari-Kabelloses-Gaming-Headset-höchstem/dp/B07G1Y2K5F/ref=sr_1_1"
# AirPods
amazon_url_4_8 = "https://www.amazon.de/Apple-479JB51-AirPods/dp/B01MCW7EOW/ref=sr_1_1"

# B07N6NRS8Q
amazon_url38 = "https://www.amazon.co.jp/Zero-Audio-TWZ-1000-%E5%AE%8C%E5%85%A8%E3%83%AF%E3%82%A4%E3%83%A4%E3%83%AC%E3%82%B9%E3%82%B9%E3%83%86%E3%83%AC%E3%82%AA%E3%83%98%E3%83%83%E3%83%89%E3%83%9B%E3%83%B3/dp/B07N6NRS8Q/ref=sr_1_1"
# B075SSLKDB
amazon_url39 = "https://www.amazon.co.jp/Liberty-Bluetooth-%E5%AE%8C%E5%85%A8%E3%83%AF%E3%82%A4%E3%83%A4%E3%83%AC%E3%82%B9%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3-%E3%80%90%E6%9C%80%E5%A4%A724%E6%99%82%E9%96%93%E9%9F%B3%E6%A5%BD%E5%86%8D%E7%94%9F-IPX5%E9%98%B2%E6%B0%B4%E8%A6%8F%E6%A0%BC%E3%80%91/dp/B075SSLKDB/ref=sr_1_1"
# B07KNK8XCP
amazon_url40 = "https://www.amazon.co.jp/%E3%82%BD%E3%83%95%E3%83%88%E3%83%90%E3%83%B3%E3%82%AF%E3%82%BB%E3%83%AC%E3%82%AF%E3%82%B7%E3%83%A7%E3%83%B3-Bluetooth%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3%EF%BC%88%E3%83%96%E3%83%A9%E3%83%83%E3%82%AF%EF%BC%89SoftBank-GLIDiC-SB-WS72-MRTW-BK/dp/B07KNK8XCP/ref=sr_1_1"
# 铁三角
amazon_url41 = "https://www.amazon.co.jp/Audio-Technica-%E3%82%AA%E3%83%BC%E3%83%87%E3%82%A3%E3%82%AA%E3%83%86%E3%82%AF%E3%83%8B%E3%82%AB-ATH-CKS5TW-Bluetooth%E3%82%A4%E3%83%A4%E3%83%9B%E3%83%B3%EF%BC%88%E3%83%96%E3%83%AB%E3%83%BC%EF%BC%89audio-technica/dp/B07T8SSPCV/ref=sr_1_4_sspa"


# yodobashi  31
yodo_url1 = "https://www.yodobashi.com/product/100000001004516643/"  # 黑色

# biccamera  32
bicc_url1 = "https://www.biccamera.com/bc/item/6904415/"  # 黑色

# e-earphone  34
e_ear_url1 = "https://www.e-earphone.jp/shopdetail/000000245037/"  # 黑色

# Kakaku  33
kakaku_url1 = "https://kakaku.com/item/J0000030659/?lid=20190108pricemenu_hot"  # 黑色

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
    bestbuy_urls.append(bestBuy_url3)
    bestbuy_urls.append(bestBuy_url4)
    bestbuy_urls.append(bestBuy_url5)
    bestbuy_urls.append(bestBuy_url6)
    bestbuy_urls.append(bestBuy_url7)
    bestbuy_urls.append(bestBuy_url8)
    bestbuy_urls.append(bestBuy_url9)
    bestbuy_urls.append(bestBuy_url10)
    bestbuy_urls.append(bestBuy_url11)
    bestbuy_urls.append(bestBuy_url12)
    bestbuy_urls.append(bestBuy_url13)
    bestbuy_urls.append(bestBuy_url14)
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
    # url_list.append(start_url33)
    # url_list.append(amazon_url34)
    # url_list.append(amazon_url35)
    # url_list.append(amazon_url36)
    # url_list.append(start_url37)
    # url_list.append(amazon_url_1_0)
    url_list.append(amazon_url38+"$$$"+"SKU-0f2e34d7-6634-4a2c-b40b-0efba00d7585")
    url_list.append(amazon_url39+"$$$"+"SKU-4f500130-4431-46bf-b266-bfc4296653eb")
    url_list.append(amazon_url40+"$$$"+"SKU-a721b98a-d33b-4903-98f4-1795fc6f18f7")
    url_list.append(amazon_url41+"$$$"+"SKU-b6a75800-af77-400c-b6a3-5adcfa45ea27")

    return url_list

def yodo_urls():
    url_lists = []
    url_lists.append(yodo_url1+"$$$"+"SKU-4135abd4-6e26-473f-a8c0-9fa9d2ffd24d")
    return url_lists

def bicc_urls():
    url_lists = []
    url_lists.append(bicc_url1)
    return url_lists

def e_ear_urls():
    url_lists = []
    url_lists.append(e_ear_url1)
    return url_lists

def kakaku_urls():
    url_lists = []
    url_lists.append(kakaku_url1)
    return url_lists

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

