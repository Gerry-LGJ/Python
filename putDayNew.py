# -*- coding: utf8 -*-

import requests
import time
import random
import json
import student

putDayNew_url = "https://gc.hc-web.cn/putDayNew"

putDayNew_headers = {
    # POST /putDayNew HTTP/1.1
    'Host': "gc.hc-web.cn",
    'Connection': "keep-alive",
    # 'Content-Length': "86",
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    'content-type': "application/x-www-form-urlencoded",
    'Referer': "https://servicewechat.com/wxa94aa0baa78ebdb9/8/page-frame.html",
    'Accept-Encoding': "gzip, deflate, br"
}

putDayNew_data = {
    'uid': "",  # 学生ID
    'am': "36",  # 上午体温
    'pm': "36",  # 下午体温
    'bex': "false",  # 是否咳嗽
    'panting': "false",  # 是否气促
    'other': "",  # 其它症状
    'campus': "南校区",  # 现住小区
    'plan': "0",  # 近一周是否计划去高风险地区
    'planaddress': ""  # 如果计划去高风险地区的话，请填写，并将plan键置1
}


def random_Float():
    temp = random.uniform(36.5, 37.0)
    result = "%.1f" % temp
    print(result)
    return result


def railyReport(uid, bex="false", panting="false", other="", campus="暂未反校"):
    """
    每日一报具体函数
    :param uid: 学生ID-str
    :param am: 上午体温-str
    :param pm: 下午体温-str
    :param bex: 是否咳嗽-str
    :param panting: 是否气促-str
    :param other: 其它症状-str
    :param campus: 现住小区-str
    :return: None
    """
    putDayNew_data['uid'] = uid
    putDayNew_data['am'] = random_Float()
    putDayNew_data['pm'] = random_Float()
    putDayNew_data['bex'] = bex
    putDayNew_data['panting'] = panting
    putDayNew_data['other'] = other
    putDayNew_data['campus'] = campus

    result = requests.post(url=putDayNew_url, headers=putDayNew_headers, data=putDayNew_data)
    response = json.loads(result.text)
    print(result.text)

    if response["msg"] != "保存成功":
        raise Exception("响应出现警告，请前往百度云函数控制台进行检查。")


if __name__ == '__main__':
    stuName = str(input("请输入姓名："))
    stuID = str(input("请输入学号："))

    stu_json = student.request_student(stuName, stuID)
    putDayNew_data['uid'] = stu_json['user']['id']

    new_result = requests.post(url=putDayNew_url, headers=putDayNew_headers, data=putDayNew_data)
    print(new_result.text)
    print("恭喜完成每日一报测试！！！")
