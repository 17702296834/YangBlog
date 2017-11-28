from tornado.web import RequestHandler
import os
import json
from models.blog import Blog, Article
from utils.pagination import Page


class IndexHandler(RequestHandler):
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
                            'summary': a.summary,
                            'read_count': a.read_count,
                            'created_date': a.created_date,
                            'article_type': a.type_choices[a.article_type-1][1]
                            })
        at_list.reverse()
        page_html = page_obj.page_str(base_url="index?")
        self.render('index/index.html', at_list=at_list, page_html=page_html)


class ArticleHandler(RequestHandler):
    def get(self, article=None):
        try:
            article_obj = Article.get(Article.id == article)
        except Exception as e:
            print(e)
            return self.render('index/404.html')
        article_data = {'id': article_obj.id,
                        'title': article_obj.title,
                        'content': article_obj.content,
                        'read_count': article_obj.read_count,
                        'created_date': article_obj.created_date,
                        'article_type': article_obj.type_choices[article_obj.article_type-1][1]
                        }
        self.render('index/article.html', article_data=article_data)


class SearchHandler(RequestHandler):
    def get(self):
        search_kw = self.get_argument('search', None)
        current_page = self.get_argument("p", 1)
        current_page = int(current_page)
        if search_kw:
            data_count = Article.select().where(Article.title.contains(search_kw)).count()
            page_obj = Page(current_page=current_page, data_count=data_count)
            try:
                if current_page == 1:
                    search_obj = Article.select().where(Article.title.contains(search_kw))[-page_obj.end:]
                else:
                    search_obj = Article.select().where(Article.title.contains(search_kw))[-page_obj.end:-page_obj.start]
            except Exception as e:
                print(e)
                return self.render('index/404.html')
            search_list = []
            for s in search_obj:
                search_list.append({'id': s.id,
                                    'title': s.title,
                                    'summary': s.summary,
                                    'read_count': s.read_count,
                                    'created_date': s.created_date,
                                    'article_type': s.type_choices[s.article_type-1][1]
                                    })
            search_list.reverse()
            page_html = page_obj.page_str(base_url="search?search={_kw}&".format(_kw=search_kw))
            self.render('index/search.html', search_list=search_list, page_html=page_html)
        self.redirect('/index')
