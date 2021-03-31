import requests, json, time, os, re

cookie = os.environ.get("cookie_zhiyou")

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

def run(*arg):
    msg = ""
    s = requests.Session()
    s.headers.update({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'})

    # 签到
    url = "http://bbs.zhiyoo.net/plugin.php?id=dsu_paulsign:sign&operation=qiandao&infloat=1&inajax=1"
    payload='formhash=f09af3af&qdxq=yl'
    headers = {
        'Connection' : 'keep-alive',
        'Content-Type' : 'application/x-www-form-urlencoded',
        'Origin' : 'http://bbs.zhiyoo.net',
        'Upgrade-Insecure-Requests' : '1',
        'Host' : 'bbs.zhiyoo.net',
        'Referer' : 'http://bbs.zhiyoo.net/plugin.php?id=dsu_paulsign:sign',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language' : 'zh-cn',
        'Accept-Encoding' : 'gzip, deflate',
        'Cookie': cookie
    }
    r = s.post(url, headers=headers, data=payload, verify=False, timeout=120)
    # print(r.text)
    if '成功' in r.text:
        msg += re.compile(r'恭喜你签到成功!获得随机奖励 金币 \d+ 元.').search(r.text)[0]
    elif '' in r.text:
        msg += '您今日已经签到，请明天再来！'
    else:
        msg += '签到失败，可能是cookie失效了！'
        pusher("智友邦  签到失败，可能是cookie失效了！！！", r.text)
    return msg + '\n'

def main(*arg):
    msg = ""
    global cookie
    clist = cookie.split("\n")
    i = 0
    while i < len(clist):
        msg += f"第 {i+1} 个账号开始执行任务\n"
        cookie = clist[i]
        msg += run(cookie)
        i += 1
    print(msg[:-1])
    return msg[:-1]


if __name__ == "__main__":
    if cookie:
        print("----------智友邦开始尝试签到----------")
        main()
        print("----------智友邦签到执行完毕----------")
