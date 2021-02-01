import requests

iui_url = "https://gc.hc-web.cn/inputUserInfo"

headers = {
    # POST /inputUserInfo HTTP/1.1
    'Host': "gc.hc-web.cn",
    'Connection': "keep-alive",
    'Content-Length': "8",
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
    'content-type': "application/x-www-form-urlencoded",
    'Referer': "https://servicewechat.com/wxa94aa0baa78ebdb9/8/page-frame.html",
    'Accept-Encoding': "gzip, deflate, br"
}

iui_data = {
    'uid': "10701"
    # 'uid': "1539"
}


def request_iui():
    try:
        result = requests.post(url=iui_url, headers=headers, data=iui_data)
        print(result.text)
    except Exception as e:
        print(f"发生错误！！！\n{e}")


# request_iui()
