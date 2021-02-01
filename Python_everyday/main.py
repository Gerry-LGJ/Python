"""
描述：
1. 程序目的用于繁杂的每日一报，别无它用，可根据需求自定义批量功能。
2. 本文件代码，仅用于百度云函数。

使用说明：
1. 自行选择开通云函数服务提供商，比如百度云，腾讯云，阿里云，等等...
2. 自行了解云函数的使用教程
3. 自行承担误操作带来的后果

警告：使用本代码，代表您已阅读并同意以下条款。
1. 如发现每日自动一报的内容与个人真实情况差异巨大，将添加黑名单，甚至停止该项目，请悉知。
2. 为防止代码滥用，运行程序时会在后台记录使用情况，请悉知。
3. 勿作死到处乱传代码，否则自行承担后果。
3. 商用请取得作者许可，否则将进行举报并停止该项目。


* 最后祝愿疫情能够早日结束，祝愿白衣天使能早日与家人团聚。祝大家新年快乐......
更新日期：2021.2.1 ---- By TimeChicken
"""
# start code
import student  # 用于获取学生的信息，以便每日一报
import putDayNew  # 用于每日一报
# import getDay  # 获取所有每日一报的记录
import time  # 用于缓冲post请求，防止服务器崩溃

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


def everyone_report(a=None, b=None):
    # 按样式添加
    name_list = [
        {'stuname': "林光纪", 'stuid': "0604190118"},
        {'stuname': "蒋滨泓", 'stuid': "0604180239"},
        {'stuname': "秦露", 'stuid': "0604190226"},
        {'stuname': "许永涛", 'stuid': "0602190339"},
        {'stuname': "吴泽森", 'stuid': "0604190107"},
        {'stuname': "程文兴", 'stuid': "0604190227"},
        # {'stuname': "吴典泽", 'stuid': "0604190208"},
        {'stuname': "李泽永", 'stuid': "1502190129"}
    ]

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
# end code
