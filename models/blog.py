from peewee import *
from playhouse.db_url import connect
import datetime
from config import MYSQL_URL


blog = connect(MYSQL_URL)


class BaseModel(Model):
    class Meta:
        database = blog


class UserInfo(BaseModel):
    username = CharField(unique=True, max_length=50, verbose_name='用户名', null=False)
    password = CharField(max_length=128, verbose_name='密码', null=False)
    nickname = CharField(max_length=50, verbose_name='昵称', default='')
    email = CharField(verbose_name='邮箱', unique=True, null=False)
    avatar = CharField(verbose_name='头像', null=True, default='')
    c_time = DateTimeField(default=datetime.datetime.now)
    u_time = DateTimeField(null=False)


class Blog(BaseModel):
    title = CharField(verbose_name='个人博客标题', max_length=64)
    site = CharField(verbose_name='个人博客前缀', max_length=32, unique=True)
    theme = CharField(verbose_name='博客主题', max_length=32)
    about = CharField(verbose_name='关于我')
    copyright = CharField(verbose_name='底部信息')


class Article(BaseModel):
    title = CharField(verbose_name='文章标题', max_length=128)
    summary = CharField(verbose_name='文章简介', max_length=255)
    read_count = IntegerField(default=0)
    content = TextField(verbose_name='文章内容')
    created_date = DateTimeField(verbose_name='创建时间', default=datetime.datetime.now)
    type_choices = [
            (1, "Python"),
            (2, "Linux"),
            (3, "OpenStack"),
            (4, "GoLang"),
            (5, "资讯")
        ]
    article_type = IntegerField(choices=type_choices, default=None)


def create_tables():
    blog.connect()
    blog.create_tables([UserInfo, Blog, Article])
    blog.close()


def drop_tables():
    blog.connect()
    blog.drop_tables([UserInfo, Blog, Article])
    blog.close()


# drop_tables()
# create_tables()


def create_test():
    user = UserInfo(username='yang')
    user.password = '123456'
    user.email = 'inboxcvt@gmail.com'
    user.u_time = datetime.datetime.now()
    user.save()


def update_test():
    pass


def delete_test():
    user = UserInfo.get(UserInfo.username == 'yang')
    user.delete_instance()


def select_test():
    obj = UserInfo.get(UserInfo.username == 'yang')
    # or
    # User.select().where((User.username == 'shenyang') | (User.username == 'wang')).first()
    # and
    # User.select().where((User.username == 'shenyang'), (User.password == '123')).first()
    if obj:
        print(obj.username)
    else:
        print('none have')


def select_all():
    ret = UserInfo.select()
    for obj in ret:
        print(obj.username)


def update_test():
    obj = UserInfo.get(UserInfo.username == 'yang')
    obj.password = '123'
    obj.u_time = datetime.datetime.now()
    obj.save()


# update_test()
# create_test()
# delete_test()
# select_test()
# update_test()
# print(datetime.datetime.now())

def create_a(i):
    obj = Article(title='阿里：未经批准不得违规擅自开展4K业务_{_i}'.format(_i=i))
    obj.summary = "近日，国家新闻出版广电总局向各省广电局及相关单位下发了关于规范和促进4K超高清电视发展的通知。通知针对超高清\
    电视发展中出现的管理不规范、技术质量不达标等问题，提出了7条指导性意见：一、充分认识发展4K超高清电视的重要性和艰巨性，坚持从\
    实际出发，加强政策引导。二、优先支持高清电视发展较好的省份和机构开展4K超高清电视试点，坚持试点先行，稳中求进_{_i}".format(_i=i)
    obj.content = '国家新闻出版广电总局文件新广电发[2017]230号'
    obj.article_type = 5
    obj.save()

def delete_a(i):
    user = Article.get(Article.id == i)
    user.delete_instance()

def create_blog():
    obj = Blog(title='YangEver的博客')
    obj.site = '前进前进..'
    obj.about = '关于我'
    obj.copyright = '©2017 prozhi.com 京ICP证030173号 京公网安备11000002000001号'
    obj.theme = 'Black'
    obj.save()

# create_blog()

# for i in range(1, 18):
#     create_a(i)

# print(Article.select().where(Article.title.contains('电')).count())
# print(Article.select().where(Article.title ** ('%电%')).count())