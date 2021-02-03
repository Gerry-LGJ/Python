# -*- coding: utf8 -*-

# start code
import student  # 用于获取学生的信息，以便每日一报
import putDayNew  # 用于每日一报
# import getDay  # 获取所有每日一报的记录
import time  # 用于缓冲post请求，防止服务器崩溃
import json
import requests

# 请自行前往 https://pushplus.hxtrip.com 获取token
TOKEN = ""

'''
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
    if TOKEN is "":
        print("未设置token哦......")
        return
    push_url = "http://pushplus.hxtrip.com/send?"
    title = "哎呀，每日一报云函数出错啦，原因如下"
    data = {
        "token": TOKEN,
        "title": title,
        "content": str(result)
    }
    response = json.loads(requests.post(push_url, data, verify=False).text)
    print(response)


def everyone_report(a=None, b=None):
    # 按样式添加即可
    name_list = [
      # {‘stuname': "姓名", 'stuid': "学号"},
        {'stuname': "张三", 'stuid': "1234567890"},
        {'stuname': "李四", 'stuid': "2234567890"},
        {'stuname': "王五", 'stuid': "3234567890"},
        {'stuname': "赵六", 'stuid': "4234567890"},
    ]

    try:
        for stu in name_list:
            person = student.request_student(stu['stuname'], stu['stuid'])  # 登陆
            print(person)  # 打印用户信息
            time.sleep(0.2)
            # getDay.getDay(person['user']['id'])  # 打印每日一报历史记录
            # time.sleep(0.2)

            putDayNew.railyReport(uid=person['user']['id'])  # 每日一报

            # getDay.getDay(person['user']['id'])  # 打印每日一报历史记录
            print("恭喜 " + stu['stuname'] + " 完成每日一报！！！")
            time.sleep(0.4)

    except Exception as big_error:
        server_push(big_error)
# end code
