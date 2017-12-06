import tornado
from tornado.web import RequestHandler
import tornado.web
import datetime
import json
import uuid
import qiniu
import sys
import io
from utils import get_status
from models.blog import Blog, Article, UserInfo, ArticleType, UploadFileInfo, FriendlyLink
from utils.pagination import Page
from utils.log import Logger
from config import ACCESS_KEY, SECRET_KEY, BUCKET_NAME, BASE_STATIC_URL

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')


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
        return self.render('admin/index.html')


class ArticleHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        current_page = self.get_argument("p", 1)
        try:
            current_page = int(current_page)
        except ValueError as e:
            Logger().log(e, True)
            self.redirect('/admin/index')
        data_count = Article.select().count()
        page_obj = Page(current_page=current_page, data_count=data_count, per_page_count=15)
        page_html = page_obj.page_str(base_url="/admin/article?")
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
        self.render('admin/article.html', at_list=at_list, page_html=page_html, article_types=article_types)

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


class TagsHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        tags_list = []
        try:
            tags_objs = ArticleType.select()
            for t in tags_objs:
                tags_list.append({'id': t.id, 'type': t.article_type})
            if len(tags_list) <= 0:
                return self.redirect('/404')
            self.render('admin/tags.html', tags_list=tags_list)
        except Exception as e:
            Logger().log(e, True)
            self.render('index/500.html')

    def post(self, *args, **kwargs):
        ret = {'status': 'false', 'message': '', 'data': ''}
        article_type_id = self.get_argument('type_id', None)
        article_type = self.get_argument('type', None)
        action = self.get_argument('action', None)
        if article_type_id and article_type and action:
            if action == 'post':
                try:
                    ArticleType.insert(article_type=article_type).execute()
                    ret['status'] = 'true'
                    ret['message'] = '类型保存成功'
                except Exception as e:
                    Logger().log(e, True)
                    ret['message'] = '类型保存失败'
            elif action == 'patch':
                try:
                    article_type_obj = ArticleType.get(ArticleType.id == article_type_id)
                    article_type_obj.article_type = article_type
                    article_type_obj.save()
                    ret['status'] = 'true'
                    ret['message'] = '类型保存成功'
                except Exception as e:
                    Logger().log(e, True)
                    ret['message'] = '类型保存失败'
            else:
                ret['message'] = '请求非法'
                Logger().log(ret, True)
        else:
            ret['message'] = '参数非法'
            Logger().log(ret, True)
        self.write(json.dumps(ret))


class FlinkHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        flink_list = []
        try:
            flink_objs = FriendlyLink.select()
            for f in flink_objs:
                flink_list.append({'id': f.id,
                                   'name': f.name,
                                   'link': f.link,
                                   'weight': f.weight})
            if len(flink_list) <= 0:
                return self.redirect('/404')
            self.render('admin/flink.html', flink_list=flink_list)
        except Exception as e:
            Logger().log(e, True)
            self.render('index/500.html')

    def post(self, *args, **kwargs):
        ret = {'status': 'false', 'message': '', 'data': ''}
        flink_id = self.get_argument('flink_id', None)
        flink_name = self.get_argument('name', None)
        flink_link = self.get_argument('link', None)
        flink_weight = self.get_argument('weight', None)
        action = self.get_argument('action', None)
        if flink_id and flink_name and flink_link and flink_weight and action:
            if action == 'post':
                try:
                    flink_obj = FriendlyLink(name=flink_name)
                    flink_obj.link = flink_link
                    flink_obj.weight = flink_weight
                    flink_obj.save()
                    ret['status'] = 'true'
                    ret['message'] = '友链保存成功'
                except Exception as e:
                    Logger().log(e, True)
                    ret['message'] = '友链保存失败'
            elif action == 'patch':
                try:
                    flink_obj = FriendlyLink.get(FriendlyLink.id == flink_id)
                    flink_obj.link = flink_link
                    flink_obj.name = flink_name
                    flink_obj.weight = flink_weight
                    flink_obj.save()
                    ret['status'] = 'true'
                    ret['message'] = '友链保存成功'
                except Exception as e:
                    Logger().log(e, True)
                    ret['message'] = '友链保存失败'
            elif action == 'delete':
                try:
                    flink_obj = FriendlyLink.get(FriendlyLink.id == flink_id)
                    flink_obj.delete_instance()
                    ret['status'] = 'true'
                    ret['message'] = '友链删除成功'
                except Exception as e:
                    Logger().log(e, True)
                    ret['message'] = '友链删除失败'
            else:
                ret['message'] = '请求非法'
                Logger().log(ret, True)
        else:
            ret['message'] = '参数非法'
            Logger().log(ret, True)
        self.write(json.dumps(ret))


class ProfileHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        username = self.get_secure_cookie('username')
        user_info = {'username': username}
        try:
            user_obj = UserInfo.get(UserInfo.username == username)
            user_info['password'] = user_obj.password
            user_info['email'] = user_obj.email
            self.render('admin/profile.html', user_info=user_info)
        except Exception as e:
            Logger().log(e, True)
            self.render('index/500.html')

    def post(self, *args, **kwargs):
        ret = {'status': 'false', 'message': '', 'data': ''}
        username = self.get_secure_cookie('username', None)
        password = self.get_argument('password', None)
        email = self.get_argument('email', None)
        if username and password and email:
            try:
                user_obj = UserInfo.get(UserInfo.username == username)
                user_obj.password = password
                user_obj.email = email
                user_obj.update_date = datetime.datetime.now()
                user_obj.save()
                ret['status'] = 'true'
                ret['message'] = '用户信息修改成功'
            except Exception as e:
                Logger().log(e, True)
                ret['message'] = '用户信息修改失败'
        else:
            ret['message'] = '参数非法'
            Logger().log(ret, True)
        self.write(json.dumps(ret))


class BlogHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        blog_info = {}
        try:
            blog_obj = Blog.get(Blog.id == 1)
            blog_info['title'] = blog_obj.title
            blog_info['site'] = blog_obj.site
            blog_info['about'] = blog_obj.about
            blog_info['copy_right'] = blog_obj.copyright
            self.render('admin/blog.html', blog_info=blog_info)
        except Exception as e:
            Logger().log(e, True)
            self.render('index/500.html')

    def post(self, *args, **kwargs):
        ret = {'status': 'false', 'message': '', 'data': ''}
        title = self.get_argument('title', None)
        site = self.get_argument('site', None)
        about = self.get_argument('about', None)
        copy_right = self.get_argument('copy_right', None)
        print(title, site, about, copy_right)
        if title and site and about and copy_right:
            try:
                blog_obj = Blog.get(Blog.id == 1)
                blog_obj.title = title
                blog_obj.site = site
                blog_obj.about = about
                blog_obj.copyright = copy_right
                blog_obj.update_date = datetime.datetime.now()
                blog_obj.save()
                ret['status'] = 'true'
                ret['message'] = '网站信息修改成功'
            except Exception as e:
                Logger().log(e, True)
                ret['message'] = '网站信息修改失败'
        else:
            ret['message'] = '参数非法'
            Logger().log(ret, True)
        self.write(json.dumps(ret))


class StatusHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        monitor_type = self.get_argument('monitor_type', None)
        count = self.get_argument('count', 10)
        stream = io.BytesIO()
        if monitor_type == 'cpu':
            plt = get_status.cpu_status(count)
            plt.savefig(stream)
            plt.close()
            self.write(stream.getvalue())
        elif monitor_type == 'mem':
            plt = get_status.mem_status(count)
            plt.savefig(stream)
            plt.close()
            self.write(stream.getvalue())


class UploadHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        ret = {'status': 'false', 'message': '', 'data': ''}
        file_metas = self.request.files["editorImage"]
        q_obj = qiniu.Auth(ACCESS_KEY, SECRET_KEY)
        key = str(uuid.uuid1())
        token = q_obj.upload_token(BUCKET_NAME, key, 3600)
        for meta in file_metas:
            file_name = meta['filename']
            q_ret, info = qiniu.put_data(token, key, meta['body'])
            if q_ret is not None:
                ret['status'] = 'true'
                ret['message'] = '图片上传成功'
                ret['data'] = BASE_STATIC_URL + key
                try:
                    UploadFileInfo.insert(name=file_name, key=key, hash=q_ret['hash']).execute()
                except Exception as e:
                    Logger().log(e, True)
                    ret['message'] = '图片上传失败'
            else:
                Logger().log(info, True)
                ret['message'] = '图片上传失败'
        return self.write(json.dumps(ret))
