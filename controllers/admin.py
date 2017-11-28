import tornado
from tornado.web import RequestHandler
import tornado.web
import os
import json
from models.blog import Blog, Article, UserInfo
from utils.pagination import Page

class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username", None)


class LoginHandler(BaseHandler):
    def get(self):
        self.render('admin/login.html')

    def post(self):
        ret = {'status': 'false', 'message': ''}
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        try:
            user_obj = UserInfo.get(UserInfo.username == username, UserInfo.password == password)
            if user_obj:
                self.set_secure_cookie("username", username)
                ret['status'] = 'true'
            else:
                ret['message'] = '用户名或密码错误'
        except Exception as e:
            print(e)
            ret['message'] = '服务器开小差了'
        return self.write(json.dumps(ret))


class LogoutHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.clear_cookie("username")
        self.redirect("/index")




class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        current_page = self.get_argument("p", 1)
        current_page = int(current_page)
        data_count = Article.select().count()
        page_obj = Page(current_page=current_page, data_count=data_count)
        if current_page == 1:
            articles = Article.select()[-page_obj.end:]
        else:
            articles = Article.select()[-page_obj.end:-page_obj.start]
        at_list = []
        for a in articles:
            at_list.append({'id': a.id,
                            'title': a.title,
                            'read_count': a.read_count,
                            'created_date': a.created_date,
                            'article_type': a.type_choices[a.article_type - 1][1]
                            })
        at_list.reverse()
        page_html = page_obj.page_str(base_url="/admin/index?")
        self.render('admin/index.html', at_list=at_list, page_html=page_html)

    # def post(self):
    #     ret = {'status': 'true', 'message': '', 'data': ''}
    #     file_md5 = self.get_argument("file_md5", None)
    #     file_name = self.get_argument("file_name", None)
    #     if file_md5 and file_name:
    #         f_obj = Files().select().where(Files.md5 == file_md5).first()
    #         f_path = os.path.join(DOWNLOAD_DIR, file_name)
    #         if f_obj:
    #             try:
    #                 Files.delete().where(Files.md5 == file_md5).execute()
    #                 os.remove(f_path)
    #                 ret['message'] = '删除成功'
    #             except Exception as e:
    #                 print(e)
    #                 ret['status'] = 'false'
    #                 ret['message'] = '删除失败'
    #     else:
    #         ret['status'] = 'false'
    #         ret['message'] = '所删文件不存在'
    #     self.write(json.dumps(ret))
#
#
# class UploadFileNginxHandle(BaseHandler):
#     @tornado.web.authenticated
#     def post(self, *args, **kwargs):
#         ret = {'status': 'true', 'message': '', 'data': ''}
#         file_name = self.get_argument("file_name", None)
#         tmp_path = self.get_argument("tmp_path", None)
#         md5 = self.get_argument("md5", None)
#         size = self.get_argument("size", None)
#         if file_name and tmp_path and md5 and size:
#             file_path = os.path.join(DOWNLOAD_DIR, file_name)
#             os.rename(tmp_path, file_path)
#             file_obj = Files()
#             file_obj.file_name = file_name
#             file_obj.md5 = md5
#             file_obj.path = tmp_path
#             file_obj.size = size
#             file_obj.save()
#             ret['data'] = {'name': file_name, 'size': size, 'path': file_path, 'md5': md5}
#         ret['status'] = 'false'
#         self.write(json.dumps(ret))
#
#
# class AdminHandle(tornado.web.RequestHandler):
#     def get(self):
#         user_list = []
#         objs = User.select()
#         for obj in objs:
#             user_list.append([obj.username, obj.password, obj.created_date])
#         self.render('index/admin.html', user_list=user_list, username='admin')
#
#     def post(self, *args, **kwargs):
#         ret = {'status': 'ture', 'message': '', 'data': ''}
#         username = self.get_argument('username', None)
#         password = self.get_argument('password', None)
#         if username and password:
#             user_obj = User()
#             user_obj.username = username
#             user_obj.password = password
#             try:
#                 user_obj.save()
#                 ret['message'] = '用户添加成功'
#             except Exception as e:
#                 print(e)
#                 ret['status'] = 'false'
#                 ret['message'] = '添加失败，此用户已经存在或者其他问题'
#         else:
#             ret['status'] = 'false'
#             ret['message'] = '用户名或者密码没有填写'
#         return self.write(json.dumps(ret))
#
#     def delete(self, *args, **kwargs):
#         ret = {'status': 'ture', 'message': '', 'data': ''}
#         username = self.get_argument('username', None)
#         if username:
#             if User.delete().where(User.username == username).execute():
#                 return self.write(json.dumps(ret))
#             else:
#                 ret['status'] = 'false'
#                 ret['message'] = '删除失败'
#         else:
#             ret['status'] = 'false'
#             ret['message'] = '没有用户'
#         return self.write(json.dumps(ret))
