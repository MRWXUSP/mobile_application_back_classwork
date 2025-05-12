#pragma once

#include <drogon/HttpController.h>

using namespace drogon;

namespace mobile
{
class movie : public drogon::HttpController<movie>
{
  public:
    METHOD_LIST_BEGIN
    // use METHOD_ADD to add your custom processing function here;
    // METHOD_ADD(movie::get, "/{2}/{1}", Get); // path is /mobile/movie/{arg2}/{arg1}
    // METHOD_ADD(movie::your_method_name, "/{1}/{2}/list", Get); // path is /mobile/movie/{arg1}/{arg2}/list
    // ADD_METHOD_TO(movie::your_method_name, "/absolute/path/{1}/{2}/list", Get); // path is /absolute/path/{arg1}/{arg2}/list
    // 获取当前地区所有正在上映电影
    METHOD_ADD(movie::get_now_playing, "/nowplaying/{1}", Get); // path is /mobile/movie/nowplaying/{arg1} arg1:地区
    // 获取某个电影的信息（不包括评论、图片等）
    METHOD_ADD(movie::get_movie_info, "/info/{1}", Get); // path is /mobile/movie/info/{arg1} arg1:电影ID
    // 获取某个电影的封面
    METHOD_ADD(movie::get_movie_photo, "/photo/{1}", Get); // path is /mobile/movie/photo/{arg1} arg1:电影ID

    METHOD_LIST_END
    // your declaration of processing function maybe like this:
    // void get(const HttpRequestPtr& req, std::function<void (const HttpResponsePtr &)> &&callback, int p1, std::string p2);
    // void your_method_name(const HttpRequestPtr& req, std::function<void (const HttpResponsePtr &)> &&callback, double p1, int p2) const;
    // 获取当前地区所有正在上映电影
    void get_now_playing(const HttpRequestPtr& req, std::function<void (const HttpResponsePtr &)> &&callback, const std::string& region) const;
    // 获取某个电影的信息（不包括评论、图片等）
    void get_movie_info(const HttpRequestPtr& req, std::function<void (const HttpResponsePtr &)> &&callback, const std::string& movieId) const;
    // 获取某个电影的封面
    void get_movie_photo(const HttpRequestPtr& req, std::function<void (const HttpResponsePtr &)> &&callback, const std::string& movieId) const;
};
}
