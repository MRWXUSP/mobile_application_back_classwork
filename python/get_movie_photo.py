import os
import time
import pymysql
import requests
from lxml import etree
from url_get import selenium_get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from get_movie_by_qr import login_qr

def get_movie_photo(movie_id, driver, photo_floder):
    """
    获取电影的封面图片
    :param movie_id: 电影ID
    :param driver: Selenium WebDriver实例
    :return: 图片URL
    """
    # 构造豆瓣电影详情页的URL
    url = f"https://movie.douban.com/subject/{movie_id}/"
    
    # 使用Selenium获取页面源代码
    page_source = selenium_get(url, driver)
    
    if page_source is None:
        print(f"无法获取电影页面: {url}")
        return None
    
    # 解析页面源代码
    tree = etree.HTML(page_source)
    
    # 提取图片URL
    try:
        image = tree.xpath('//*[@id="mainpic"]/a/img')
    except Exception as e:
        print(f"解析图片URL失败: {e}")
        return None
    if not image:
        print("没有找到图片元素")
        return None
    try:
        image_url = image[0].get("src")
    except Exception as e:
        print(f"获取图片URL失败: {e}")
        return None
    if not image_url:
        print("没有找到图片URL")
        return None
    # 下载图片
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            # 创建图片文件夹
            if not os.path.exists(photo_floder):
                os.makedirs(photo_floder)
            # 保存图片
            image_path = os.path.join(photo_floder, f"{movie_id}.jpg")
            with open(image_path, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"图片已保存: {image_path}")
        else:
            print(f"下载图片失败: {response.status_code}")
    except Exception as e:
        print(f"下载图片异常: {e}")
        return None
    
if __name__ == "__main__":

    current_path = os.path.dirname(os.path.abspath(__file__))
    photo_floder = os.path.join(current_path, "../datas/movies/photos/")

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

    login_qr(driver)

    # 获取电影ID列表
    sql = "SELECT uid FROM movie_info;"
    try:
        cursor.execute(sql)
        movie_ids = cursor.fetchall()
        print("Movie IDs fetched successfully")
    except pymysql.MySQLError as e:
        print(f"Failed to fetch movie IDs: {e}")
        exit(1)
    # 遍历电影ID列表
    for movie_id in movie_ids:
        movie_id = movie_id[0]
        print(f"Processing movie ID: {movie_id}")
        get_movie_photo(movie_id, driver, photo_floder)
    # 关闭数据库连接
    cursor.close()
    connection.close()
    driver.quit()
    print("Database connection closed")
    print("Selenium driver closed")
    print("Script completed successfully")
            