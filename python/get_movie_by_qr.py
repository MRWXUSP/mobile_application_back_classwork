# 

import os
import time
import pymysql
import requests
from lxml import etree
from url_get import get_and_sleep
from url_get import selenium_get
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# url example:
# url = "https://movie.douban.com/subject/36512371/"

# 电影类
# 以下数据除特殊标注外均为字符串
# uid: 电影的唯一标识符
# title: 电影标题
# rating: 电影评分
# vote_num: 电影评分人数
# stars5: 5星评分人数占比
# stars4: 4星评分人数占比
# stars3: 3星评分人数占比
# stars2: 2星评分人数占比
# stars1: 1星评分人数占比
# director: 电影导演
# editor: 电影编剧
# actors: 电影演员
# genre: 电影类型
# country: 制片国家
# 语言: 电影语言
# release_date: 电影上映日期
# duration: 电影时长
# other_name: 电影其他名称
# IMDb: 电影IMDb编号
# summary: 电影简介

class Movie:
    def __init__(self, uid, title, rating, vote_num, stars5, stars4, stars3, stars2, stars1,
                 director, editor, actors, genre, country, language, release_date, duration,
                 other_name, IMDb, summary):
        self.uid = uid
        self.title = title
        self.rating = rating
        self.vote_num = vote_num
        self.stars5 = stars5
        self.stars4 = stars4
        self.stars3 = stars3
        self.stars2 = stars2
        self.stars1 = stars1
        self.director = director
        self.editor = editor
        self.actors = actors
        self.genre = genre
        self.country = country
        self.language = language
        self.release_date = release_date
        self.duration = duration
        self.other_name = other_name
        self.IMDb = IMDb
        self.summary = summary

    def __str__(self):
        return f"Movie({self.uid}, {self.title}, {self.rating}, {self.vote_num}, {self.stars5}, {self.stars4}, {self.stars3}, {self.stars2}, {self.stars1}, {self.director}, {self.editor}, {self.actors}, {self.genre}, {self.country}, {self.language}, {self.release_date}, {self.duration}, {self.other_name}, {self.IMDb}, {self.summary})"

def login_qr(driver):
    # 打开豆瓣登录页面
    login_url = "https://accounts.douban.com/passport/login?source=movie"
    selenium_get(login_url, driver)

    # 等待页面加载
    time.sleep(2)

    # 切换到扫码登录
    try:
        password_login_button = driver.find_element(By.XPATH, '//*[@id="account"]/div[2]/div[2]/div/div[1]/div/div[1]/a[1]')
    except:
        print("没有找到扫码登录按钮")
        driver.quit()
        exit(1)
    password_login_button.click()
    # 等待页面加载
    time.sleep(2)

    try:
        qr_scan = driver.find_element(By.XPATH, '//*[@id="account"]/div[2]/div[2]/div/div[3]/div[1]/div[2]/img')
        print("扫码登录按钮点击成功")
    except:
        print("扫码登录按钮点击失败")
        driver.quit()
        exit(1)
    
    while True:
        # 获得扫码登录的二维码
        header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
        response = requests.get(qr_scan.get_attribute("src"), headers=header)
        if response.status_code == 200:
            current_path = os.path.dirname(os.path.abspath(__file__))
            with open(os.path.join(current_path, "./img_temp/qr_code.png"), "wb") as f:
                f.write(response.content)
        else:
            print("二维码下载失败")
            driver.quit()
            exit(1)
        print("请前往./img_temp/qr_code.png扫码登录")
        try:
            WebDriverWait(driver, 20).until(EC.url_changes(driver.current_url))
        except Exception as e:
            print(f"等待扫码登录失败: {e}")
            continue
        if driver.current_url != login_url:
            print("扫码登录成功")
            break
        else:
            print("扫码登录失败，请重新扫码")
            time.sleep(2)


def get_movie_info_by_uid(uid, driver):
    url = f"https://movie.douban.com/subject/{uid}/"
    
    # 获取页面
    selenium_get(url, driver)
    time.sleep(2)  # 等待页面加载
    # 获取页面源代码
    html = driver.page_source
    tree = etree.HTML(html)
    uid = uid
    try:
        title = tree.xpath('//*[@id="content"]/h1/span[1]')[0].text
        # print(title)
    except:
        print("title not found")
        exit(1)
    try:
        rating = tree.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong')[0].text
        # print(rating)
    except:
        print("rating not found")
        rating = ""
        # exit(1)
    try:
        vote_num = tree.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span')[0].text
        # print(vote_num)
    except:
        print("vote_num not found")
        vote_num = ""
        # exit(1)
    try:
        stars5 = tree.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[1]/span[2]')[0].text
        # print(stars5)
    except:
        print("stars5 not found")
        stars5 = ""
        # exit(1)
    try:
        stars4 = tree.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[2]/span[2]')[0].text
        # print(stars4)
    except:
        print("stars4 not found")
        stars4 = ""
        # exit(1)
    try:
        stars3 = tree.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[3]/span[2]')[0].text
        # print(stars3)
    except:
        print("stars3 not found")
        stars3 = ""
        # exit(1)
    try:
        stars2 = tree.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[4]/span[2]')[0].text
        # print(stars2)
    except:
        print("stars2 not found")
        stars2 = ""
        # exit(1)
    try:
        stars1 = tree.xpath('//*[@id="interest_sectl"]/div[1]/div[3]/div[5]/span[2]')[0].text
        # print(stars1)
    except:
        print("stars1 not found")
        stars1 = ""
        # exit(1)
    try:
        info_list = tree.xpath('//*[@id="info"]//*')
    except:
        print("info_list not found")
        exit(1)

    director = ""
    editor = ""
    actors = ""
    genre = ""
    country = ""
    language = ""
    release_date = ""
    duration = ""
    other_name = ""
    IMDb = ""

    index = 0
    while index < len(info_list):
        if info_list[index].text == None:
            index += 1
            continue
        if info_list[index].text.find("导演") >= 0:
            index += 1
            while index < len(info_list) and info_list[index].tag != "br":
                if info_list[index].text != None:
                    if info_list[index].text.find("更多") >= 0:
                        break
                    director += info_list[index].text.strip() + "/"
                index += 1
            if director[-1] == "/":
                director = director[:-1]
        elif info_list[index].text.find("编剧") >= 0:
            index += 1
            while index < len(info_list) and info_list[index].tag != "br":
                if info_list[index].text != None:
                    if info_list[index].text.find("更多") >= 0:
                        break
                    editor += info_list[index].text.strip() + "/"
                index += 1
            if editor[-1] == "/":
                editor = editor[:-1]
        elif info_list[index].text.find("主演") >= 0:
            index += 1
            while index < len(info_list) and info_list[index].tag != "br":
                if info_list[index].text != None:
                    if info_list[index].text.find("更多") >= 0:
                        break
                    actors += info_list[index].text.strip() + "/"
                index += 1
            if actors[-1] == "/":
                actors = actors[:-1]
        elif info_list[index].text.find("类型") >= 0:
            if info_list[index].tail != None:
                genre = info_list[index].tail.strip()
            index += 1
            while index < len(info_list) and info_list[index].tag != "br":
                if info_list[index].text != None:
                    if info_list[index].text.find("更多") >= 0:
                        break
                    genre += info_list[index].text.strip() + "/"
                index += 1
            if genre[-1] == "/":
                genre = genre[:-1]
        elif info_list[index].text.find("制片国家/地区") >= 0:
            if info_list[index].tail != None:
                country = info_list[index].tail.strip()
            index += 1
            while index < len(info_list) and info_list[index].tag != "br":
                if info_list[index].text != None:
                    if info_list[index].text.find("更多") >= 0:
                        break
                    country += info_list[index].text.strip() + "/"
                index += 1
            if country[-1] == "/":
                country = country[:-1]
        elif info_list[index].text.find("语言") >= 0:
            if info_list[index].tail != None:
                language = info_list[index].tail.strip()
            index += 1
            while index < len(info_list) and info_list[index].tag != "br":
                if info_list[index].text != None:
                    if info_list[index].text.find("更多") >= 0:
                        break
                    language += info_list[index].text.strip() + "/"
                index += 1
            if language[-1] == "/":
                language = language[:-1]
        elif info_list[index].text.find("上映日期") >= 0:
            if info_list[index].tail != None:
                release_date = info_list[index].tail.strip()
            index += 1
            while index < len(info_list) and info_list[index].tag != "br":
                if info_list[index].text != None:
                    if info_list[index].text.find("更多") >= 0:
                        break
                    release_date += info_list[index].text.strip() + "/"
                index += 1
            if release_date[-1] == "/":
                release_date = release_date[:-1]
        elif info_list[index].text.find("片长") >= 0:
            if info_list[index].tail != None:
                duration = info_list[index].tail.strip()
            index += 1
            while index < len(info_list) and info_list[index].tag != "br":
                if info_list[index].text != None:
                    if info_list[index].text.find("更多") >= 0:
                        break
                    duration += info_list[index].text.strip() + "/"
                index += 1
            if duration[-1] == "/":
                duration = duration[:-1]
        elif info_list[index].text.find("又名") >= 0:
            if info_list[index].tail != None:
                other_name = info_list[index].tail.strip()
            index += 1
            while index < len(info_list) and info_list[index].tag != "br":
                if info_list[index].text != None:
                    if info_list[index].text.find("更多") >= 0:
                        break
                    other_name += info_list[index].text.strip() + "/"
                index += 1
            if other_name[-1] == "/":
                other_name = other_name[:-1]
        elif info_list[index].text.find("IMDb") >= 0:
            if info_list[index].tail != None:
                IMDb = info_list[index].tail.strip()
            index += 1
            while index < len(info_list) and info_list[index].tag != "br":
                if info_list[index].text != None:
                    if info_list[index].text.find("更多") >= 0:
                        break
                    IMDb += info_list[index].text.strip() + "/"
                index += 1
            if IMDb[-1] == "/":
                IMDb = IMDb[:-1]
        else:
            index += 1

    summary = ""
    try:
        # summary_list = tree.xpath('//*[@id="link-report-intra"]/span[1]/text()')
        hidden_summary_list = tree.xpath('//*[@id="link-report-intra"]/span[2][@class="all hidden"]/text()')
        if len(hidden_summary_list) == 0:
            raise Exception("hidden_summary_list not found")
        for i in range(len(hidden_summary_list)):
            summary += hidden_summary_list[i]
    except:
        summary_list = tree.xpath('//*[@id="link-report-intra"]/span[1]/text()')
        for i in range(len(summary_list)):
            summary += summary_list[i]

    # 检查所有元素（除简介），删去前置空格
    for attr in [title, rating, vote_num, stars5, stars4, stars3, stars2, stars1,
                 director, editor, actors, genre, country, language, release_date,
                 duration, other_name, IMDb]:
        if attr == None:
            attr = ""
            continue
        attr = attr.strip()
    # 检查简介，格式化每一行字符串，删去前置空格
    if summary == None:
        print("summary not found")
        exit(1)
    # 识别有几行
    summary_lines = summary.split("\n")
    # 格式化每一行字符串
    for i in range(len(summary_lines)):
        summary_lines[i] = summary_lines[i].strip()
    # 拼接成字符串
    summary = ""
    for i in range(len(summary_lines)):
        if summary_lines[i] == "":
            continue
        summary += summary_lines[i]
        if i != len(summary_lines) - 1:
            summary += "\n"
    # 去掉最后一个换行符
    summary = summary[:-1]
    # 创建电影对象
    movie = Movie(uid, title, rating, vote_num, stars5, stars4, stars3, stars2, stars1,
                  director, editor, actors, genre, country, language, release_date,
                  duration, other_name, IMDb, summary)
    # print(movie)
    return movie
    
def insert_movie_info_to_mysql(movie, cursor):
    # 未建表先建表
    sql = """
    CREATE TABLE IF NOT EXISTS movie_info (
        uid VARCHAR(255) PRIMARY KEY,
        title VARCHAR(255),
        rating VARCHAR(255),
        vote_num VARCHAR(255),
        stars5 VARCHAR(255),
        stars4 VARCHAR(255),
        stars3 VARCHAR(255),
        stars2 VARCHAR(255),
        stars1 VARCHAR(255),
        director TEXT,
        editor TEXT,
        actors TEXT,
        genre TEXT,
        country TEXT,
        language TEXT,
        release_date TEXT,
        duration TEXT,
        other_name TEXT,
        IMDb TEXT,
        summary TEXT
    )
    """
    try:
        cursor.execute(sql)
        connection.commit()
        print("Table created successfully")
    except pymysql.MySQLError as e:
        print(f"Failed to create table: {e}")
        connection.rollback()
        exit(1)
    # 插入数据
    sql = """
    INSERT INTO movie_info (uid, title, rating, vote_num, stars5, stars4, stars3, stars2, stars1,
    director, editor, actors, genre, country, language, release_date, duration, other_name, IMDb, summary)
    VALUES (
        %(uid)s, %(title)s, %(rating)s, %(vote_num)s, %(stars5)s, %(stars4)s, %(stars3)s, %(stars2)s, %(stars1)s,
        %(director)s, %(editor)s, %(actors)s, %(genre)s, %(country)s, %(language)s, %(release_date)s, %(duration)s,
        %(other_name)s, %(IMDb)s, %(summary)s
    )
    ON DUPLICATE KEY UPDATE
        title = VALUES(title),
        rating = VALUES(rating),
        vote_num = VALUES(vote_num),
        stars5 = VALUES(stars5),
        stars4 = VALUES(stars4),
        stars3 = VALUES(stars3),
        stars2 = VALUES(stars2),
        stars1 = VALUES(stars1),
        director = VALUES(director),
        editor = VALUES(editor),
        actors = VALUES(actors),
        genre = VALUES(genre),
        country = VALUES(country),
        language = VALUES(language),
        release_date = VALUES(release_date),
        duration = VALUES(duration),
        other_name = VALUES(other_name),
        IMDb = VALUES(IMDb),
        summary = VALUES(summary)
    """
    try:
        cursor.execute(sql, {
            'uid': movie.uid,
            'title': movie.title,
            'rating': movie.rating,
            'vote_num': movie.vote_num,
            'stars5': movie.stars5,
            'stars4': movie.stars4,
            'stars3': movie.stars3,
            'stars2': movie.stars2,
            'stars1': movie.stars1,
            'director': movie.director,
            'editor': movie.editor,
            'actors': movie.actors,
            'genre': movie.genre,
            'country': movie.country,
            'language': movie.language,
            'release_date': movie.release_date,
            'duration': movie.duration,
            'other_name': movie.other_name,
            'IMDb': movie.IMDb,
            'summary': movie.summary
        })
        connection.commit()
        print(f"Inserted/Updated movie info for UID: {movie.uid}, Title: {movie.title}")
    except pymysql.MySQLError as e:
        print(f"Failed to insert/update movie info: {e}")
        connection.rollback()
        exit(1)


if __name__ == "__main__":

    current_path = os.path.dirname(os.path.abspath(__file__))
    proxy_file = os.path.join(current_path, "./proxy.txt")
    if not os.path.exists(proxy_file):
        print(f"Proxy file not found: {proxy_file}")
        exit(1)

    # 连接到数据库
    dbconfig = {
        'host': 'localhost',
        'user': 'root',
        'password': 'asd1438com',
        'database': 'mobile_db',
        'port': 3306
    }

    try:
        connection = pymysql.connect(**dbconfig)
        print("Database connection successful")
    except pymysql.MySQLError as e:
        print(f"Database connection failed: {e}")
        exit(1)
    # 创建游标对象
    try:
        cursor = connection.cursor()
        print("Cursor created successfully")
    except pymysql.MySQLError as e:
        print(f"Failed to create cursor: {e}")
        exit(1)

    driver_path = "/usr/bin/chromedriver"  # 替换为你的 ChromeDriver 路径
    service = Service(driver_path)

    options = Options()
    options.add_argument("--headless")  # 无头模式
    options.add_argument("--disable-gpu")  # 禁用 GPU 加速
    options.add_argument("--no-sandbox")  # 解决某些环境中的权限问题
    options.add_argument("--disable-dev-shm-usage")  # 解决共享内存不足的问题
    options.add_argument("--window-size=1920x1080")  # 设置窗口大小
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--lang=zh-CN")  # 设置语言为中文

    driver = webdriver.Chrome(service=service, options=options)

    # uid_test = "26149750"
    # login_qr(driver)
    # movie = get_movie_info_by_uid(uid_test, driver)

    # 查询now_playing表中所有电影的uid，保存到列表中，重复的uid忽略
    sql_main = """
    SELECT DISTINCT movie_id FROM now_playing
    """
    try:
        cursor.execute(sql_main)
        result = cursor.fetchall()
        uid_list = []
        for row in result:
            uid_list.append(row[0])
        print(f"Fetched {len(uid_list)} unique UIDs from now_playing table")
    except pymysql.MySQLError as e:
        print(f"Failed to fetch UIDs from now_playing table: {e}")
        exit(1)

    # 登录豆瓣
    login_qr(driver)


    # 遍历uid_list，获取电影信息

    #上次失败的uid
    start_uid = ""
    sign = True

    for uid in uid_list:
        print(f"Getting movie info for UID: {uid}")
        if sign:
            if uid == start_uid:
                sign = False
                print(f"Starting from UID: {uid}")
            elif start_uid == "":
                sign = False
                print(f"Starting from UID: {uid}")
                start_uid = uid
            else:
                print(f"Skipping UID: {uid}")
                continue
        movie = get_movie_info_by_uid(uid, driver)
        if movie:
            insert_movie_info_to_mysql(movie, cursor)
        else:
            print(f"Failed to get movie info for UID: {uid}")
    # 关闭游标和连接
    cursor.close()
    connection.close()
    print("Database connection closed")
