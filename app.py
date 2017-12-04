#!/usr/bin/env python3
import tornado.ioloop
import tornado.web
from controllers import index
from controllers import admin
from controllers import uimethods as umt

settings = {
    'template_path': 'template',
    'static_path': 'static',
    'static_url_prefix': '/static/',
    'cookie_secret': '43809138f51b96f8ac24e79b3a2cb482',
    'login_url': '/admin/login',
    'xsrf_cookies': True,
    'debug': True,
    'autoreload': True,
    'ui_methods': umt,
}

application = tornado.web.Application([
    # 主页
    (r"/index", index.IndexHandler),
    # 文章页
    (r"/article/([\d]+).html", index.ArticleHandler),
    # 查询
    (r"/search", index.SearchHandler),
    # 关于
    (r"/about", index.AboutHandler),
    # 登录
    (r"/admin/login", admin.LoginHandler),
    # 主页
    (r"/admin/index", admin.IndexHandler),
    # 登出
    (r"/admin/logout", admin.LogoutHandler),
    # 上传图片
    (r"/upload", admin.UploadHandler),
    # 文章页
    (r"/tag/([\w]+)", index.TagsHandler),
    # 404处理页面
    (r"/404", index.NotfindHandler),
    (r".*", index.NotfindHandler),
], **settings)

if __name__ == '__main__':
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
