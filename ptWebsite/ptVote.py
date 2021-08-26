# -*- coding: utf8 -*-

import requests, os, sys, json
sys.path.append('.')
requests.packages.urllib3.disable_warnings()
try:
    from pusher import pusher
except:
    def pusher(*args):
        pass

cookie = os.environ.get("cookie_pt")
pt_website = os.environ.get("pt_website")

def main(cookie, website):
    s = requests.Session()
    if os.path.exists("./ptconfig.json"):
        with open('ptconfig.json', 'r', encoding="utf8") as f:
            data = json.load(f)
        try:
            vote_id = data[website]["vote_id"]
            if vote_id == "disable":
                return f"{website} 不需要投票\n"
        except:
            try:
                data[website]["vote_id"] = "disable"
            except:
                data[website] = {}
                data[website]["vote_id"] = "disable"
            with open('./ptconfig.json', 'w', encoding="utf8") as f:
                json.dump(data, f, ensure_ascii=False)
            return f"{website} 投票初始化，自行修改起始投票id才会开始投票\n"
    else:
        try:
            data = {}
            data[website] = {}
            data[website]["vote_id"] = "disable"
            with open('./ptconfig.json', 'w', encoding="utf8") as f:
                json.dump(data, f, ensure_ascii=False)
            return f"{website} 投票初始化，自行修改起始投票id才会开始投票\n"
        except:
            msg = "warning::: 无法写入ptconfig.json,请使用有读写权限的环境运行脚本\n"
            print(msg)
            pusher(msg, msg)
            return msg
    url = f'{website.replace("index.php", "fun.php")}?action=vote&id={vote_id}&yourvote=fun'

    headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
            'Cookie' : cookie,
            'Content-type': 'text/html; charset=utf-8; Cache-control:private',
            'Referer': website,
            }

    r = s.get(url, headers=headers, verify=False)
    data[website]["vote_id"] = int(vote_id) + 1
    if not r.text:
        msg = "趣味盒投票有趣"
        with open('./ptconfig.json', 'w', encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False)
    elif "你已经投过票了！" in r.text:
        msg = "你已经投过票了！"
        with open('./ptconfig.json', 'w', encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False)
    elif "无效的ID" in r.text:
        msg = "无效的ID"
    else:
        msg = "cookie失效"
        pusher(f"PT站点{website} Cookie过期", r.text[:200])
    return msg + '\n'

def main_handler(*args):
    msg = ""
    global cookie, pt_website
    if "\\n" in cookie:
        clist = cookie.split("\\n")
        weblist = pt_website.split("\\n")
    else:
        clist = cookie.split("\n")
        weblist = pt_website.split("\n")
    i = 0
    while i < len(clist):
        msg += f"第 {i+1} 个网站开始执行任务\n"
        cookie = clist[i]
        website = weblist[i]
        msg += main(cookie, website)
        i += 1
    return msg[:-1]      

if __name__ == "__main__":
    if cookie:
        print("----------PTwebsite_Vote开始尝试签到----------")
        print(main_handler())
        print("----------PTwebsite_Vote签到执行完毕----------")
