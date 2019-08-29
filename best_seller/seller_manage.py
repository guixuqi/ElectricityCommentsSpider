from best_seller.amazon_seller.amazon_best_selling import AmazonBestSelling
from best_seller.bestbuy_seller.bestbuy_best_selling import BestBuyBestSelling
from best_seller.seller_urls import amazon_urls, bestbuy_urls


def run():
    list_amazon = amazon_urls()
    list_bestbuy = bestbuy_urls()
    for tuple1 in list_amazon:
        AmazonBestSelling().run(*tuple1)
    for tuple2 in list_bestbuy:
        BestBuyBestSelling(*tuple2).run()


if __name__ == '__main__':
    run()