from tornado.web import RequestHandler
from models.blog import blog


class BaseHandler(RequestHandler):
    # 初始化，请求之前做的操作
    # def initialize(self, *args, **kwargs):
          # someting ...

    # 响应 Head 的请求
    def head(self, *args, **kwargs):
        self.write('200')

    # 设置header 添加，删除，更改等..
    def set_default_headers(self):
        self.clear_header('Server')

    # 当真正调用请求处理方法之前的初始化处理
    def prepare(self):
        # 连接数据库
        blog.connect()

    # 设置用户cookie认证
    def get_current_user(self):
        return self.get_secure_cookie("username", None)

    # 结束调用后的操作
    def on_finish(self):
        # 关闭数据库连接
        if not blog.is_closed():
            blog.close()
