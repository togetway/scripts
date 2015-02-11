# -*- coding: utf-8 -*-
'''
使用飞信接口发送短信通知
第一次启动都需要输入验证码，之前会读取cookies,不用输入认证码
'''
import requests
import chardet
import json, time
from cookielib import LWPCookieJar
 
class fetion(object):
    def __init__(self, phone, passwd):
        self.host = 'http://f.10086.cn'
        self.phone = phone
        self.passwd = passwd
        self.requests = requests.Session()
        self.requests.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36"}
        self.requests.cookies = LWPCookieJar('cookiejar')
        self.id_list = {}  #缓存手机号对应的id
        self.check_login()
        
  
    ##获取自己信息
    def userinfo(self):
        a = str(int(time.time()))
        url = self.host + '/im5/user/selfInfo.action?t=' + a
        data = {'t':a}
        r = self.requests.get(url, data=data)
        return r.text

    def check_login(self):
        if not os.path.exists('cookiejar'):
            self.new_passcode()
        else:
            try:
                self.requests.cookies.load(ignore_discard=True)
                json.loads(self.userinfo())
                print '-- fetion login Success [cookies]'
            except:
                print 'read cookies file failed.'
                self.new_passcode()

    ## 定时访问，保持在线
    def ping(self):
        self.userinfo()
    
    ## 读取验证码
    def new_passcode(self):
        global tm
        tm = str(int(time.time()))
        url = self.host + "/im5/systemimage/verifycode{0}.png?tp=im5&t={0}".format(tm)
        r = self.requests.post(url)
        content = r.content

        imf = 'rand.jpg'
        with open(imf, 'wb') as fw:
            fw.write(content)

        try:
            os.startfile(imf)
        except:
            import Image
            im  = Image.open(imf)
            im.show()
        rand_code = raw_input('Fetion Rand Code:')
        self.login(rand_code)
  
    ## 登陆飞信
    def login(self, rand_code):
        url = self.host + '/im5/login/loginHtml5.action?t=' + tm
        data = {
            'm':self.phone
            ,'pass':self.passwd
            ,'captchaCode':rand_code
            ,'checkCodeKey':'null'      
        }

        r = self.requests.post(url, data=data)
        re = json.loads(r.text)
        if re['tip'] == "":
            print '-- fetion login Success [requests]'
            self.requests.cookies.save(ignore_discard=True)
        else:
            print '-- fetion login Failed'
            self.new_passcode()

    
  
    ## 由飞信号或者手机号码获取id
    def get_id_by_tel(self, tophone):
        url = self.host + "/im5/index/searchFriendsByQueryKey.action"
        data = {
            "queryKey":tophone
        }
        r = self.requests.post(url, data=data)
        try:
            response = json.loads(r.text)
            ret = response.get("contacts",[{}])[0].get("idContact", False)
            return ret
        except Exception, e:
            return False

    ## 发送短信
    def send_msg(self, tophones, msg):
        url = self.host + "/im5/chat/sendNewMsg.action"
        tophones_list = tophones.split(',')

        #获取编码并转为utf-8编码
        code = chardet.detect(msg)
        msg = msg.decode(code['encoding']).encode('utf-8')

        for tophone in tophones_list:
            if tophone in self.id_list and self.id_list[tophone]:
                uid = self.id_list[tophone]
            else:
                uid = self.get_id_by_tel(tophone)
                self.id_list[tophone] = uid
            if uid:
                data = {
                    "touserid":uid,
                    "msg":msg
                }
                r = self.requests.post(url, data=data)
                ret = json.loads(r.text)
                print '-- [%s] %s %s' % (tophone, ret["info"], ret["sendCode"])
            else:
                print '-- [%s] get id error.' %(tophone)

    

if __name__ == "__main__":
    '''
    目前只能发送给飞信好友。
    多个接收者用豆号隔开
    '''
    f = fetion('发送者手机号或飞信号', '密码')
    f.send_msg('接收手机号或者飞信号', '发送内容')