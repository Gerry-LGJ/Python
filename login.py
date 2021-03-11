# -*- coding: utf8 -*-
"""
此模块用于模拟登陆，获取用于信息，尤其是(四位数的)uid
"""
import requests
import json

login_url = "https://gc.hc-web.cn/login"

login_headers = {
    # Client
    'Accept-Encoding': "gzip, deflate, br",
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    # Entity
    # 'Content-Length': '83',
    'content-type': "application/x-www-form-urlencoded",
    # Miscellaneous
    'Referer': "https://servicewechat.com/wxa94aa0baa78ebdb9/8/page-frame.html",
    # Transport
    'Connection': "keep-alive",
    'Host': "gc.hc-web.cn"
}


def request_student(name, pwd):
    """
    此函数用于获取学生信息对象
    :param name: 姓名-str
    :param pwd: 学号-str
    :return: student的信息对象
    """

    login_data = {'name': name, 'pwd': pwd}                 # 新建登陆信息字典
    stuResult = requests.post(url=login_url, headers=login_headers, data=login_data)  # 登陆获取信息
    student = json.loads(stuResult.text)                    # 将结果转换为json的python字典
    if student['status'] == 0:                              # 最近发现有憨批用错误的姓名学号，临时加个错误的解决方案
        raise Exception(student['msg'] + "，请检查学号姓名是否正确。")
    return student


if __name__ == '__main__':
    stuName = str(input("请输入姓名："))
    stuID = str(input("请输入学号："))
    print(request_student(stuName, stuID))
