# -*- coding: utf8 -*-

import requests, json, time, os

cookie = os.environ.get("cookie_smzdm")

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

def main(*arg):
    try:
        msg = ""
        s = requests.Session()
        s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'})
        t = round(int(time.time() * 1000))
        url = f'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin?_={t}'

        headers = {
            "cookie" : cookie,
            'Referer': 'https://www.smzdm.com/'
            }

        r = s.get(url, headers=headers, verify=False)
        print(r.text.encode('latin-1').decode('unicode_escape'))
        if r.json()["error_code"] != 0:
            pusher("smzdm  Cookie过期", r.text)
            msg += "smzdm cookie失效"
        else:
            msg += "smzdm签到成功"
    except Exception as e:
        print('repr(e):', repr(e))
        msg += '运行出错,repr(e):'+repr(e)
    return msg + "\n"

def smzdm_pc(*arg):
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
        print("----------什么值得买开始尝试签到----------")
        smzdm_pc()
        print("----------什么值得买签到执行完毕----------")

    
