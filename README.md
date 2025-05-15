[toc]

# mobile_application_back_classwork
hnu移动应用开发课程作业后端

## 目录结构（主要）
```bash
mobile_application_back_classwork/
├── drogon_mobile/      服务器与数据库（暂定）
│   ├── build/          服务器构建目录
│   │   ├── drogon_mobile  服务器可执行文件
│   ├── controllers/    控制器，操作api主要代码
│   │   ├──filters/     过滤器
│   │   ├── models/     数据库模型
│   │   ├── plugins/    插件
│   │   ├── test/      测试
│   │   ├── views/     视图
│   ├── CMakeLists.txt  cmake配置文件
│   ├── config.json     服务器配置文件
│   ├── main.cc        服务器入口文件
├── python/          爬虫
│   ├── get_movie_by_qr.py 获取影视信息
│   ├── get_movie_photo.py 获取影视海报
│   ├── now_playing.py 获取正在上映的电影
│   ├── url_get.py 设置url
├── README.md         说明文档
```

## 部署
本服务器基于`drogon`框架构建，使用`mariaDB`作为数据库，`python`作为爬虫获取信息，**AI部分待补充**
### 安装mariaDB
```bash
sudo apt install libmariadb-dev
sudo apt install mariadb-server mariadb-client
```
### 配置mariaDB
```bash
sudo mysql_secure_installation
```
会让你进行以下操作
- 设置root密码
- 删除匿名用户
- 禁止root远程登录
- 删除测试数据库
- 刷新权限

### 创建数据库
```bash
mysql -u root -p
```
输入密码后进入数据库，执行以下命令
```sql
CREATE DATABASE mobile_db;
```

### 更改服务器配置文件
在[config.json](./drogon_mobile/config.json)中，修改以下内容：

```json
"db_clients": [
    {
        //name: Name of the client,'default' by default
        "name": "default",
        //rdbms: Server type, postgresql,mysql or sqlite3, "postgresql" by default
        "rdbms": "mysql",
        //filename: Sqlite3 db file name
        //"filename":"",
        //host: Server address,localhost by default
        "host": "127.0.0.1",
        //port: Server port, 5432 by default
        "port": 3306,
        //dbname: Database name
        "dbname": "mobile_db",
        //user: 'postgres' by default
        "user": "root",
        //passwd: '' by default
        "passwd": "asd1438com",
        //is_fast: false by default, if it is true, the client is faster but user can't call
        //any synchronous interface of it.
        "is_fast": false,
        //client_encoding: The character set used by the client. it is empty string by default which 
        //means use the default character set.
        //"client_encoding": "",
        //number_of_connections: 1 by default, if the 'is_fast' is true, the number is the number of  
        //connections per IO thread, otherwise it is the total number of all connections.  
        "number_of_connections": 1,
        //timeout: -1.0 by default, in seconds, the timeout for executing a SQL query.
        //zero or negative value means no timeout.
        "timeout": -1.0,
        //auto_batch: this feature is only available for the PostgreSQL driver(version >= 14.0), see
        //the wiki for more details.
        "auto_batch": false
        //connect_options: extra options for the connection. Only works for PostgreSQL now.
        //For more information, see https://www.postgresql.org/docs/16/libpq-connect.html#LIBPQ-CONNECT-OPTIONS
        //"connect_options": { "statement_timeout": "1s" }
    }
],
```
- `db_clients`中的`rdbms`为`mysql`
- `db_clients`中的`host`为`127.0.0.1`
- `db_clients`中的`port`为`3306`
    若你在本地运行数据库，默认端口为`3306`，如果想更改端口号，请前往[/etc/mysql/mariadb.conf.d/50-server.cnf](/etc/mysql/mariadb.conf.d/50-server.cnf)文件中修改，如需查看，请进入数据库查看
    ```bash
    mysql -u root -p
    <password>
    SHOW VARIABLES LIKE 'port';
    ```
    你将会看到类似的输出：
    ```sql
    +---------------+-------+
    | Variable_name | Value |
    +---------------+-------+
    | port          | 3306  |
    +---------------+-------+
    ```
- `db_clients`中的`dbname`为`mobile_db`
- `db_clients`中的`user`为`root`
- `db_clients`中的`passwd`为你在安装数据库时设置的密码




### 安装drogon
请参考`drogon`官方文档：[Drogon](https://drogonframework.github.io/drogon-docs/#/CHN/CHN-02-%E5%AE%89%E8%A3%85?id=%e7%b3%bb%e7%bb%9f%e8%a6%81%e6%b1%82)

## 构建服务器
进入`drogon_mobile/build`目录，执行以下命令
```bash
cmake ..
make
```
## 运行
执行以下命令（在`drogon_mobile/build`目录下）
```bash
./drogon_mobile
```

<!---

/*

now_playing 表结构
+----------+--------------+------+-----+---------+-------+
| Field    | Type         | Null | Key | Default | Extra |
+----------+--------------+------+-----+---------+-------+
| movie_id | varchar(255) | NO   | PRI | NULL    |       |
| location | varchar(255) | NO   | PRI | NULL    |       |
+----------+--------------+------+-----+---------+-------+

movie_info 表结构
+--------------+--------------+------+-----+---------+-------+
| Field        | Type         | Null | Key | Default | Extra |
+--------------+--------------+------+-----+---------+-------+
| uid          | varchar(255) | NO   | PRI | NULL    |       |
| title        | varchar(255) | YES  |     | NULL    |       |
| rating       | varchar(255) | YES  |     | NULL    |       |
| vote_num     | varchar(255) | YES  |     | NULL    |       |
| stars5       | varchar(255) | YES  |     | NULL    |       |
| stars4       | varchar(255) | YES  |     | NULL    |       |
| stars3       | varchar(255) | YES  |     | NULL    |       |
| stars2       | varchar(255) | YES  |     | NULL    |       |
| stars1       | varchar(255) | YES  |     | NULL    |       |
| director     | text         | YES  |     | NULL    |       |
| editor       | text         | YES  |     | NULL    |       |
| actors       | text         | YES  |     | NULL    |       |
| genre        | text         | YES  |     | NULL    |       |
| country      | text         | YES  |     | NULL    |       |
| language     | text         | YES  |     | NULL    |       |
| release_date | text         | YES  |     | NULL    |       |
| duration     | text         | YES  |     | NULL    |       |
| other_name   | text         | YES  |     | NULL    |       |
| IMDb         | text         | YES  |     | NULL    |       |
| summary      | text         | YES  |     | NULL    |       |
+--------------+--------------+------+-----+---------+-------+
*/

-->

## api
服务器ip：47.121.24.255
- `/`
    - GET
    - 返回`<text>:"server is running"`
- `/mobile/movie/nowplaying/{arg1}`
    - GET
    - 参数`arg1`为用户所在地区位置的拼音，如`beijing`
    - 返回`<json>:[{"movie_id":"<movie_id>"}]`
    - 错误返回`<json>:[{"error":"<error_info>"}]`
    - 其中`<movie_id>`为电影id
- `/mobile/movie/info/{arg1}`
    - GET
    - 参数`arg1`为电影id
    - 返回json格式
        ```json
        [
            {
                "movie_id":"<movie_id>",
                "title":"<title>",
                "rating":"<rating>","vote_num":"<vote_num>",
                "stars5":"<stars5>",
                "stars4":"<stars4>",
                "stars3":"<stars3>",
                "stars2":"<stars2>",
                "stars1":"<stars1>",
                "director":"<director>",
                "editor":"<editor>",
                "actors":"<actors>",
                "genre":"<genre>",
                "country":"<country>",
                "language":"<language>",
                "release_date":"<release_date>",
                "duration":"<duration>",
                "other_name":"<other_name>",
                "IMDb":"<IMDb>",
                "summary":"<summary>"
            },
            ...
        ]
        ```
    - 错误返回`<json>:[{"error":"<error_info>"}]`
    - 其中`<movie_id>`为电影id，`<title>`为电影标题，`<rating>`为电影评分，`<vote_num>`为电影评分人数，`<stars5>`为5星人数，`<stars4>`为4星人数，`<stars3>`为3星人数，`<stars2>`为2星人数，`<stars1>`为1星人数，`<director>`为导演，`<editor>`为编剧，`<actors>`为演员，`<genre>`为类型，`<country>`为国家，`<language>`为语言，`<release_date>`为上映日期，`<duration>`为时长，`<other_name>`为其他名称，`<IMDb>`为IMDb链接，`<summary>`为简介
- `/mobile/movie/photo/{arg1}`
    - GET
    - 参数`arg1`为电影id
    - 返回`<jpg>:<file>`
    - 错误返回`<json>:[{"error":"<error_info>"}]`
    - 其中`<file>`为电影海报文件
- `/mobile/movie/recommend/{arg1}`
    - GET
    - 参数`arg1`为用户id，有一初始用户id为`"123456"`
    - 返回json格式
        ```json
        {
            "uid": <uid>,
            "like_movie":[<movie_name>,...],
            "like_type":[<type_name>,...],
            "recommend_movies":[
                {
                    "movie_id": <movie_id>,
                    "movie_name": <movie_name>,
                    "ai_rating": <rating>,
                    "reason_good": <reason_good>,
                    "reason_bad": <reason_bad>,
                    "recommendation_score": <recommendation_score>,
                    "douban_rating": <douban_rating>
                },
                ...
            ]
        }
        ```
    - 错误返回`<json>:[{"error":"<error_info>"}]`
    - 其中`<uid>`为用户id，`<like_movie>`为用户喜欢的电影，`<like_type>`为用户喜欢的类型，`<movie_id>`为电影id，`<movie_name>`为电影名称，`<ai_rating>`为AI为电影评的分数，`<reason_good>`为推荐理由，`<reason_bad>`为不推荐理由，`<recommendation_score>`为推荐分数，`<douban_rating>`为豆瓣评分
- `/mobile/check/check_user/{arg1}`
    - GET
    - 参数`arg1`为用户id
    - 返回`<text>:"check_user: <arg1> is OK`
    - 错误返回`<text>:"check_user: <arg1> is not OK"`
    - 其中`<arg1>`为用户id


## 爬虫

爬虫部分使用`python`编写，主要用于获取电影信息和海报

不具体描述爬虫实现和使用，~~以免遭受不必要的问询~~