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
