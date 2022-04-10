# -*- coding: utf8 -*-

import time
import requests
import time
import random
import json
import traceback
import sys
from datetime import datetime

# 请自行前往 https://wxpusher.dingliqc.com/docs/#/ 获取token，没有留空即可，没有token时若云函数出错则不能及时推送
TOKEN = ""

################################################################################################
# 警告：使用前请认真看说明文档。使用此脚本已代表你已阅读说明文档，并愿意承担使用后带来的不良后果。#
################################################################################################
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

# python script config
SCRIPT_VERSION = "v4.0"
IS_DEBUG = True
RUNTIME_ENV_MODE = 1 # runtime environment: 0:cloud 1:local


def dbgprint(*args, sep=' ', end='\n', file=None):
    if IS_DEBUG:
        print(*args, sep=sep, end=end, file=file)
    else:
        pass


def dbg_json_str_print_format(json_obj: dict) -> dict:
    return json.dumps(json_obj, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False)


def reportEveryone(a=None, b=None):
    # 注意：此部分为模拟人工每日一报流程的函数代码(时间较长)，main()中的是省略部分流程，但容易被服务器探测出日报逻辑问题，从而钓鱼

    start_time = time.time()
    dbgprint(f"{SCRIPT_VERSION} {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
    dbgprint(f"API_VERSION: {PutDay.API_VERSION}")
    try:
        for student in name_list:
            person = login_student(student['stuname'], student['stuid'])     # 登陆
            time.sleep(0.5)                                                  # 缓冲
            getDay(person['user']['id'])                                     # 打印每日一报历史记录
            time.sleep(2)                                                    # 缓冲
            everyone = PutDay(uid=person['user']['id'], stu_info=student)    # 创建每日一报实例
            everyone.railyReport()                                           # 每日一报ing
            del everyone                                                     # 清空对象
            time.sleep(0.5)                                                  # 缓冲
            getDay(person['user']['id'])                                     # 打印每日一报历史记录

    except Exception as big_error:
        if RUNTIME_ENV_MODE == 0:
            server_push(big_error, TOKEN)
        elif RUNTIME_ENV_MODE == 1:
            print(big_error)
            raise big_error
        return "每日一报失败，若设置push plus的token请前往微信查看错误内容，未设置请查看云函数运行过程所产生的日志。"

    dbgprint(f"Runtime take {time.time() - start_time} s.")
    return "每日一报成功。"


def main(a=None, b=None):
    start_time = time.time()
    dbgprint(f"{SCRIPT_VERSION} {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
    dbgprint(f"API_VERSION: {PutDay.API_VERSION}")
    try:
        for student in name_list:
            dbgprint(f"StartReport {str(student)}")
            person = login_student(student['stuname'], student['stuid'])     # 登陆
            time.sleep(0.1)                                                  # 缓冲
            everyone = PutDay(uid=person['user']['id'], stu_info=student)    # 创建每日一报实例
            everyone.railyReport()                                           # 每日一报
            del everyone                                                     # 清空对象

    except Exception as big_error:
        if RUNTIME_ENV_MODE == 0:
            server_push(big_error, TOKEN)
        elif RUNTIME_ENV_MODE == 1:
            print(big_error)
            raise big_error
        return "每日一报失败，若设置push plus的token请前往微信查看错误内容，未设置请查看云函数运行过程所产生的日志。"

    dbgprint(f"Runtime take {time.time() - start_time} s.")
    return "每日一报成功。"


class PutDay(object):

    # API config
    API_VERSION =               "20220409"              # 接口填报信息版本更新截止时间
    HOST =                      "jsd.hc-web.cn"         # 控制http报头的url和host属性，防止跨域请求
    HOST_URL =                  "https://" + HOST       # host url
    LOGIN_URL =   HOST_URL +    "/api/index/login"
    PUT_DAY_URL = HOST_URL +    "/api/index/putDay"
    GET_DAY_URL = HOST_URL +    "/api/index/getDay"

    ID_NAME = {}                                        # 学号和姓名
    PutDayNew_data = {}                                 # 每日一报的发送报文数据部分
    PutDayNew_headers = {
        # POST  HTTP/1.1
        'Host': HOST,
        'Connection': "keep-alive",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143"
                      " Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        'content-type': "application/x-www-form-urlencoded",
        'Referer': "https://servicewechat.com/wxa94aa0baa78ebdb9/8/page-frame.html",
        'Accept-Encoding': "gzip, deflate, br"
    }

    __PutDayNew_data_initial = {
        'version': API_VERSION,
        'uid': None,                                    # 学生ID
        'is_campus': "是",
        'campus': "南校区",
        'nowaddress': "目前在广州市内",
        'phone': "13456789012",
        'fever': "2",
        'jie': "5",
        'plan': "2",
        'risk_area': "低风险地区",
        'jkcode': "绿码",
        'new_status': "已返校",

        'planaddress': "undefined",
        'jie5': "undefined",
        'jie6': "undefined",
        'vaccine': "undefined",
        'vaccine1': "undefined",
        'status_remark': "undefined",
    }

    def __init__(self, uid: str, stu_info: dict):
        """
        初始化，更新用户自定义的信息
        :param uid: 学生ID(通过登陆后获取)-str
        :param stu_info: 学生信息-dict
        """
        self.__reset_PutDayNew_data()                               # reset data
        self.PutDayNew_data['uid'] = uid
        for key, value in stu_info.items():
            if not self.__PutDayNew_data_initial.__contains__(key):  # 查找键，防止“憨憨”传入不存在的键
                if key == 'stuname' or key == 'stuid':              # 筛选姓名和学号，因为报文当中不包含这俩选项
                    self.ID_NAME[key] = value                       # 将姓名学号保存起来，可能有用
                    continue
                raise Exception(f"The search for the \"{key}\" key failed. Please check if it exists.")
            self.PutDayNew_data[key] = value

    def __str__(self):
        return str(self.ID_NAME)

    def __reset_PutDayNew_data(self):
        """
        重置PutDayNew_data的数据
        :return: 无
        """
        self.PutDayNew_data.clear()
        for key, value in self.__PutDayNew_data_initial.items():
            self.PutDayNew_data[key] = value

    def railyReport(self):
        dbgprint(f"Requests: {self.PUT_DAY_URL}\n{dbg_json_str_print_format(self.PutDayNew_data)}")
        result = requests.post(url=self.PUT_DAY_URL, headers=self.PutDayNew_headers, data=self.PutDayNew_data)
        if result.status_code != 200:
            dbgprint(f"{sys._getframe().f_code.co_name}:{sys._getframe().f_lineno} "
                     f"SERVER-RESPONSE-ERROR: {str(self.ID_NAME)}")
            dbgprint(result.text)
            return # try next one
        response = json.loads(result.text)
        dbgprint(f"Response:{result.text}")

        if response["msg"] != "保存成功" or response["code"] != 1:  # 防止出现奇怪的回应，例如在非填报时间内做测试的时候
            raise Exception(f"每日一报-ERROR。Error_to:{str(self.ID_NAME)} {str(result.text)}")
        dbgprint(f"=========={sys._getframe().f_code.co_name} Done.==========",  end="\n\n")


# ############################################### 登陆模块 #############################################################
def login_student(name: str, pwd: str) -> dict:
    """
    此函数用于获取学生信息对象,测试函数为login_student_test()
    :param name: 姓名-str
    :param pwd: 学号-str
    :return: student的信息对象-dict
    """

    login_url = PutDay.LOGIN_URL
    login_headers = {
        # Client
        'Accept-Encoding': "gzip, deflate, br",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 "
                      "Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        # Entity
        # 'Content-Length': '83',
        'content-type': "application/x-www-form-urlencoded",
        # Miscellaneous
        'Referer': "https://servicewechat.com/wxa94aa0baa78ebdb9/22/page-frame.html",
        # Transport
        'Connection': "keep-alive",
        'Host': PutDay.HOST
    }

    login_data = {
        'version': PutDay.API_VERSION,
        'name': name,
        'pwd': pwd,
        'openid': "",
        'subscription': "reject"
    } # 新建登陆信息字典
    dbgprint(f"Requests: {login_url}\n{sys._getframe().f_code.co_name} \n {dbg_json_str_print_format(login_data)}")
    stuResult = requests.post(url=login_url, headers=login_headers, data=login_data)
    if stuResult.status_code != 200:
        dbgprint(f"{sys._getframe().f_code.co_name}:{sys._getframe().f_lineno}"
                 f" SERVER-RESPONSE-ERROR: {stuResult.text}")
        raise Exception(f"SERVER-RESPONSE-ERROR")
    stuResult_json = json.loads(stuResult.text)
    dbgprint(f"Response:\n{sys._getframe().f_code.co_name} \n {dbg_json_str_print_format(stuResult_json)}")
    if stuResult_json['code'] == 0:                                  # 最近发现有憨批用错误的姓名学号，临时加个错误的解决方案
        raise Exception(f"{name}=>{pwd}，" + stuResult_json['msg'] + "，请检查学号姓名是否正确。")
    student = stuResult_json['data']                                 # 拆包
    return student


def login_student_test():
    stuName = str(input("请输入姓名："))
    stuID = str(input("请输入学号："))
    print("获取信息成功！！！")
    print(json.dumps(login_student(stuName, stuID), sort_keys=True,
                     indent=4, separators=(',', ':'), ensure_ascii=False))
# ######################################################################################################################


# #################################################### 获取历史填报信息 #################################################
def getDay(uid: str) -> dict:

    getDay_url = PutDay.GET_DAY_URL
    getDay_headers = {
        # POST /getDay HTTP/1.1
        'Host': PutDay.HOST,
        'Connection': "keep-alive",
        'Content-Length': "8",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 "
                      "Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
        'content-type': "application/x-www-form-urlencoded",
        'Referer': "https://servicewechat.com/wxa94aa0baa78ebdb9/8/page-frame.html",
        'Accept-Encoding': "gzip, deflate, br"
    }
    getDay_data = {'uid': uid}

    dbgprint(f"Requests:{getDay_url}\n{sys._getframe().f_code.co_name} \n {dbg_json_str_print_format(getDay_data)}")
    try:
        result = requests.post(url=getDay_url, headers=getDay_headers, data=getDay_data)
        if result.status_code != 200:
            dbgprint(f"{sys._getframe().f_code.co_name}:{sys._getframe().f_lineno}"
                     f" SERVER-RESPONSE-ERROR: {result.text}")
            raise Exception(f"SERVER-RESPONSE-ERROR")
        dbgprint(f"Response:\n{dbg_json_str_print_format(json.loads(result.text))}")
        return json.loads(result.text)
    except Exception as err:
        dbgprint(f"获取历史日报信息失败！！！\n{err}")
        return {}


def getDay_test():
    stuName = str(input("请输入姓名："))
    stuID = str(input("请输入学号："))

    uid = login_student(stuName, stuID)['user']['id']
    result = getDay(uid=uid)
    if result is {}:
        print("获取信息失败！！！")
    else:
        print("获取信息成功！！！")
        print(json.dumps(result, sort_keys=True, indent=4, separators=(',', ':'), ensure_ascii=False))
# ######################################################################################################################


# ############################################### 检查是否每日一报模块(弃用) ###################################################
def isReport(uid):
    t = time.localtime()
    now_date = "%d-" % t.tm_year
    if 1 <= t.tm_mon <= 9:
        now_date += "0%d-" % t.tm_mon
    else:
        now_date += "%d-" % t.tm_mon
    if 1 <= t.tm_mday <= 9:
        now_date += "0%d" % t.tm_mday
    else:
        now_date += "%d" % t.tm_mday

    getDay_data = getDay(uid=uid)

    # print(getDay_data['data'][0]['time'])
    # print(now_date)
    if getDay_data['data'][0]['time'] == now_date:
        return True
    else:
        return False
# ######################################################################################################################


# ############################################### 云函数异常汇报模块 ####################################################
def server_push(result, token: str):
    """
    此函数用于每日一报出现问题时能及时通过push_plus进行微信推送
    :param token: 请自行前往 https://wxpusher.dingliqc.com/docs/#/ 获取token，没有留空即可，
                    没有token时若云函数出错则不能及时推送-str
    :param result: 错误信息-Exception
    :return: 无
    """
    error_file = result.__traceback__.tb_frame.f_globals['__file__']  # 错误产生的文件
    error_line = result.__traceback__.tb_lineno  # 错误行数
    if token == "":
        print("[未设置token，将不能及时推送错误......]")
        print(str(result) + "(Error_filename:" + str(error_file) + ", Error_line:" + str(error_line) + ")")
        return
    push_url = "http://wxpusher.zjiecode.com/api/send/message"
    title = "哎呀，每日一报云函数出错啦，点击查看"
    data = {
        "appToken": token,
        "summary": title,
        "contentType": 1,  # //内容类型 1表示文字  2表示html(只发送body标签内部的数据即可，不包括body标签) 3表示markdown
        "uids": ["UID_xxxxxxxxxxxxxxxxx"],
        "content": traceback.format_exc() + "(Error_filename:" + str(error_file) +
                   ", Error_line:" + str(error_line) + ")"
    }
    headers = {
        'Content-Type': "application/json",
    }
    data = json.dumps(data)
    response = json.loads(requests.post(push_url, data, headers=headers).text)
    dbgprint(response)
# ######################################################################################################################


# ########################################## 暴力每日一报 (刚写完又废弃了)################################################
START_ID = 26858 # [1~99999]
END_ID = 26903
def violence_railyReprot():
    '''
    直接用uid暴力请求日报，用pthread更爽
    :return: None
    '''
    dbgprint(f"{SCRIPT_VERSION} {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")
    dbgprint(f"API_VERSION: {PutDay.API_VERSION}")
    start_time = time.time()
    print(f"=========={sys._getframe().f_code.co_name} Start.==========")
    try:
        for every_id in range(START_ID, END_ID + 1):
            everyone = PutDay(str(every_id), {})
            everyone.railyReport()
            print(f"{every_id} Done.")

    except Exception as err:
        raise err
    print(f"=========={sys._getframe().f_code.co_name} Done.==========")
    print(f"Runtime take {time.time() - start_time} s.")
# ######################################################################################################################


if __name__ == '__main__':
    main()
    # reportEveryone()
    # login_student_test()
    # getDay_test()
    # violence_railyReprot()

