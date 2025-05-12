#include "mobile_movie.h"
#include <drogon/orm/DbClient.h>
#include <drogon/drogon.h>
#include <json/json.h>
#include <fstream>
#include <unistd.h> // for getcwd
#include <limits.h> // for PATH_MAX

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
    