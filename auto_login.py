"""

        该类的主要功能是利用二维码登陆达到网页登陆wechat的目的。

        二维码将会下载到本地或者利用命令行以黑白为底进行输出。

"""

import time ,requests ,re ,os ,threading ,json
import xml.dom.minidom

class AUTO_LOGIN:
    """

        获得二维码图片所需要的请求数据有：
        url = 'https://login.weixin.qq.com/jslogin'
        appid : wx782c26e4c19acffb
        redirect_uri : https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage
        fun : new
        lang : zh_CN
        _ : int(time.time())

    """

    baseRequest = {}

    def __init__(self):
        """

            每一个人有一个id进行标示，即cookies。
            实例化之后自动生成。

        """
        self.session = requests.session()


    def __uuid(self):
        """

            通过发送数据获取二维码图片的标示（uuid）。

        """
        url = 'https://login.weixin.qq.com/jslogin'
        params = {
            'appid' : 'wx782c26e4c19acffb',
            'redirect_uri' : 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage',
            'fun' : 'new',
            'lang' : 'zh_CN',
            '_' : int(time.time()),
        }
        data = self.session.get(url, params = params).text
        code = re.findall('window.QRLogin.code = (.+?);' ,data)[0]
        if(data and code == '200'):
            QRLogin_uuid = re.findall('window.QRLogin.uuid = "(.+?)"' ,data)[0]
        else:
            pass
            self.__uuid()
        return QRLogin_uuid


    def __check(self, uuid):
        """

            向服务器确认用户是否扫描成功，登陆成功以及二维码的状态是否失效。

        """
        url = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login'
        params = {
            'loginicon' : 'true',
            'uuid' : uuid,
            'tip' : '0',
            '_' : int(time.time()),
        }
        code = self.session.get(url, params = params).text
        windows_code = re.findall('window.code=(.*?);' ,code)[0]
        if windows_code == '200':
            window_redirect_uri = re.findall('window.redirect_uri="(.*?)";', code)[0]
            return window_redirect_uri
        elif windows_code == '201':
            return True
        else:
            return False
        return False


    def __qrcode(self, uuid):
        """

            从服务器上获取二维码数据并存放到本地。

        """
        url = 'https://login.weixin.qq.com/qrcode/' + uuid
        r = self.session.get(url, stream = True)
        with open('QRCode.jpg', 'wb') as f:
            f.write(r.content)
        # 模拟双击文件
        os.startfile('QRCode.jpg')


    def __get_login_info(self, url):
        """

            得到一个扫描成功的标示。
            利用dom分析文档结构获得post内容。

        """
        s = self.session.get(url).text
        baseRequest = {}
        for node in xml.dom.minidom.parseString(s).documentElement.childNodes:
            if node.nodeName == 'skey':
                baseRequest['Skey'] = node.childNodes[0].data
            elif node.nodeName == 'wxsid':
                baseRequest['Sid'] = node.childNodes[0].data
            elif node.nodeName == 'wxuin':
                baseRequest['Uin'] = node.childNodes[0].data
            elif node.nodeName == 'pass_ticket':
                baseRequest['DeviceID'] = node.childNodes[0].data
        return baseRequest


    def __web_init(self, baseRequest):
        """

            获取登陆成功返回的数据打包成json数据发送给服务器获取用户信息。

        """
        redirectUri = 'https://wx2.qq.com/cgi-bin/mmwebwx-bin'
        url = '%s/webwxinit?r=%s' % (redirectUri, int(time.time()))
        data = {
            'BaseRequest': baseRequest,
        }
        headers = {'ContentType': 'application/json; charset=UTF-8'}
        r = self.session.post(url, data=json.dumps(data), headers=headers)
        dic = json.loads(r.content.decode('utf-8', 'replace'))

        return dic['User']['UserName']


    def login(self):
        """

            作为一个外部的接口，用来整体调用对象的私有方法。

        """
        QRLogin_uuid = self.__uuid()

        self.__qrcode(QRLogin_uuid)

        while(True):
            if self.__check(QRLogin_uuid):
                baseRequestText = self.__check(QRLogin_uuid) + '&fun=new&version=v2'
                break
            else:
                continue
        AUTO_LOGIN.baseRequest = self.__get_login_info(baseRequestText)

        return self.session ,AUTO_LOGIN.baseRequest ,self.__web_init(AUTO_LOGIN.baseRequest)