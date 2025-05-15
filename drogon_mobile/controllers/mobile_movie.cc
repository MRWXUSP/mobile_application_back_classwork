#include "mobile_movie.h"
#include <drogon/orm/DbClient.h>
#include <drogon/drogon.h>
#include <json/json.h>
#include <fstream>
#include <unistd.h> // for getcwd
#include <limits.h> // for PATH_MAX
#include <thread>
#include <chrono>

using namespace mobile;

// Add definition of your processing function here

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

recommend_movies 表结构
+-----------+--------------+------+-----+---------+-------+
| Field     | Type         | Null | Key | Default | Extra |
+-----------+--------------+------+-----+---------+-------+
| uid       | varchar(255) | NO   | PRI | NULL    |       |
| user_json | longtext     | YES  |     | NULL    |       |
+-----------+--------------+------+-----+---------+-------+
其中user_json结构如：
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

*/

// 获取当前地区所有正在上映电影
void movie::get_now_playing(const HttpRequestPtr& req, std::function<void (const HttpResponsePtr &)> &&callback, const std::string& region) const
{
    // 1. 获取数据库连接
    auto dbClient = drogon::app().getDbClient("default");
    // 2. 构建SQL语句
    std::string sql = "SELECT * FROM now_playing WHERE location = ?";
    // 3. 执行SQL语句
    dbClient->execSqlAsync(
        sql,
        [callback](const drogon::orm::Result &r) {
            // 4. 处理结果
            Json::Value json;
            for (const auto &row : r) {
                Json::Value movie;
                movie["movie_id"] = row["movie_id"].as<std::string>();
                json.append(movie);
            }
            auto resp = drogon::HttpResponse::newHttpJsonResponse(json);
            callback(resp);
        },
        [callback](const drogon::orm::DrogonDbException &e) {
            // 5. 处理错误
            Json::Value json;
            json["error"] = e.base().what();
            auto resp = drogon::HttpResponse::newHttpJsonResponse(json);
            callback(resp);
        },
        region);
}
// 获取某个电影的信息（不包括评论、图片等）
void movie::get_movie_info(const HttpRequestPtr& req, std::function<void (const HttpResponsePtr &)> &&callback, const std::string& movieId) const
{
    // 1. 获取数据库连接
    auto dbClient = drogon::app().getDbClient("default");
    // 2. 构建SQL语句
    std::string sql = "SELECT * FROM movie_info WHERE uid = ?";
    // 3. 执行SQL语句
    dbClient->execSqlAsync(
        sql,
        [callback](const drogon::orm::Result &r) {
            // 4. 处理结果
            Json::Value json;
            if (r.size() > 0) {
                const auto &row = r[0];
                json["movie_id"] = row["uid"].as<std::string>();
                json["title"] = row["title"].as<std::string>();
                json["rating"] = row["rating"].as<std::string>();
                json["vote_num"] = row["vote_num"].as<std::string>();
                json["stars5"] = row["stars5"].as<std::string>();
                json["stars4"] = row["stars4"].as<std::string>();
                json["stars3"] = row["stars3"].as<std::string>();
                json["stars2"] = row["stars2"].as<std::string>();
                json["stars1"] = row["stars1"].as<std::string>();
                json["director"] = row["director"].as<std::string>();
                json["editor"] = row["editor"].as<std::string>();
                json["actors"] = row["actors"].as<std::string>();
                json["genre"] = row["genre"].as<std::string>();
                json["country"] = row["country"].as<std::string>();
                json["language"] = row["language"].as<std::string>();
                json["release_date"] = row["release_date"].as<std::string>();
                json["duration"] = row["duration"].as<std::string>();
                json["other_name"] = row["other_name"].as<std::string>();
                json["IMDb"] = row["IMDb"].as<std::string>();
                json["summary"] = row["summary"].as<std::string>();
            }
            auto resp = drogon::HttpResponse::newHttpJsonResponse(json);
            callback(resp);
        },
        [callback](const drogon::orm::DrogonDbException &e) {
            // 5. 处理错误
            Json::Value json;
            json["error"] = e.base().what();
            auto resp = drogon::HttpResponse::newHttpJsonResponse(json);
            callback(resp);
        },
        movieId);
}

// 获取某个电影的封面
void movie::get_movie_photo(const HttpRequestPtr& req, std::function<void (const HttpResponsePtr &)> &&callback, const std::string& movieId) const
{
    //检查id是否为数字
    if (!std::all_of(movieId.begin(), movieId.end(), ::isdigit)) {
        Json::Value json;
        json["error"] = "movieId must be a number";
        auto resp = drogon::HttpResponse::newHttpJsonResponse(json);
        callback(resp);
        return;
    }
    // 构建路径
    char cwd[PATH_MAX];
    if (getcwd(cwd, sizeof(cwd)) != nullptr) {
        // debug
        printf("Current working dir: %s\n", cwd);
        std::string path = std::string(cwd) + "/../../datas/movies/photos/" + movieId + ".jpg";
        // 检查文件是否存在
        std::ifstream file(path);
        if (file.good()) {
            // 文件存在，读取文件内容
            file.close();
            auto resp = drogon::HttpResponse::newFileResponse(path);
            resp->setContentTypeCode(drogon::CT_IMAGE_JPG);
            callback(resp);
        } else {
            // 文件不存在，返回404
            file.close();
            Json::Value json;
            json["error"] = "file not found";
            auto resp = drogon::HttpResponse::newHttpJsonResponse(json);
            callback(resp);
        }
    } else {
        // 获取当前工作目录失败，返回500
        Json::Value json;
        json["error"] = "getcwd failed";
        auto resp = drogon::HttpResponse::newHttpJsonResponse(json);
        callback(resp);
    }
}

/*
返回的json在原来的基础上加入豆瓣评分
原来json结构如：
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
返回的json结构如：
'''
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
'''
*/

// 获取某个用户的推荐电影
void movie::get_user_recommendations(const HttpRequestPtr& req, std::function<void (const HttpResponsePtr &)> &&callback, const std::string& userId) const
{   
    std::this_thread::sleep_for(std::chrono::seconds(5));
    auto dbClient = drogon::app().getDbClient("default");
    std::string sql = "SELECT * FROM recommend_movies WHERE uid = ?";
    try{
        auto result = dbClient->execSqlAsyncFuture(sql, userId).get();
        // auto result = dbClient->execSqlSync(sql, userId);
        Json::Value json;
        if (result.size() > 0) {
            const auto &row = result[0];
            std::string user_json = row["user_json"].as<std::string>();
            Json::CharReaderBuilder reader;
            Json::Value user_data;
            std::istringstream s(user_json);
            std::string errs;
            if (Json::parseFromStream(reader, s, &user_data, &errs)) {
                // 解析成功
                json["uid"] = user_data["uid"];
                json["like_movie"] = user_data["like_movie"];
                json["like_type"] = user_data["like_type"];
                for (const auto &movie : user_data["recommend_movies"]) {
                    Json::Value movie_info;
                    movie_info["movie_id"] = movie["movie_id"];
                    movie_info["movie_name"] = movie["movie_name"];
                    movie_info["ai_rating"] = movie["rating"];
                    movie_info["reason_good"] = movie["reason_good"];
                    movie_info["reason_bad"] = movie["reason_bad"];
                    movie_info["recommendation_score"] = movie["recommendation_score"];

                    // 获取豆瓣评分
                    std::string sql2 = "SELECT rating FROM movie_info WHERE uid = ?";
                    auto result2 = dbClient->execSqlSync(sql2, movie["movie_id"].as<std::string>());
                    if (result2.size() > 0) {
                        const auto &row2 = result2[0];
                        movie_info["douban_rating"] = row2["rating"].as<std::string>();
                    } else {
                        movie_info["douban_rating"] = "N/A";
                    }
                    json["recommend_movies"].append(movie_info);
                }
            } else {
                // 解析失败
                json["error"] = "Failed to parse JSON";
            }
        } else {
            // 没有找到推荐电影
            json["error"] = "No recommendations found";
        }
        auto resp = drogon::HttpResponse::newHttpJsonResponse(json);
        callback(resp);
    }
    catch (const drogon::orm::DrogonDbException &e) {
        // 处理错误
        Json::Value json;
        json["error"] = e.base().what();
        auto resp = drogon::HttpResponse::newHttpJsonResponse(json);
        callback(resp);
        return;
    }
    catch (const std::exception &e) {
        // 处理其他错误
        Json::Value json;
        json["error"] = e.what();
        auto resp = drogon::HttpResponse::newHttpJsonResponse(json);
        callback(resp);
        return;
    }
    catch (...) {
        // 处理未知错误
        Json::Value json;
        json["error"] = "Unknown error";
        auto resp = drogon::HttpResponse::newHttpJsonResponse(json);
        callback(resp);
        return;
    }
}
    