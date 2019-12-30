#coding:utf-8
#IgnaleoG server for Luogu PaintBoard
#'https://www.luogu.com.cn/paintBoard'
#'https://www.luogu.com.cn/paintBoard/board'
#Paint 1 pixel every 10 seconds online

portList=[55568,]#本服务器监听端口

import gevent,asyncio
from gevent import monkey
monkey.patch_all()

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import logging
#logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level = logging.INFO,format = '[%(levelname)s] - %(message)s')
logger = logging.getLogger(__name__)

import time,json
from retryapi import retry,RetryExhausted

import tornado.ioloop
import tornado.web
from tornado.platform.asyncio import AsyncIOMainLoop

headers = {
    'User-Agent': 'Destroyer IgnaleoG for civil use',
    'Connection':'keep-alive',
}

with open("cookies.json",'r') as cookiesjson:#[{第一个用户的cookies},{第二个用户的cookies},...]
    cookies=json.load(cookiesjson)

with open("picture.json",'r') as picturejson:
    pic=json.load(picturejson)

RequestExceptions=( #遇到这些异常Exception时重试
    requests.RequestException,
    requests.ConnectionError,
    requests.HTTPError,
    requests.Timeout,
    )
request_timeout=80  #超时设置

def data_generator():#每调用一次next(dataGen)，产生一个需要被画上绘板的像素点
    try:
        for pixel in pic:#pixel==[x.y,c]，横坐标，纵坐标，颜色值
            print('正在作画，像素:',pixel)
            yield {'x':pixel[0],'y':pixel[1],'z':pixel[2]}
    except GeneratorExit:
        print('这很奇怪。程序不应该执行到这里。即将抛出StopIteration')
dataGen=data_generator()


class LPBops:#定义对洛谷绘板(LPB)的操作(ops)。生成的每个LPBops对象对应一个洛谷账号

    def __init__(self,cookies):
        #cookies须为Python字典。可以从你的浏览器获得。
        '''cookie示例:
        {
            "__client_id":"一长串16进制数",
            "UM_distinctid":"更长的一串有横杠'-'的16进制数",
            "_uid":"一个不太长的十进制数",
            "CNZZDATA乱七八糟一大堆":"cnzz_eid%乱七八糟一大堆-乱七八糟一大堆-%26ntime%乱七八糟一大堆"
        }
        '''
        session=requests.Session()
        session.cookies=requests.utils.cookiejar_from_dict(cookies)
        session.headers=headers
        self.session=session

    @retry(exceptions=RequestExceptions,tries=2,logger=None)
    def paint(self,data):
        r=self.session.post("https://www.luogu.com.cn/paintBoard/paint",data=data)
        if(r.text=='{"status":500,"data":"\\u6d3b\\u52a8\\u672a\\u5f00\\u59cb"}'):
            raise Exception('活动尚未开始')
        if(r.text=='{"status":401,"data":"\\u6ca1\\u6709\\u767b\\u5f55"}'):
            raise Exception('cookie无效',self.session.cookies)

    def keep_painting(self):
        try:
            while 1:
                data=next(dataGen)
                self.paint(data)
                gevent.sleep(10)
                #break
        except StopIteration:
            print('整张图片已绘画完成')
        except RetryExhausted:
            print('警告！绘制某个像素点时重试多次仍然失败！',data)

class MainHandler(tornado.web.RequestHandler):#服务器收到HTTP请求后的行为

    def get(self, *args, **kwargs):
        self.write('IgnaleoG：洛谷冬日绘板')

    def post(self, *args, **kwargs):
        pass

worker_loop=asyncio.get_event_loop()
def run_proc(port):
    AsyncIOMainLoop().install()
    app=tornado.web.Application([
        (r'/',MainHandler),
    ])
    app.listen(port)
    print('DestroyerIgnaleoG@localhost:%d'%(port))

    for cookie in cookies:
        operator=LPBops(cookie)
        task=gevent.spawn(operator.keep_painting)
##    注意：可能无法在gevent发起的任务中做debug
    
    # gevent.joinall([gevent.spawn(LPBops(cookie).keep_painting) for cookie in cookies])
    
    worker_loop.run_forever()

if __name__ == '__main__':
    print("本服务器用于在洛谷冬日绘板作画\n参考https://www.luogu.com.cn/paintBoard/board")
    logger.info('本服务器目前的代码并没有发挥它的全部力量，可以说相当于普通单进程工具')
    logger.info('如果修改本服务器的代码，可以通过 HTTP API 动态添加大量异步网络I/O任务。')
    logger.warning('禁止用于CC攻击')
    from multiprocessing import Process
    length=len(portList)
    for port in range(length-1):
        p=Process(target=run_proc, args=(portList[port],))
        p.start()
    run_proc(portList[length-1])
