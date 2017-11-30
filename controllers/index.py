from tornado.web import RequestHandler
from models.blog import Blog, Article, UserInfo
from utils.pagination import Page
from utils.log import Logger


class IndexHandler(RequestHandler):
    def get(self):
        current_page = self.get_argument("p", 1)
        try:
            current_page = int(current_page)
        except ValueError as e:
            Logger().log(e, True)
            self.redirect('/index')
        data_count = Article.select().count()
        page_obj = Page(current_page=current_page, data_count=data_count)
        page_html = page_obj.page_str(base_url="index?")
        at_list = []
        try:
            if current_page == 1:
                article_objs = Article.select()[-page_obj.end:]
            else:
                article_objs = Article.select()[-page_obj.end:-page_obj.start]

            for article_obj in article_objs:
                at_list.append({'id': article_obj.id,
                                'title': article_obj.title,
                                'summary': article_obj.summary,
                                'read_count': article_obj.read_count,
                                'created_date': article_obj.created_date,
                                'article_type': article_obj.article_type.article_type
                                })
            at_list.reverse()
        except Exception as e:
            Logger().log(e, True)
            return self.render('index/500.html')
        self.render('index/index.html', at_list=at_list, page_html=page_html)


class ArticleHandler(RequestHandler):
    def get(self, article_id=None):
        try:
            article_obj = Article.get(Article.id == article_id)
            article_data = {'id': article_obj.id,
                            'title': article_obj.title,
                            'content': article_obj.content,
                            'read_count': article_obj.read_count,
                            'created_date': article_obj.created_date,
                            'update_date': article_obj.update_date,
                            'article_type': article_obj.article_type.article_type
                            }
            query = Article.update(read_count=Article.read_count + 1).where(Article.id == article_id)
            query.execute()
        except Article.DoesNotExist as e:
            Logger().log(e, True)
            return self.render('index/404.html')
        except Exception as e:
            Logger().log(e, True)
            return self.render('index/500.html')
        self.render('index/article.html', article_data=article_data)


class SearchHandler(RequestHandler):
    def get(self):
        s_kw = self.get_argument('search', None)
        current_page = self.get_argument("p", 1)
        try:
            current_page = int(current_page)
        except ValueError as e:
            Logger().log(e, True)
            self.redirect('/index')
        if s_kw:
            data_count = Article.select().where(Article.title.contains(s_kw)).count()
            page_obj = Page(current_page=current_page, data_count=data_count)
            page_html = page_obj.page_str(base_url="search?search={_kw}&".format(_kw=s_kw))
            search_list = []
            try:
                if current_page == 1:
                    search_objs = Article.select().where(Article.title.contains(s_kw))[-page_obj.end:]
                else:
                    search_objs = Article.select().where(Article.title.contains(s_kw))[-page_obj.end:-page_obj.start]
                for search_obj in search_objs:
                    search_list.append({'id': search_obj.id,
                                        'title': search_obj.title,
                                        'summary': search_obj.summary,
                                        'read_count': search_obj.read_count,
                                        'created_date': search_obj.created_date,
                                        'article_type': search_obj.article_type.article_type
                                        })
                search_list.reverse()
                self.render('index/search.html', search_list=search_list, page_html=page_html)
            except Exception as e:
                Logger().log(e, True)
                return self.render('index/500.html')
        self.redirect('/index')


class AboutHandler(RequestHandler):
    def get(self):
        try:
            blog_obj = Blog.get(Blog.id == 1)
            user_obj = UserInfo.get(UserInfo.username == 'yang')
            about_data = {'username': user_obj.username,
                          'email': user_obj.email,
                          'about': blog_obj.about}
        except Exception as e:
            Logger().log(e, True)
            return self.render('index/500.html')
        self.render('index/about.html', about_data=about_data)


class NotfindHandler(RequestHandler):
    def get(self):
        return self.render('index/404.html')