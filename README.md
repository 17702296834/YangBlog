# YangBlog
* 两个星期'撸'好的一个博客程序 XD
## 技术栈
* 基于 Py3 + Tornado
* 前端框架 Bootstrap + JQuery
* 富文本编辑框 bootstrap-wysiwyg
* 字体图标 Font Awesome 
* 按钮 Buttons
* 数据库 Mysql + Peewee
* 图片存储  QiniuYun 对象存储

## 实现功能
* /index 首页 文章列表，分页展示
* /article 文章页，上一页，下一页按钮
* /search 搜索标题展示页面，分页展示
* 头部标题、底部信息、右侧友链使用ui_methods功能实现
* /admin/index 后端管理页面，实现文章增加，删除，更改
* /admin/login 登录，使用Tornado的secure_cookie 认证
* /upload 上传图片处理，直接上传到Qiniu对象存储中

## 待完成
* 管理界面中的友链添加，删除，调整权重
* 管理界面中的最新文章展示
* 管理界面中的最后更改文章展示
* 管理界面的Tag分类显示，搜索
* 管理员忘记密码重置

## 感谢
* 开源软件
* Qiniu云的免费对象存储

## 使用模块
* peewee
* qiniu

## 部署方法
* config.py 中填写自己的qiniu对象存储的ACCESS_KEY，SECRET_KEY，BUCKET_NAME，BASE_STATIC_URL
* config.py 中修改MYSQL_URL 为自己的地址
* 使用 python app.py 启动，建议使用supervisor 管理程序运行

## 效果图
* index
![index](https://github.com/lgphone/YangBlog/blob/master/doc/pic/index.png)
* article
![article](https://github.com/lgphone/YangBlog/blob/master/doc/pic/article.png)
* search
![search](https://github.com/lgphone/YangBlog/blob/master/doc/pic/search.png)
* about
![about](https://github.com/lgphone/YangBlog/blob/master/doc/pic/about.png)
* page
![page](https://github.com/lgphone/YangBlog/blob/master/doc/pic/page.png)
* admin index
![admin index](https://github.com/lgphone/YangBlog/blob/master/doc/pic/admin_index.png)
* add article
![add article](https://github.com/lgphone/YangBlog/blob/master/doc/pic/add.png)
* del article
![del article](https://github.com/lgphone/YangBlog/blob/master/doc/pic/del.png)
* edit article
![edit article](https://github.com/lgphone/YangBlog/blob/master/doc/pic/edit.png)
