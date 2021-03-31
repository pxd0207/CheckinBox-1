# -*- coding: utf8 -*-

import requests, os
from bs4 import BeautifulSoup

cookie = os.environ.get('cookie_52pj')

def pusher(*args):
    msg = args[0]
    othermsg = ""
    for i in range(1, len(args)):
        othermsg += args[i]
        othermsg += "\n"
    SCKEY = os.environ.get('SCKEY') # http://sc.ftqq.com/
    SCTKEY = os.environ.get('SCTKEY') # http://sct.ftqq.com/
    Skey = os.environ.get('Skey') # https://cp.xuthus.cc/
    Smode = os.environ.get('Smode') # send, group, psend, pgroup, wx, tg, ww, ding(no send email)
    pushplus_token = os.environ.get('pushplus_token') # http://www.pushplus.plus/
    pushplus_topic = os.environ.get('pushplus_topic') # pushplus一对多推送需要的"群组编码"，一对一推送不用管
    if SCKEY:
        sendurl = f"https://sc.ftqq.com/{SCKEY}.send"
        data = {
            "text" : msg,
            "desp" : othermsg
            }
        requests.post(sendurl, data=data)
    if SCTKEY:
        sendurl = f"https://sctapi.ftqq.com/{SCTKEY}.send"
        data = {
            "title" : msg,
            "desp" : othermsg
            }
        requests.post(sendurl, data=data)
    if pushplus_token:
        sendurl = "http://www.pushplus.plus/send"
        if not othermsg:
            othermsg = msg
        if pushplus_topic:
            params = {
            "token" : pushplus_token,
            "title" : msg,
            "content" : othermsg,
            "template" : "html",
            "topic" : pushplus_topic
            }
        else:
            params = {
                "token" : pushplus_token,
                "title" : msg,
                "content" : othermsg,
                "template" : "html"
            }
        r = requests.post(sendurl, params=params)
        print(r.json())
        if r.json()["code"] != 200:
            print(f"pushplus推送失败！{r.json()['msg']}")
    if Skey:
        if not Smode:
            Smode = 'send'
        if othermsg:
            msg = msg + "\n" + othermsg
        sendurl = f"https://push.xuthus.cc/{Smode}/{Skey}"
        params = {"c" : msg}
        requests.post(sendurl, params=params)

def main(*args):
    try:
        msg = ""
        s = requests.Session()
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'Cookie': cookie,
            'ContentType':'text/html;charset=gbk'
        }
        s.get('https://www.52pojie.cn/home.php?mod=task&do=apply&id=2', headers=headers)
        a = s.get('https://www.52pojie.cn/home.php?mod=task&do=draw&id=2', headers=headers)
        b = BeautifulSoup(a.text,'html.parser')
        c = b.find('div',id='messagetext').find('p').text

        if "您需要先登录才能继续本操作"  in c:
            pusher("52pojie  Cookie过期", c)
            print("cookie_52pj失效，需重新获取")
            msg += "cookie_52pj失效，需重新获取"
        elif "恭喜"  in c:
            print("52pj签到成功")
            msg += "52pj签到成功"
        else:
            print(c)
    except:
        if "防护" in b:
            print("触发52pj安全防护，访问出错。自行修改脚本运行时间和次数，总有能访问到的时间")
        # print(b)
        print("52pj出错")
        msg += "52pj出错"
    return msg + "\n"

def pjCheckin(*args):
    msg = ""
    global cookie
    clist = cookie.split("\n")
    i = 0
    while i < len(clist):
        msg += f"第 {i+1} 个账号开始执行任务\n"
        cookie = clist[i]
        msg += main(cookie)
        i += 1
    return msg

if __name__ == "__main__":
    if cookie:
        print("----------52pojie开始尝试签到----------")
        pjCheckin()
        print("----------52pojie签到执行完毕----------")
