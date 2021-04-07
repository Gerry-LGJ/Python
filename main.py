# -*- coding: utf8 -*-

import login                # 用于获取学生的信息，以便每日一报
import putDay               # 用于每日一报
# import getDay             # 获取所有每日一报的记录
import time                 # 用于缓冲post请求，防止服务器崩溃
import json                 # 转换响应对象为字典
import requests             # 请求包

# 请自行前往 https://pushplus.hxtrip.com 获取token，没有留空即可，没有token时若云函数出错则不能及时推送
TOKEN = ""

# 1.按样式添加即可
# 2.校区可选参数有 "南校区","北校区","海珠校区","滨江校区","花都校区","走读","暂未返校"
# 3.其它具体可选参数请参考代码
name_list = [
    # ####{‘stuname': "姓名", 'stuid': "学号", 'campus': "校区"},####
    {'stuname': "碳烤时光鸡", 'stuid': "1234567890", 'campus': "烤鸡大学"},
    {'stuname': "康师傅冰红茶", 'stuid': "0123456789", 'campus': "野鸡大学"},
    {'stuname': "再来杯82年的情露", 'stuid': "9012345678", 'campus': "山鸡大学"},
    {'stuname': "榨果粒橙子", 'stuid': "8901234567", 'campus': "养鸡大学"},
    {'stuname': "镊子", 'stuid': "7890123456", 'campus': "吃鸡大学"},
    {'stuname': "蟠桃", 'stuid': "6789012345", 'campus': "煲鸡大学"},
    {'stuname': "涛涛江水", 'stuid': "5678901234", 'campus': "椰子鸡大学"},
]

'''真正每日一报的流程函数代码，main()中的是省略部分流程，容易被服务器探测出日报逻辑问题
def reportEveryone(name, stuid):
    """
    此函数可用于批量用户每日一报，个人请运行main。云函数用不到，故停止维护
    :param name: 姓名-str
    :param stuid: 学号-str
    :return: None
    """
    people = student.request_student(name, stuid)  # 登陆
    print(people)
    time.sleep(0.3)
    # getDay.getDay(people['user']['id'])  # 打印每日一报历史记录
    time.sleep(0.3)
    putDayNew.railyReport(people['user']['id'])  # 每日一报
    # getDay.getDay(people['user']['id'])  # 打印每日一报历史记录
    time.sleep(0.3)
    print("恭喜完成每日一报！！！")
'''


def server_push(result):
    """
    此函数用于每日一报出现问题时能及时通过push_plus进行微信推送
    :param result: 错误信息
    :return: None
    """
    error_file = result.__traceback__.tb_frame.f_globals['__file__']  # 错误文件
    error_line = result.__traceback__.tb_lineno  # 错误行数
    if TOKEN is "":
        print("[未设置token，将不能及时推送错误......]")
        print(str(result) + "(Error_filename:" + str(error_file) + ", Error_line:" + str(error_line) + ")")
        return
    push_url = "http://pushplus.hxtrip.com/send?"
    title = "哎呀，每日一报云函数出错啦，原因如下"
    data = {
        "token": TOKEN,
        "title": title,
        "content": str(result) + "(Error_filename:" + str(error_file) + ", Error_line:" + str(error_line) + ")"
    }
    response = json.loads(requests.post(push_url, data, verify=False).text)
    # print(response)                           # 云函数可以不用打印


def main(a=None, b=None):
    try:
        for stu in name_list:
            person = login.request_student(stu['stuname'], stu['stuid'])  # 登陆
            # print(person)                                                   # 打印用户信息
            time.sleep(0.2)  # 缓冲
            # getDay.getDay(person['user']['id'])                             # 打印每日一报历史记录
            # time.sleep(0.2)

            putDayNew.railyReport(uid=person['user']['id'], campus=stu['campus'])  # 每日一报

            # getDay.getDay(person['user']['id'])                             # 打印每日一报历史记录
            # print("恭喜 " + stu['stuname'] + " 完成每日一报！！！")
            time.sleep(0.2)

    except Exception as big_error:
        server_push(big_error)
        return "每日一报失败，若设置push plus的token请前往微信查看错误内容，未设置请查看云函数运行过程所产生的日志。"

    return "每日一报成功。"


if __name__ == '__main__':
    main()
