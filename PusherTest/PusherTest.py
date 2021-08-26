# -*- coding: utf8 -*-

import requests, sys
sys.path.append('.')
requests.packages.urllib3.disable_warnings()
try:
    from pusher import pusher
except:
    pass

def main(*arg):
    try:
        msg = "这是一条Github Actions测试推送信息"
        testmsg = pusher("测试推送信息", msg)
        print(testmsg)
    except Exception as e:
        print('repr(e):', repr(e))

if __name__ == "__main__":
    print("----------开始执行测试推送----------")
    main()
    print("----------测试推送执行完毕----------")

    
