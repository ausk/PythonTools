#!/usr/bin/python3
# 2017.06.20 15:10:02 CST
# 有道命令行在线搜索(调用有道翻译)

import socket
import os,sys,re
from urllib import request,parse

socket.setdefaulttimeout(2) # 超时 5s

def fy(queryword):
    url = 'http://dict.youdao.com/fsearch?q={}'.format(parse.quote(queryword))
    html = request.urlopen(url).read().decode('utf-8')
    res1 = re.findall("<translation><content><!\[CDATA\[([^\]]*)\]\]></content></translation>", html)
    res2 = re.findall("<trans><value><!\[CDATA\[([^\]]*)\]\]></value></trans>", html)
    trans1 =  len(res1) < 2 and "\n".join(res1) or "\n".join(("[{:02}] {}".format(idx,item)) for idx,item in enumerate(res1,start=1))
    trans2 = "\n".join(("[{:02}] {}".format(idx,item)) for idx,item in enumerate(res2,start=1))
    content = ">>> {}".format(queryword)
    if len(trans1)>0:
        content = "{}\n{}\n".format(content, trans1)
    if len(trans2)>0:
        content = "{}\nWeb translation:\n{}".format(content,trans2)
    print(content)

if __name__ == "__main__":
    queryword = "hello" if len(sys.argv) == 1 else sys.argv[1:]
    try:
        fy(queryword)
    except:
        print("404: 服务器响应错误，请稍后再试。。。")




