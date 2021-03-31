# -*- coding: utf8 -*-

import requests, base64, json, hashlib, os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

netease_username = os.environ.get("netease_username")
netease_password = os.environ.get("netease_password")

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

def encrypt(key, text):
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key.encode('utf8')), modes.CBC(b'0102030405060708'), backend=backend)
    encryptor = cipher.encryptor()
    length = 16                    
    count = len(text.encode('utf-8'))     
    if (count % length != 0):
        add = length - (count % length)
    else:
        add = 16             
    pad = chr(add)
    text1 = text + (pad * add)
    ciphertext = encryptor.update(text1.encode('utf-8')) + encryptor.finalize()      
    cryptedStr = str(base64.b64encode(ciphertext),encoding='utf-8')
    return cryptedStr

def md5(str):
    hl = hashlib.md5()
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()

def protect(text):
    return {"params":encrypt('TA3YiYCfY2dDJQgg',encrypt('0CoJUm6Qyw8W8jud',text)),"encSecKey":"84ca47bca10bad09a6b04c5c927ef077d9b9f1e37098aa3eac6ea70eb59df0aa28b691b7e75e4f1f9831754919ea784c8f74fbfadf2898b0be17849fd656060162857830e241aba44991601f137624094c114ea8d17bce815b0cd4e5b8e2fbaba978c6d1d14dc3d1faf852bdd28818031ccdaaa13a6018e1024e2aae98844210"}

def run(*args):
    try:
        msg = ""
        s=requests.Session()
        url="https://music.163.com/weapi/login/cellphone"
        url2="https://music.163.com/weapi/point/dailyTask"
        url3="https://music.163.com/weapi/v1/discovery/recommend/resource"
        logindata={
            "phone":str(netease_username),
            "countrycode":"86",
            "password":md5(str(netease_password)),
            "rememberLogin":"true",
        }
        headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
                "Referer" : "http://music.163.com/",
                "Accept-Encoding" : "gzip, deflate",
                }
        headers2 = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
                "Referer" : "http://music.163.com/",
                "Accept-Encoding" : "gzip, deflate",
                "Cookie":"os=pc; osver=Microsoft-Windows-10-Professional-build-10586-64bit; appver=2.0.3.131777; channel=netease; __remember_me=true;"
                }

        res=s.post(url=url,data=protect(json.dumps(logindata)),headers=headers2)
        tempcookie=res.cookies
        object=json.loads(res.text)
        if object['code']==200:
            print("登录成功！")
            msg += "登录成功！,"
        else:
            print("登录失败！请检查密码是否正确！"+str(object['code']))
            return "登录失败！请检查密码是否正确！"

        res=s.post(url=url2,data=protect('{"type":0}'),headers=headers)
        object=json.loads(res.text)
        if object['code']!=200 and object['code']!=-2:
            print("签到时发生错误："+object['msg'])
            msg += "签到时发生错误,"
            pusher("网易云音乐签到时发生错误", object['msg'])
        else:
            if object['code']==200:
                print("签到成功，经验+"+str(object['point']))
                msg += "签到成功,"
            else:
                print("重复签到")
                msg += "重复签到,"


        res=s.post(url=url3,data=protect('{"csrf_token":"'+requests.utils.dict_from_cookiejar(tempcookie)['__csrf']+'"}'),headers=headers)
        object=json.loads(res.text,strict=False)
        for x in object['recommend']:
            url='https://music.163.com/weapi/v3/playlist/detail?csrf_token='+requests.utils.dict_from_cookiejar(tempcookie)['__csrf']
            data={
                'id':x['id'],
                'n':1000,
                'csrf_token':requests.utils.dict_from_cookiejar(tempcookie)['__csrf'],
            }
            res=s.post(url,protect(json.dumps(data)),headers=headers)
            object=json.loads(res.text,strict=False)
            buffer=[]
            count=0
            for j in object['playlist']['trackIds']:
                data2={}
                data2["action"]="play"
                data2["json"]={}
                data2["json"]["download"]=0
                data2["json"]["end"]="playend"
                data2["json"]["id"]=j["id"]
                data2["json"]["sourceId"]=""
                data2["json"]["time"]="240"
                data2["json"]["type"]="song"
                data2["json"]["wifi"]=0
                buffer.append(data2)
                count+=1
                if count>=310:
                    break
            if count>=310:
                break
        url = "http://music.163.com/weapi/feedback/weblog"
        postdata={
            "logs":json.dumps(buffer)
        }
        res=s.post(url,protect(json.dumps(postdata)))
        object=json.loads(res.text,strict=False)
        if object['code']==200:
            text = "刷单成功！共"+str(count)+"首"
            print(text)
            msg += text
        else:
            text = "发生错误："+str(object['code'])+object['message']
            print(text)
            msg += text
            pusher("网易云音乐刷歌单时发生错误", object['message'])
    except Exception as e:
        print('repr(e):', repr(e))
        msg += '运行出错,repr(e):'+repr(e)
    return msg + "\n"

def main(*args):
    msg = ""
    global netease_username, netease_password
    ulist = netease_username.split("\n")
    plist = netease_password.split("\n")
    if len(ulist) == len(plist):
        i = 0
        while i < len(ulist):
            msg += f"第 {i+1} 个账号开始执行任务\n"
            netease_username = ulist[i]
            netease_password = plist[i]
            msg += run(netease_username, netease_password)
            i += 1
    else:
        msg = "账号密码个数不相符"
        print(msg)
    return msg


if __name__ == "__main__":
    if netease_username and netease_password:
        print("----------网易云音乐开始尝试执行日常任务----------")
        main()
        print("----------网易云音乐日常任务执行完毕----------")
