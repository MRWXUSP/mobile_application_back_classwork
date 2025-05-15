#pragma once

#include <drogon/HttpController.h>

using namespace drogon;

namespace mobile
{
class check : public drogon::HttpController<check>
{
  public:
    METHOD_LIST_BEGIN
    // use METHOD_ADD to add your custom processing function here;
    // METHOD_ADD(check::get, "/{2}/{1}", Get); // path is /mobile/check/{arg2}/{arg1}
    // METHOD_ADD(check::your_method_name, "/{1}/{2}/list", Get); // path is /mobile/check/{arg1}/{arg2}/list
    // ADD_METHOD_TO(check::your_method_name, "/absolute/path/{1}/{2}/list", Get); // path is /absolute/path/{arg1}/{arg2}/list

    // 检验
    METHOD_ADD(check::check_user, "/check_user/{1}", Get); // path is /mobile/check/check_user/{arg1} arg1:用户ID
    METHOD_LIST_END
    // your declaration of processing function maybe like this:
    // void get(const HttpRequestPtr& req, std::function<void (const HttpResponsePtr &)> &&callback, int p1, std::string p2);
    // void your_method_name(const HttpRequestPtr& req, std::function<void (const HttpResponsePtr &)> &&callback, double p1, int p2) const;
    void check_user(const HttpRequestPtr& req, std::function<void (const HttpResponsePtr &)> &&callback, const std::string& userId) const;
};
}
