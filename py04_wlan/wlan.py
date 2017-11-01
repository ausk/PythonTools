#!/usr/bin/python3
# 2017.08.05 08:39:35 CST
# 2017.11.01 00:32:22 CST
"""
登录校园网！
"""

import re, bs4, requests
import urllib
import os, sys, time
import pprint

## 切换工作目录
os.chdir(os.path.abspath(os.path.expanduser(os.path.dirname(__file__))))
prt = pprint.pprint

LINE_DOT = "." * 77
LINE_EQ  = "=" * 77
usr = "XXX"  # 你的校园网账号
pwd = "XXX"  # 你的校园网密码

_headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/51.04",
    "Host": "192.168.50.3:8080",
}

_cookies ={
    "EPORTAL_AUTO_LAND": "",
    "EPORTAL_COOKIE_OPERATORPWD": "",
    "EPORTAL_COOKIE_DOMAIN": "",
    "EPORTAL_COOKIE_SERVER": "",
    "EPORTAL_COOKIE_SAVEPASSWORD": "true",
    "EPORTAL_COOKIE_USERNAME": "{usr}".format(usr=usr),
    "EPORTAL_COOKIE_PASSWORD": "{pwd}".format(pwd=pwd),
    "EPORTAL_COOKIE_SERVER_NAME": "è¯·éæ©æå¡",
}

_data={
    "userId": "{usr}".format(usr=usr),
    "password": "{pwd}".format(pwd=pwd),
    "service": "",
    "operatorPwd": "",
    "validcode": ""
}

def getServerData(sess):
    """访问 "http://192.168.50.3:8080/", 获取JSESSIONID和跳转地址。
    """
    url = "http://192.168.50.3:8080/"
    res = sess.get(url)
    jsid = sess.cookies.get_dict()["JSESSIONID"]
    href = re.findall(r"(?<=<script>top.self.location.href=')(.*)(?='</script>)", res.text)[0]
    open("wlan_serverdata.txt", "w+").write(res.text)
    return jsid, href

def genPostCookies(jsid):
    """模仿JS代码，生成提交时用到的Cookies。
    """
    cookies = _cookies.copy()
    cookies["JSESSIONID"] = jsid
    return cookies

def genPostHeaders(href):
    """生成提交时的请求头
    """
    headers = _headers.copy()
    headers["Referer"] = href
    return headers

def genPostData(href):
    """生成待提交的数据
    """
    query = urllib.parse.urlparse(href).query
    data = _data.copy()
    data["queryString"] = query
    return data

def login(sess=None):
    """使用账户密码登录
    """
    sess = requests.Session()
    ## 获取/生成配置
    jsid, href = getServerData(sess)    # 从服务器获取信息
    time.sleep(1)
    cookies = genPostCookies(jsid)      # 生成 cookies
    headers = genPostHeaders(href)      # 生成 headers
    data_login = genPostData(href)      # 生成 form data

    ## 使用生成的数据，更新会话，登录校园网，并获取用户idx
    url = "http://192.168.50.3:8080/eportal/InterFace.do?method=login"
    sess.cookies.update(cookies)
    sess.headers.update(headers)
    res = sess.post(url, data = data_login).json()

    ## 判断是否登录成功
    result = res["result"]
    if result == "success":
        print("Login success!")
        return True
    else:
        print("Login error!")
        return False

def wlan_login():
    try:
        return login()
    except:
        return False

if __name__ == "__main__":
    flag = False
    for i in range(3):
        print("Try {}/3 times".format(i+1))
        flag = wlan_login()
        if flag:
            break

    if not flag:
        print("Fatal error, exiting...")



