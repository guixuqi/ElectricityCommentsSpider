# -*-coding:utf-8-*-
import time
from selenium import webdriver
import string
import zipfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains


proxyHost = "http-proxy-t2.dobel.cn"
proxyPort = "9180"
proxyUser = "GUIXUQIG2BCNKM80"
proxyPass = "9Bb66Yz7"

def create_proxy_auth_extension(proxy_host, proxy_port,
                                   proxy_username, proxy_password,
                                   scheme='http', plugin_path=None):
        if plugin_path is None:
            plugin_path = r'./{}_{}@http-proxy-sg2.dobel.cn_9180.zip'.format(proxy_username, proxy_password)

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "dobel http proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = string.Template(
            """
            var config = {
                mode: "fixed_servers",
                rules: {
                    singleProxy: {
                        scheme: "${scheme}",
                        host: "${host}",
                        port: parseInt(${port})
                    },
                    bypassList: ["foobar.com"]
                }
              };

            chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

            function callbackFn(details) {
                return {
                    authCredentials: {
                        username: "${username}",
                        password: "${password}"
                    }
                };
            }

            chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
            );
"""
        ).substitute(
            host=proxy_host,
            port=proxy_port,
            username=proxy_username,
            password=proxy_password,
            scheme=scheme,
        )

        with zipfile.ZipFile(plugin_path, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)

        return plugin_path

proxy_auth_plugin_path = create_proxy_auth_extension(
        proxy_host=proxyHost,
        proxy_port=proxyPort,
        proxy_username=proxyUser,
        proxy_password=proxyPass)

options = webdriver.ChromeOptions()
# options.binary_location = ''
#options.add_argument('window-size=800x841')
#options.add_argument('headless')
#options.add_argument("--start-maximized")
options.add_extension(proxy_auth_plugin_path)

driver = webdriver.Chrome(chrome_options=options)
# url = 'https://detail.tmall.com/item.htm?id=574870586003'
url = 'https://www.amazon.co.jp/'
# driver.get('https://detail.tmall.com/item.htm?id=574870586003')
url_ip = "http://ip.dobel.cn/current-ip"
set_ip = "http://ip.dobel.cn/switch-ip"

def parse_url(url):
    driver.maximize_window()
    driver.get(set_ip)
    time.sleep(2)
    driver.get(url)


def close_alter():
    try:
        close_login = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'sufei-dialog-close')))
        driver.execute_script("arguments[0].click()", close_login)
    except:
        pass


def click_review():
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='J_TabBarBox']//a[text()='累计评价 ']"))).click()


def order_time():
    elements = WebDriverWait(driver, 20).until(
        lambda driver: driver.find_element_by_xpath("//span[@class='tm-current']"))
    actions = ActionChains(driver)
    actions.move_to_element(elements).perform()
    time.sleep(5)
    element_artist = WebDriverWait(driver, 20).until(
        lambda driver: driver.find_elements_by_tag_name('a"'))
    element_artist[1].click()


# 发送请求
parse_url(url)
time.sleep(3)
# 关闭弹窗
close_alter()
time.sleep(5)
# 点击累计评论
click_review()
# 等待二维码消失
time.sleep(15)
# 点击按时间排序
order_time()
time.sleep(5)
# 总评分
score = WebDriverWait(driver, 20).until(
    lambda driver: driver.find_element_by_xpath("//div[@class='rate-score']/strong")).text
score = float(score)
print(score)

# driver.quit()