import matplotlib.pyplot as plt
from matplotlib.font_manager import *
from models.blog import ServerStatus
import datetime

# # 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
# # 解决负号'-'显示为方块的问题
matplotlib.rcParams['axes.unicode_minus'] = False


def cpu_status(count):
    # 获取要显示几分钟之前的
    # step = query_data['filter']
    # 获取当前时间
    # now = datetime.datetime.now()
    # 获取当前分钟
    # now_min = datetime.datetime.strftime(now, '%M')
    # 获取当前减去要显示几分钟
    # get_min = int(now_min) - int(step)
    # 获取几分钟之前的时间
    # get_date = now.replace(minute=get_min)
    # print(get_date)
    # x周 时间数据  y周 cpu数据
    x_data_1, y_data_1 = [], []
    y_data_5 = []
    y_data_15 = []

    # 数据库中查询大于之前几分钟的数据，就是获取从那个时间点后又创建的数据
    # old_objs = ServerStatus.select().where(ServerStatus.created_date > get_date).order_by(ServerStatus.created_date.asc())[0:4]
    # 提取数据库最后的几条数据
    old_objs = ServerStatus.select().order_by(ServerStatus.created_date.desc())[0:int(count)]
    for i in old_objs:
        # print(i.id)
        # 存在
        if i.created_date:
            # 分钟时间添加进x周
            x_data_1.append(datetime.datetime.strftime(i.created_date, '%H:%M'))
            # 负载数据添加进y周
            y_data_1.append(i.cpu_load_1)
            y_data_5.append(i.cpu_load_5)
            y_data_15.append(i.cpu_load_15)
    # # 画图，设置画布大小
    plt.figure(figsize=(4.8, 1.2))
    # 设置画布x轴数据字体及颜色
    plt.xticks(fontsize=6, color='#f06215')
    # 设置画布y轴数据字体及颜色
    plt.yticks(fontsize=6, color='#337ab7')
    # 设置图像的上下左右距离边际的位置
    plt.subplots_adjust(left=0.06, bottom=0.15, right=0.996, top=0.996, wspace=0.2, hspace=0)
    # 画图 设置lable
    plt.plot(x_data_1, y_data_1, linewidth=0.8, label='1分钟')
    plt.plot(x_data_1, y_data_5, linewidth=0.8, label='5分钟')
    plt.plot(x_data_1, y_data_15, linewidth=0.8, label='15分钟')
    # 设置x轴最小位置，最大位置
    plt.xlim([min(x_data_1), max(x_data_1)])
    # 设置x轴最小位置，最大位置
    # plt.ylim([0.00, 10.00])
    # 设置x周名称
    # plt.xlabel('时间', fontsize=8)
    # 设置y周名称
    # plt.ylabel('负载', fontsize=8)
    # 设置title
    # plt.title('CPU 使用率')
    # 生成描述
    plt.legend(fontsize=5)
    # 展示
    # plt.show()
    # plt.savefig('status.png')
    return plt


def mem_status(count):
    x_data, y_data = [], []

    # 提取数据库最后的几条数据
    mem_objs = ServerStatus.select().order_by(ServerStatus.created_date.desc())[0:int(count)]
    for i in mem_objs:
        # print(i.id)
        # 存在
        if i.created_date:
            # 分钟时间添加进x周
            x_data.append(datetime.datetime.strftime(i.created_date, '%H:%M'))
            # 负载数据添加进y周
            y_data.append(i.mem)
    y_data = [9321, 12932, 10512, 9432, 12612, 11932, 9527, 8921, 11910, 13080]
    while len(y_data) < int(count):
        y_data.insert(0, 0)
    # # 画图，设置画布大小
    plt.figure(figsize=(4.8, 1.2))
    # 设置画布x轴数据字体及颜色
    plt.xticks(fontsize=6, color='#f06215')
    # 设置画布y轴数据字体及颜色
    plt.yticks(fontsize=6, color='#337ab7')
    # 设置图像的上下左右距离边际的位置
    plt.subplots_adjust(left=0.08, bottom=0.15, right=0.996, top=0.996, wspace=0.2, hspace=0)
    # 画图 设置颜色
    plt.plot([], [], color='g', label='可用内存', linewidth=3)
    plt.stackplot(x_data, y_data, color='g')
    # 设置x轴最小位置，最大位置
    plt.xlim([min(x_data), max(x_data)])
    # 设置x轴最小位置，最大位置(内存最大)
    plt.ylim([0, 15887])
    # 生成描述
    plt.legend(fontsize=6)
    # 展示
    # plt.show()
    return plt


# mem_status(count=10)
