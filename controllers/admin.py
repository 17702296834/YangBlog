import tornado
from tornado.web import RequestHandler
import tornado.web
import datetime
import json
from models.blog import Blog, Article, UserInfo, ArticleType
from utils.pagination import Page
from utils.log import Logger


class BaseHandler(RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username", None)


class LoginHandler(BaseHandler):
    def get(self):
        self.render('admin/login.html')

    def post(self):
        ret = {'status': 'false', 'message': '', 'data': ''}
        username = self.get_argument("username", None)
        password = self.get_argument("password", None)
        try:
            user_obj = UserInfo.get(UserInfo.username == username, UserInfo.password == password)
            if user_obj:
                self.set_secure_cookie("username", username)
                ret['status'] = 'true'
        except UserInfo.DoesNotExist as e:
            Logger().log(e, True)
            ret['message'] = '用户名或密码错误'
        except Exception as e:
            Logger().log(e, True)
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
        page_obj = Page(current_page=current_page, data_count=data_count, per_page_count=15)
        page_html = page_obj.page_str(base_url="/admin/index?")
        at_list = []
        article_types = []
        try:
            if current_page == 1:
                articles = Article.select()[-page_obj.end:]
            else:
                articles = Article.select()[-page_obj.end:-page_obj.start]
            for a in articles:
                at_list.append({'id': a.id,
                                'title': a.title,
                                'read_count': a.read_count,
                                'summary': a.summary,
                                'content': a.content,
                                'created_date': a.created_date,
                                'article_type_id': a.article_type_id,
                                'article_type': a.article_type.article_type
                                })
            at_list.reverse()
            article_type_objs = ArticleType.select()
            for article_type_obj in article_type_objs:
                article_types.append({'id': article_type_obj.id, 'article_type': article_type_obj.article_type})
        except Exception as e:
            Logger().log(e, True)
            return self.render('index/500.html')
        self.render('admin/index.html', at_list=at_list, page_html=page_html, article_types=article_types)

    def post(self, *args, **kwargs):
        ret = {'status': 'false', 'message': '', 'data': ''}
        article_id = self.get_argument('article_id', None)
        title = self.get_argument('title', None)
        article_type = self.get_argument('article_type', None)
        summary = self.get_argument('summary', None)
        content = self.get_argument('content', None)
        action = self.get_argument('action', None)
        if article_id and title and article_type and summary and content and action:
            if action == 'post':
                try:
                    article_obj = Article(title=title)
                    article_obj.article_type_id = article_type
                    article_obj.summary = summary
                    article_obj.content = content
                    article_obj.save()
                    ret['status'] = 'true'
                    ret['message'] = '文章保存成功'
                except Exception as e:
                    Logger().log(e, True)
                    ret['message'] = '文章保存失败'
            elif action == 'patch':
                try:
                    article_obj = Article.get(Article.id == article_id)
                    article_obj.title = title
                    article_obj.article_type_id = article_type
                    article_obj.summary = summary
                    article_obj.content = content
                    article_obj.update_date = datetime.datetime.now()
                    article_obj.save()
                    ret['status'] = 'true'
                    ret['message'] = '文章修改成功'
                except Exception as e:
                    Logger().log(e, True)
                    ret['message'] = '文章修改失败'

            elif action == 'delete':
                try:
                    article_obj = Article.get(Article.id == article_id)
                    article_obj.delete_instance()
                    ret['status'] = 'true'
                    ret['message'] = '文章删除成功'
                except Exception as e:
                    Logger().log(e, True)
                    ret['message'] = '文章删除失败'
            else:
                ret['message'] = '请求非法'
                Logger().log(ret, True)
        else:
            ret['message'] = '参数非法'
            Logger().log(ret, True)
        self.write(json.dumps(ret))

