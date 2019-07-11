import json
from datetime import datetime
import cx_Oracle
from Logs.log import log1


# 数据库配置
dsnStr = cx_Oracle.makedsn("192.168.110.205", 1521, "EIP")
# dsnStr = cx_Oracle.makedsn("192.168.110.214", 1521, "HORNEIP")  # 测试库
conn = cx_Oracle.connect("EIP", "EIP", dsnStr)
c = conn.cursor()

# 配置抓取日期
review_days = 1

# selenium定位标签等待时间
wait = 30

# 评论内容分拆
def review_split(REVIEW_TEXT):
    REVIEW_TEXT = REVIEW_TEXT.encode('gbk', 'ignore')
    length = len(REVIEW_TEXT)
    num = 4000
    if length < num:
        # REVIEW_TEXT = REVIEW_TEXT.decode('gbk')
        REVIEW_TEXT1 = REVIEW_TEXT
        REVIEW_TEXT2 = b""
        REVIEW_TEXT3 = b""
        REVIEW_TEXT4 = b""
        REVIEW_TEXT5 = b""
    elif num * 2 > length > num:
        # REVIEW_TEXT = REVIEW_TEXT.decode('gbk')
        REVIEW_TEXT1 = REVIEW_TEXT[0:num]
        REVIEW_TEXT2 = REVIEW_TEXT[num:num * 2]
        REVIEW_TEXT3 = b""
        REVIEW_TEXT4 = b""
        REVIEW_TEXT5 = b""
    elif num * 3 > length > num * 2:
        # REVIEW_TEXT = REVIEW_TEXT.decode('gbk')
        REVIEW_TEXT1 = REVIEW_TEXT[0:num]
        REVIEW_TEXT2 = REVIEW_TEXT[num:num * 2]
        REVIEW_TEXT3 = REVIEW_TEXT[num * 2:num * 3]
        REVIEW_TEXT4 = b""
        REVIEW_TEXT5 = b""
    else:
        # REVIEW_TEXT = REVIEW_TEXT.decode('gbk')
        REVIEW_TEXT1 = REVIEW_TEXT[0:num]
        REVIEW_TEXT2 = REVIEW_TEXT[num:num * 2]
        REVIEW_TEXT3 = REVIEW_TEXT[num * 2:num * 3]
        REVIEW_TEXT4 = REVIEW_TEXT[num * 3:num * 4]
        REVIEW_TEXT5 = REVIEW_TEXT[num * 4:num * 5]
    return REVIEW_TEXT1.decode('gbk'), REVIEW_TEXT2.decode('gbk'), REVIEW_TEXT3.decode('gbk'), REVIEW_TEXT4.decode('gbk'), REVIEW_TEXT5.decode('gbk')

# 从数据库取出所有urls,sku_id
def get_urls():
    sql = "select REVIEW_URL,SKU_CODE from ECOMMERCE_SKU_DETAIL"
    results = c.execute(sql).fetchall()  # [(),()]
    return results

# 以SKU_ID和ECOMMERCE_CODE联合查询ECOMMERCE_SKU_DETAIL表SKU_DETAIL_ID的值
def SKU_DETAIL_ID(SKU_ID, ECOMMERCE_CODE):
    sql_detail_id = "select SKU_ID from ECOMMERCE_SKU_DETAIL p where SKU_CODE='{}' and ECOMMERCE_CODE='{}'".format(
        SKU_ID, ECOMMERCE_CODE)
    try:
        return c.execute(sql_detail_id).fetchone()[0]
    except Exception as e:
        print(e, "查询不到SKU_DETAIL_ID")
        return False


# 查询总评论数量
def select_count(SKU_ID):
    sql_count = "select count(REVIEW_ID) from ECOMMERCE_REVIEW_P p where sku_id='{}'".format(SKU_ID)
    count = c.execute(sql_count).fetchone()[0]
    return count


# 查询总评分数量
def star_count(SKU_ID):
    sql_count = "select count(SKU_OVERALLSTAR) from ECOMMERCE_SKU_STAR_S p where sku_id='{}'".format(SKU_ID)
    count = c.execute(sql_count).fetchone()[0]
    return count


# 评论内容保存
def save_review(REVIEW_ID, SKU_ID, score, REVIEW_NAME, REVIEW_TITLE, REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3,
                REVIEW_TEXT4, REVIEW_DATE, REVIEW_TEXT5, SKU_DETAIL_ID):
    CREATE_TIME = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    sql = "INSERT INTO ECOMMERCE_REVIEW_P(REVIEW_ID, SKU_ID, REVIEW_STAR, REVIEW_NAME, REVIEW_TITLE, REVIEW_TEXT1, REVIEW_TEXT2, REVIEW_TEXT3, REVIEW_TEXT4, REVIEW_DATE, CREATE_TIME, REVIEW_TEXT5, SKU_DETAIL_ID) VALUES('{}', '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}', to_date('{}','yyyy/MM/dd'), to_date('{}','yyyy/MM/dd HH24:mi:ss'), '{}', '{}')".format(
        REVIEW_ID, SKU_ID, score, REVIEW_NAME.replace("'", ""),
        REVIEW_TITLE.replace("'", ""), REVIEW_TEXT1.replace("'", ""),
        REVIEW_TEXT2.replace("'", ""), REVIEW_TEXT3.replace("'", ""), REVIEW_TEXT4.replace("'", ""),
        REVIEW_DATE, CREATE_TIME, REVIEW_TEXT5.replace("'", ""), SKU_DETAIL_ID)
    return sql

# 保存评论总评分(新增)
def save_score(SKU_ID, score, name, SKU_DETAIL_ID):
    CREATE_TIME = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    sql_star = "insert into ECOMMERCE_SKU_STAR_S(SKU_ID, SCORE, CREATE_TIME, UPDATE_TIME, SKU_DETAIL_ID) values('{}',{}, to_date('{}','yyyy/MM/dd HH24:mi:ss'), to_date('{}','yyyy/MM/dd HH24:mi:ss'), '{}')".format(
        SKU_ID, score, CREATE_TIME, CREATE_TIME, SKU_DETAIL_ID)
    try:
        c.execute(sql_star)
        conn.commit()
    except Exception as e:
        print(e, "{}({})保存失败".format(name, SKU_ID))
        logger(name, SKU_ID, "保存失败")
        conn.rollback()


# 保存评论总评分(更新)
def update_score(score, SKU_ID, name, SKU_DETAIL_ID):
    UPDATE_TIME = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    sql_star = "update ECOMMERCE_SKU_STAR_S set score={}, UPDATE_TIME=to_date('{}','yyyy/MM/dd HH24:mi:ss') where SKU_DETAIL_ID='{}'".format(score, UPDATE_TIME, SKU_DETAIL_ID)
    try:
        c.execute(sql_star)
        conn.commit()
    except Exception as e:
        print(e, "{}({})更新失败".format(name, SKU_ID))
        logger(name, SKU_ID, "更新失败")
        conn.rollback()


# 查询数据库评论最晚评论日期
def max_date(sku_id):
    sql = "select max(review_date) from ECOMMERCE_REVIEW_P where sku_id='{}'".format(sku_id)
    max_date = c.execute(sql).fetchone()[0]
    return max_date


# 更新评论爬取
def newReview(max_date, re_date):
    if not max_date or (re_date - max_date).days < 0:
        return True

# def newReview(re_date):
#     now = datetime.now()
#     if (now - re_date).days > 10:
#         return True


# 随机UA
import random

def get_ua():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    # print(ua)
    return ua


# 以json存本地
def save_json(commentList):
    comments_js = json.dumps(commentList, indent=2, separators=(',', ':'), ensure_ascii=False)
    with open('comments_{}.json'.format(commentList[0]["SKU_ID"]), 'w', encoding='utf-8') as f:
        f.write(comments_js)


# 日志记录异常
def logger(name, sku_id, info=None):
    log1.error("{}({})报错信息：{}".format(name, sku_id, info), exc_info=1)


def log_info(info):
    log1.info(info)


# 数据库保存,关闭
def save_db(sql, name, sku_id):
    try:
        c.execute(sql)
        conn.commit()
    except Exception as e:
        print(e, "{}({})保存失败".format(name, sku_id))
        logger(name, sku_id, "保存失败")
        conn.rollback()


def close_db():
    c.close()
    conn.close()

