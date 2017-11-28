#!/usr/bin/env python3

import tornado.ioloop
import tornado.web
from controllers import index
from controllers import admin

settings = {
    'template_path': 'template',
    'static_path': 'static',
    'static_url_prefix': '/static/',
    'cookie_secret': '43809138f51b96f8ac24e79b3a2cb482',
    'login_url': '/login',
    #'xsrf_cookies': True,
    'debug': True,
    'autoreload': True,
}

application = tornado.web.Application([
    # 主页
    (r"/index", index.IndexHandler),
    # 文章页
    (r"/article/([\d]+).html", index.ArticleHandler),
    # 查询
    (r"/search", index.SearchHandler),
    # # Admin
    # (r"/admin", admin.LoginHandler),
    # # 登录
    # (r"/login", admin.LoginHandler),
    # # 登出
    # (r"/logout", admin.LogoutHandler),
    # # 上传
    # (r"/upload", index.UploadFileNginxHandle),
], **settings)

if __name__ == '__main__':
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
