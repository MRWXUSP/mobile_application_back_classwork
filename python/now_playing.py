# -*- coding: utf-8 -*-
# 此脚本可以获取当前地区正在上映的电影的ID，需要以地区为参数运行，或者直接获取全部

from multiprocessing import connection
import requests
from lxml import etree
import os
from url_get import get_and_sleep
import argparse
import pymysql

def refresh_now_playing(cursor):
    # 删除表
    sql = "DELETE FROM now_playing"
    try:
        cursor.execute(sql)
        connection.commit()
        print("Refreshed now_playing table")
        return True
    except pymysql.MySQLError as e:
        print(f"Failed to refresh now_playing table: {e}")
        connection.rollback()
        return False

def insert_now_playing(cursor, location:str, id:str):
    # 若未创建表，则创建表
    cursor.execute("CREATE TABLE IF NOT EXISTS now_playing (movie_id VARCHAR(255), location VARCHAR(255), PRIMARY KEY (movie_id, location))")
    # 插入数据
    sql = "INSERT IGNORE INTO now_playing (movie_id, location) VALUES (%s, %s)"
    try:
        cursor.execute(sql, (id, location))
        connection.commit()
        print(f"Inserted movie ID: {id} for location: {location}")
    except pymysql.MySQLError as e:
        print(f"Failed to insert data: {e}")
        connection.rollback()

def get_all_area(url, headers, proxy_file):
    with open(proxy_file, "r") as f:
        proxies = f.readlines()
    # 读取代理文件
    proxies = [proxy.strip() for proxy in proxies]
    for proxy in proxies:
        proxies_dict = {
            "http": f"http://{proxy}"
        }
        try:
            response = get_and_sleep(url, headers, proxies_dict)
            if response.status_code == 200:
                html = etree.HTML(response.text)
                area =[]
                location = html.xpath('//*[@id="cities-list"]/div[2]/div[@class="cities-list-item"]')
                for loc in location:
                    span = loc.xpath('./dl/dd/span')
                    for s in span:
                        area.append(s.xpath('./a/@uid')[0])
                return area
            else:
                print(f"Error: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        

def get_location_now_playing(url, headers, proxy_file, location, cursor):
    with open(proxy_file, "r") as f:
        proxies = f.readlines()
    # 读取代理文件
    proxies = [proxy.strip() for proxy in proxies]
    for proxy in proxies:
        proxies_dict = {
            "http": f"http://{proxy}"
        }
        try:
            response = get_and_sleep(url, headers, proxies_dict)
            print(f"Proxy: {proxies_dict} - Status Code: {response.status_code}")
            if response.status_code == 200:
                html = etree.HTML(response.text)
                lists = html.xpath('//*[@id="nowplaying"]/div[2]/ul/li')
                for list in lists:
                    name = list.xpath('./ul/li[2]/a/@href')[0]
                    #查找'subject/'的位置
                    index_start = name.find('subject/')
                    index_end = name.find('/?', index_start) 
                    #截取字符串
                    id = name[index_start + len('subject/'):index_end]
                    insert_now_playing(cursor, location, id)
                break
            else:
                print(f"Proxy: {proxies_dict} - Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Proxy: {proxies_dict} - Error: {e}")

if __name__ == "__main__":

    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Get the current playing movies in a specific area or all area.")
    parser.add_argument("--area", type=str, nargs="?",default="changsha",help="Get the current playing movies in a specific area.")
    parser.add_argument("--all", action="store_true", help="Get all areas.")
    parser.add_argument("--refresh", action="store_true", help="Refresh the database.")
    args = parser.parse_args()

    dbconfig = {
        'host': 'localhost',
        'user': 'root',
        'password': 'asd1438com',
        'database': 'mobile_db',
        'port': 3306
    }

    # 连接数据库

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


    url=f"https://movie.douban.com/cinema/nowplaying/{args.area}/"

    current_dir = os.path.dirname(os.path.abspath(__file__))
    proxy_file = os.path.join(current_dir, "proxy.txt")
    if not os.path.exists(proxy_file):
        print (f"Proxy file not found: {proxy_file}")
        exit(1)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
    }

    if args.refresh:
        # 刷新数据库
        if refresh_now_playing(cursor):
            print("Database refreshed successfully")
        else:
            print("Failed to refresh database")
            exit(1)

    if args.all:
        # 获取所有地区
        area = get_all_area(url, headers, proxy_file)
        if not area:
            print("Failed to get all areas.")
            exit(1)
        for area_id in area:
            url = f"https://movie.douban.com/cinema/nowplaying/{area_id}/"
            print(f"Getting movies in area: {area_id}")
            get_location_now_playing(url, headers, proxy_file, area_id, cursor)
    else:
        # 获取指定地区
        print(f"Getting movies in area: {args.area}")
        get_location_now_playing(url, headers, proxy_file, args.area, cursor)

    # 关闭数据库连接
    try:
        connection.close()
        print("Database connection closed")
    except pymysql.MySQLError as e:
        print(f"Failed to close database connection: {e}")
        exit(1)

