from models.blog import Blog, FriendlyLink, Article
from utils.log import Logger

server_error = '服务器开小差了。。。'

def footer_info(self):
    try:
        blog_obj = Blog.get(Blog.id == 1)
        footer_text = blog_obj.copyright
        return footer_text
    except Exception as e:
        Logger().log(e, True)
        return server_error


def get_title_data(self, info):
    try:
        blog_obj = Blog.get(Blog.id == 1)
        if info == 'title':
            title_data = blog_obj.title
        elif info == 'site':
            title_data = blog_obj.site
        else:
            return server_error
        return title_data
    except Exception as e:
        Logger().log(e, True)
        return server_error


def frindly_link(self):
    try:
        blog_objs = FriendlyLink.select().order_by(FriendlyLink.weight)
        fl_html = ""
        for obj in blog_objs:
            fl_html += '<li><a href = "{_url}" >{_name}</a></li>'.format(_url=obj.link, _name=obj.name)
        return fl_html
    except Exception as e:
        Logger().log(e, True)
        return server_error


def get_aid(self, a_id, action):
    flag = False
    if a_id and action:
        if action == 'prev':
            while not flag:
                try:
                    article_obj = Article.get(id=a_id-1)
                    if article_obj:
                        flag = True
                        return article_obj.id
                except Article.DoesNotExist as e:
                    Logger().log(e, True)
                a_id -= 1
        elif action == 'next':
            while not flag:
                try:
                    article_obj = Article.get(id=a_id + 1)
                    if article_obj:
                        flag = True
                        return article_obj.id
                except Article.DoesNotExist as e:
                    Logger().log(e, True)
                a_id += 1
    return 1
