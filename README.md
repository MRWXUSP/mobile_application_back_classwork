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
├── README.md         说明文档
```

## 部署
本服务器基于`drogon`框架构建，使用`mariaDB`作为数据库，**爬虫与AI部分待补充**
### 安装mariaDB
```bash
sudo apt install libmariadb-dev
```
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
## api
- `/`
    - GET
    - 返回`<text>:"server is running"`