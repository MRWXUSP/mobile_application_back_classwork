# 此脚本用于将 "datas/movies/recommend"中的推荐json数据导入到数据库中
# json格式
'''
{
    "uid": <uid>,
    "like_movie":[<movie_name>,...],
    "like_type":[<type_name>,...],
    "recommend_movies":[
        {
            "movie_id": <movie_id>,
            "movie_name": <movie_name>,
            "rating": <rating>,
            "reason_good": <reason_good>,
            "reason_bad": <reason_bad>,
            "recommendation_score": <recommendation_score>
        },
        ...
    ]
}
'''

import os
import json
import pymysql

# 将json文件插入数据库
'''
数据库表结构
recommend_movies
uid VARCHAR(255) PRIMARY KEY,
user_json JSON
'''
def insert_json_to_db(json_file, cursor):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        uid = data['uid']
        user_json = json.dumps(data, ensure_ascii=False)
        # 如果没有表则创建表
        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS recommend_movies (
                    uid VARCHAR(255) PRIMARY KEY,
                    user_json JSON
                )
            ''')
        except pymysql.MySQLError as e:
            print(f"Error creating table: {e}")
            return
        # 插入数据
        try:
            cursor.execute('''
                INSERT INTO recommend_movies (uid, user_json)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE user_json = VALUES(user_json)
            ''', (uid, user_json))
        except pymysql.MySQLError as e:
            print(f"Error inserting data: {e}")
            return
        print(f"Inserted data for user {uid} into database.")


if __name__ == '__main__':
    # 数据库连接信息
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'asd1438com',
        'database': 'mobile_db',
        'charset': 'utf8mb4'
    }
    # 连接数据库
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
    except pymysql.MySQLError as e:
        print(f"Error connecting to database: {e}")
        exit(1)
    # 获取当前目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # 获取推荐json文件夹路径
    recommend_dir = os.path.join(current_dir, '../datas/movies/recommend')
    # 遍历文件夹中的所有json文件
    for filename in os.listdir(recommend_dir):
        if filename.endswith('.json'):
            json_file = os.path.join(recommend_dir, filename)
            try:
                # 插入json数据到数据库
                insert_json_to_db(json_file, cursor)
            except Exception as e:
                print(f"Error processing file {filename}: {e}")
                continue
    # 提交事务
    try:
        connection.commit()
    except pymysql.MySQLError as e:
        print(f"Error committing transaction: {e}")
    else:
        print("All data inserted successfully.")
    # 关闭游标和连接
    finally:
        try:
            cursor.close()
            connection.close()
        except pymysql.MySQLError as e:
            print(f"Error closing connection: {e}")
        else:
            print("Database connection closed.")