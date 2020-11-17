import requests
import readConfig
from common.Log import MyLog

localReadConfig = readConfig.ReadConfig()                    #初始化读取配置信息的类


class ConfigHttp:

    def __init__(self):
        global scheme, host, port, timeout                   #通过读取配置信息类中的方法读取配置信息并赋予给定义的变量
        scheme = localReadConfig.get_http("scheme")         #根据配置信息中的名称获取
        host = localReadConfig.get_http("baseurl")          #url地址
        port = localReadConfig.get_http("port")             #端口号
        timeout = localReadConfig.get_http("timeout")       #响应时间
        self.log = MyLog.get_log()                           #Log中Mylog的get_log方法          启动MyLog的get_log方法开启锁，get_log中又启动Log进行初始化
        self.logger = self.log.get_logger()                  #与Log中最底下代码一样
        self.headers = {}                                    #定制请求头（headers），例如：content-type = application/x-www-form-urlencoded
        self.Cookie = {}
        self.params = {}                                     #get方法传递参数，用于传递测试接口所要用的参数，这里我们用python中的字典形式（key：value）进行参数的传递。
        self.data = {}                                       #post方法传递参数
        self.url = None                                      #接口地址
        self.files = {}                                      #上传文件
        self.state = 0                                       #用于上传文件的地址判断 0 为存在，1为空，在set_files设置文件路径中使用
        self.seesion = requests.session()

    def set_url(self, url):
        """拼接完整的url
        set url
        :param: interface url
        :return:
        """
        # print(host)
        # print(port)
        # print(url)
        self.url = scheme+'://'+host+':'+port+'/'+url

        # print("拼接完整的url："+self.url)

    def update_url(self, url):
        """更新url
        update url
        :param: interface url
        :return:
        """
        # print(host)
        # print(port)
        # print(url)
        self.url = url

        # print("*****url******" + self.url + "************")

    def set_headers(self, header):
        """请求头
        set headers
        :param header:
        :return:
        """
        self.headers = header

    def set_Cookie(self, Cookie):
        """Cookie
        set Cookie
        :param Cookie:
        :return:
        """
        self.Cookie = Cookie

    def set_params(self, param):
        """get传递参数
        set params
        :param param:
        :return:
        """
        self.params = param

    def set_data(self, data):
        """post传递参数
        set data
        :param data:
        :return:
        """
        self.data = data

    def set_files(self, filename):
        """上传文件路径设置
        set upload files
        :param filename:
        :return:
        """
        if filename != '':
            file_path = 'D:\1-刘-lyh\亿能达\接口测试框架\testFile\img/' + filename
            self.files = {'file': open(file_path, 'rb')}

        if filename == '' or filename is None:
            self.state = 1

    # defined http get method
    def get(self):
        """get方法
        defined get method
        :return:
        """
        try:                                #request库发送一次get请求
            response = self.seesion.get(self.url, headers=self.headers, timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:                     #超时抛出异常
            self.logger.error("Time out!")
            return None

    # defined http get method
    def getjson(self):
        """get方法
        defined get method
        :return:
        """
        try:  # request库发送一次get请求
            response = self.seesion.get(self.url, headers=self.headers, json=self.data,timeout=float(timeout))
            # response.raise_for_status()
            return response
        except TimeoutError:  # 超时抛出异常
            self.logger.error("Time out!")
            return None


    # defined http post method
    # include get params and post data            包括get参数和post数据
    # uninclude upload file                       不包括上传文件
    def post(self):
        """post方法
        defined post method
        :return:
        """
        try:                                #request库发送一次post请求
            response = self.seesion.post(self.url,headers=self.headers,data=self.data, timeout=float(timeout))
            # response.raise_for_status(),params=self.params
            return response
        except TimeoutError:                       #超时抛出异常
            self.logger.error("Time out!")
            return None

    # defined http post method
    # include upload file                          包括上传文件
    def postWithFile(self):
        """以self.files路径上传文件
        defined post method
        :return:
        """
        try:
            response = self.seesion.post(self.url, headers=self.headers, data=self.data, files=self.files, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # for json
    def postWithJson(self):
        """json格式
        defined post method
        :return:
        """
        try:
            response = self.seesion.post(self.url, headers=self.headers, json=self.data,timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http put method
    # for json
    def putWithJson(self):
        """json格式
        defined post method
        :return:
        """
        try:
            response = self.seesion.put(self.url, headers=self.headers, json=self.data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None


    # defined http post method
    # for json
    def postWithJsondata(self,data):
        """含传参data的json格式
        defined post method
        :return:
        """
        try:
            response = requests.post(self.url, headers=self.headers, json=data,timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None


    # defined http post method
    # for json
    def postWithJsondataurl(self,url,data):
        """含传参data和url的json格式
        defined post method
        :return:
        """
        try:
            response = self.seesion.post(url, headers=self.headers, json=data, timeout=float(timeout))
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None

    # defined http post method
    # for allow_redirects=False
    def postredirects(self):
        """json格式
        defined post method
        :return:
        """
        try:
            response = self.seesion.post(self.url,headers=self.headers,data=self.data, timeout=float(timeout),allow_redirects=False)
            return response
        except TimeoutError:
            self.logger.error("Time out!")
            return None



if __name__ == "__main__":
    print("ConfigHTTP")
