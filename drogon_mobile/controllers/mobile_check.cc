#include "mobile_check.h"
#include <thread>
#include <chrono>
#include <drogon/drogon.h>

using namespace mobile;

// Add definition of your processing function here
void check::check_user(const HttpRequestPtr& req, std::function<void (const HttpResponsePtr &)> &&callback, const std::string& userId) const
{
    std::this_thread::sleep_for(std::chrono::seconds(5)); // 模拟延迟5秒
    // 暂未实现
    auto resp = drogon::HttpResponse::newHttpResponse();
    resp->setStatusCode(k200OK);
    resp->setContentTypeCode(CT_TEXT_PLAIN);
    resp->setBody("check_user: " + userId + " is OK");
    callback(resp);
}
