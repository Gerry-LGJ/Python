# -*- coding: utf8 -*-

import requests
import login

getDay_url = "https://gc.hc-web.cn/getDay"

getDay_headers = {
    # POST /getDay HTTP/1.1
    'Host': "gc.hc-web.cn",
    'Connection': "keep-alive",
    'Content-Length': "8",
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    'content-type': "application/x-www-form-urlencoded",
    'Referer': "https://servicewechat.com/wxa94aa0baa78ebdb9/8/page-frame.html",
    'Accept-Encoding': "gzip, deflate, br"
}

getDay_data = {
    'uid': "1540"
}


def getDay(uid):
    getDay_data['uid'] = uid
    try:
        result = requests.post(url=getDay_url, headers=getDay_headers, data=getDay_data)
        print("获取信息成功！！！\n" + result.text)
    except Exception as err:
        print(f"获取信息失败！！！\n{err}")


if __name__ == '__main__':
    stuName = str(input("请输入姓名："))
    stuID = str(input("请输入学号："))

    try:
        stu_json = login.request_student(stuName, stuID)
        getDay_data['uid'] = stu_json['user']['id']

        getDay_result = requests.post(url=getDay_url, headers=getDay_headers, data=getDay_data)
        print("获取信息成功！！！\n" + getDay_result.text)

    except Exception as e:
        print(f"获取信息失败！！！\n{e}")
