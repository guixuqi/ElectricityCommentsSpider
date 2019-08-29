

def amazon_urls():
    list_amazon = []
    amazon_headphones_url = "https://www.amazon.com/Best-Sellers-Electronics-Audio-Headphones/zgbs/electronics/172541/ref=zg_bs_nav_e_1_e"   # amazon耳机
    customerNo10 = "AMAZON"
    t0 = (amazon_headphones_url, customerNo10)
    amazon_speaker_url = "https://www.amazon.com/销售排行榜-Electronics-音箱/zgbs/electronics/172563/ref=zg_bs_nav_e_2_667846011"   # amazon音箱
    customerNo11 = "AMAZON1"
    t1 = (amazon_speaker_url, customerNo11)
    amazon_mic_url = "https://www.amazon.com/销售排行榜-Electronics-麦克风/zgbs/electronics/8882489011/ref=zg_bs_nav_e_3_11974521"   # amazon麦克风
    customerNo12 = "AMAZON2"
    t2 = (amazon_mic_url, customerNo12)
    amazon_new_mic_url = "https://www.amazon.com/gp/new-releases/electronics/8882489011/ref=zg_bs_tab_t_bsnr"   # amazon麦克风(新品)
    customerNo13 = "AMAZON3"
    t3 = (amazon_new_mic_url, customerNo13)
    amazon_new_headphones_url = "https://www.amazon.com/gp/new-releases/electronics/172541/ref=zg_bs_tab_t_bsnr"   # amazon耳机(新品)
    customerNo14 = "AMAZON4"
    t4 = (amazon_new_headphones_url, customerNo14)
    amazon_new_speaker_url = "https://www.amazon.com/gp/new-releases/electronics/172563/ref=zg_bs_tab_t_bsnr"   # amazon音箱(新品)
    customerNo15 = "AMAZON5"
    t5 = (amazon_new_speaker_url, customerNo15)
    t6 = ("https://www.amazon.com/s?k=TWS&i=electronics&rh=n%3A172282%2Cn%3A172541&s=review-rank&dc&language=en_US&qid=1566528354&rnid=493964&ref=sr_st_review-rank", "AMAZON6")  # TWS
    t7 = ("https://www.amazon.com/s?k=Game+Headphones&i=electronics&rh=n%3A172541&s=review-rank&qid=1566549516&ref=sr_st_review-rank", "AMAZON7")  # 游戏耳机

    # 英国AMAZON
    t2_0 = ("https://www.amazon.co.uk/Best-Sellers-Electronics-Headphones-Earphones/zgbs/electronics/4085731/ref=zg_bs_nav_ce_2_17489626031", "AMAZON_UK0")  # 耳机
    t2_1 = ("https://www.amazon.co.uk/Best-Sellers-Electronics-Hi-Fi-Speakers/zgbs/electronics/4085831/ref=zg_bsnr_tab_t_bs", "AMAZON_UK1")  # 音箱
    t2_6 = ("https://www.amazon.co.uk/s?k=tws&i=electronics&rh=n%3A4085731&s=review-rank&qid=1566532008&ref=sr_st_review-rank", "AMAZON_UK6")  # TWS
    t2_7 = ("https://www.amazon.co.uk/s?k=game+Headphones&i=electronics&rh=n%3A4085731&s=review-rank&qid=1566532385&ref=sr_st_review-rank", "AMAZON_UK7")  # 游戏耳机
    # 日本AMAZON
    t3_0 = ("https://www.amazon.co.jp/gp/bestsellers/electronics/3477981/ref=zg_bsnr_tab_t_bs", "AMAZON_JP0")  # 耳机
    t3_1 = ("https://www.amazon.co.jp/gp/bestsellers/electronics/171351011/ref=zg_bs_nav_e_2_16462081", "AMAZON_JP1")  # 音箱
    t3_6 = ("https://www.amazon.co.jp/s?k=tws&rh=n%3A3477981&language=ja_JP&ref=nb_sb_noss", "AMAZON_JP6")  # TWS
    t3_7 = ("https://www.amazon.co.jp/s?k=ゲームヘッドセット&i=electronics&rh=n%3A3477981&s=review-rank&__mk_ja_JP=カタカナ&qid=1566787621&ref=sr_st_review-rank", "AMAZON_JP7")  # 游戏耳机
    # 德国AMAZON
    t4_0 = ("https://www.amazon.de/gp/bestsellers/ce-de/570278/ref=zg_bs_nav_ce_2_17303695031", "AMAZON_DE0")  # 耳机
    t4_1 = ("https://www.amazon.de/gp/bestsellers/ce-de/589878/ref=zg_bs_nav_ce_3_3468081", "AMAZON_DE1")  # 音箱
    t4_6 = ("https://www.amazon.de/s?k=tws&s=review-rank&__mk_de_DE=ÅMÅŽÕÑ&qid=1566532896&ref=sr_st_review-rank", "AMAZON_DE6")  # TWS
    t4_7 = ("https://www.amazon.de/s?k=Kopfhörer&i=videogames&s=review-rank&__mk_de_DE=ÅMÅŽÕÑ&qid=1566532699&ref=sr_st_review-rank", "AMAZON_DE7")  # 游戏耳机
    # 法国AMAZON
    t5_0 = ("https://www.amazon.fr/gp/bestsellers/electronics/14054961/ref=zg_bs_nav_ce_4_17371396031", "AMAZON_FR0")  # 耳机
    t5_1 = ("https://www.amazon.fr/gp/bestsellers/amazon-devices/14884240031/ref=zg_bs_nav_3_14254546031", "AMAZON_FR1")  # 音箱
    t5_6 = ("https://www.amazon.fr/s?k=tws&s=review-rank&__mk_fr_FR=ÅMÅŽÕÑ&qid=1566539485&ref=sr_st_review-rank", "AMAZON_FR6")  # TWS
    t5_7 = ("https://www.amazon.fr/s?k=Casques+d’écoute+pour+jeux&__mk_fr_FR=ÅMÅŽÕÑ&ref=nb_sb_noss", "AMAZON_FR7")  # 游戏耳机

    # list_amazon.append(t0)
    # list_amazon.append(t1)
    # list_amazon.append(t2)
    # list_amazon.append(t3)
    # list_amazon.append(t4)
    # list_amazon.append(t5)
    # list_amazon.append(t2_0)
    # list_amazon.append(t2_1)
    # list_amazon.append(t3_0)
    # list_amazon.append(t3_1)
    # list_amazon.append(t4_0)
    # list_amazon.append(t4_1)
    # list_amazon.append(t5_0)
    # list_amazon.append(t5_1)
    # list_amazon.append(t6)
    # list_amazon.append(t7)
    list_amazon.append(t2_6)
    list_amazon.append(t2_7)
    list_amazon.append(t3_6)
    list_amazon.append(t3_7)
    list_amazon.append(t4_6)
    list_amazon.append(t4_7)
    list_amazon.append(t5_6)
    list_amazon.append(t5_7)
    return list_amazon


def bestbuy_urls():
    list_bestbuy = []
    bestbuy_headphones_url = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&sp=-bestsellingsort%20skuidsaas&st=Headphones&intl=nosplash"   # bestbuy耳机
    customerNo0 = "BESTBUY"
    t0 = (bestbuy_headphones_url, customerNo0)
    bestbuy_sound_url = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&qp=category_facet%3DSmart%20Speakers~pcmcat1504117413781&sp=-bestsellingsort%20skuidsaas&st=speaker&type=page&usc=All%20Categories&intl=nosplash"   # bestbuy音箱
    customerNo1 = "BESTBUY1"
    t1 = (bestbuy_sound_url, customerNo1)
    bestbuy_mic_url = "https://www.bestbuy.com/site/searchpage.jsp?_dyncharset=UTF-8&id=pcat17071&qp=category_facet%3DMicrophones~pcmcat152100050038&sc=Global&sp=-bestsellingsort%20skuidsaas&st=microphone&type=page&usc=All%20Categories&intl=nosplash"   # bestbuy麦克风
    customerNo2= "BESTBUY2"
    t2 = (bestbuy_mic_url, customerNo2)
    bestbuy_TWS_url = "https://www.bestbuy.com/site/headphones/true-wireless-headphones/pcmcat1498066426386.c?id=pcmcat1498066426386&intl=nosplash"   # bestbuy TWS
    customerNo6= "BESTBUY6"
    t6 = (bestbuy_TWS_url, customerNo6)
    bestbuy_gaming_url = "https://www.bestbuy.com/site/pc-gaming-hardware/gaming-headsets/pcmcat230800050019.c?id=pcmcat230800050019&intl=nosplash"   # bestbuy 游戏耳机
    customerNo7= "BESTBUY7"
    t7 = (bestbuy_gaming_url, customerNo7)

    # list_bestbuy.append(t0)
    # list_bestbuy.append(t1)
    # list_bestbuy.append(t2)
    list_bestbuy.append(t6)
    list_bestbuy.append(t7)
    return list_bestbuy


def jd_urls():
    list_jd = []
    j0 = ("https://list.jd.com/list.html?cat=652,828,842", "JD0")  # 耳机
    j1 = ("https://list.jd.com/list.html?cat=652,828,841", "JD1")  # 音箱
    j6 = ("https://search.jd.com/search?keyword=TWS&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=TWS&cid2=828&cid3=842&psort=3&click=0", "JD6")  # TWS
    j7 = ("https://list.jd.com/list.html?cat=652,828,842&ev=3155_2104&sort=sort_totalsales15_desc&trans=1&JL=3_用途_游戏耳机#J_crumbsBar", "JD7")  # 游戏耳机
    list_jd.append(j0)
    list_jd.append(j1)
    list_jd.append(j6)
    list_jd.append(j7)
    return list_jd


def tmall_urls():
    list_tm = []
    t0 = ("https://list.tmall.com/search_product.htm?q=%B6%FA%BB%FA&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton", "TMALL0")  # 耳机
    t1 = ("https://list.tmall.com/search_product.htm?q=%D2%F4%CF%E4&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton", "TMALL1")  # 音箱
    t6 = ("https://list.tmall.com/search_product.htm?q=tws%B6%FA%BB%FA&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&xl=TWS_2&from=mallfp..pc_1_suggest", "TMALL6")  # TWS
    t7 = ("https://list.tmall.com/search_product.htm?q=%D3%CE%CF%B7%B6%FA%BB%FA&type=p&vmarket=&spm=875.7931836%2FB.a2227oh.d100&from=mallfp..pc_1_searchbutton", "TMALL7")  # 游戏耳机
    list_tm.append(t0)
    list_tm.append(t1)
    list_tm.append(t6)
    list_tm.append(t7)
    return list_tm
