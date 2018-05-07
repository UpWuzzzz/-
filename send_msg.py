"""

        这个模块的主要功能是实现微信信息的发送，
        是微信机器人的主要功能。

"""
from auto_login import AUTO_LOGIN
import time ,json

INTERACT_URL = 'https://wx2.qq.com/cgi-bin/mmwebwx-bin'

def send_msg(session ,baseRequest ,myUserName ,toUserName = 'filehelper' ,msg = 'Test messsage'):
    """

            将信息发送给好友，默认文件传输助手。

    """
    url = '%s/webwxsendmsg'%INTERACT_URL
    payloads = {
            'BaseRequest': baseRequest,
            'Msg': {
                'Type': 1,
                'Content': msg,
                'FromUserName': myUserName,
                'ToUserName': (toUserName if toUserName else myUserName),
                'LocalID': int(time.time()),
                'ClientMsgId': int(time.time()),
                },
            'Scene': '0',
            }
    headers = { 'ContentType': 'application/json; charset=UTF-8' }
    session.post(url, data = json.dumps(payloads, ensure_ascii = False), headers = headers)

if __name__ == '__main__':
    user1 = AUTO_LOGIN()
    session, baseRequest, myUserName = user1.login()
    print('登陆成功。')
    send_msg(session, baseRequest, myUserName)
    print('消息发送成功。')