from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json

d = DesiredCapabilities.CHROME
d['loggingPrefs'] = {'performance': 'ALL'}


# def getHttpStatus(browser):
#     for responseReceived in browser.get_log('performance'):
#         try:
#             response = json.loads(responseReceived[u'message'])[u'message'][u'params'][u'response']
#             if response[u'url'] == browser.current_url:
#                 return (response[u'status'], response[u'statusText'])
#         except:
#             pass
#     return None


def getHttpResponseHeader(browser):
    for responseReceived in browser.get_log('performance'):
        try:
            response = json.loads(responseReceived[u'message'])[u'message'][u'params'][u'response']
            # print
            if response[u'url'] == browser.current_url:
                return response[u'headers']
        except:
            pass
    return None


# if __name__ == '__main__':
#     browser = webdriver.Chrome(desired_capabilities=d)
#     url = 'https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.66e57458moteHW&id=587390513906&skuId=4058104517792&user_id=2453006198&cat_id=2&is_b=1&rn=ff8546c9b43b702b41bce33f0077cf11'
#     browser.get(url)
#     t = getHttpStatus(browser)
#     print(t[0])
#     # 因get_log后旧的日志将被清除，两个函数切勿同时使用
#     # print getHttpResponseHeader(browser)
#     browser.quit()
