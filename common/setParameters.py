from common import configHttp
import readConfig
from common.BasePage import BasePage

localReadConfig = readConfig.ReadConfig()                      #初始化读取配置信息类
configHttp = configHttp.ConfigHttp()                           #初始化http信息


class setParameters:
    def setParameters(cls,data):
        '''
       定义变量接收值
       '''
        print("*******************************************************************************************************")
        if '用例名' in data:
            cls.case_name = str(data['用例名'])
            setParameters.dataprint('测试用例数据：%s' % cls.case_name)
        if 'result' in data:
            cls.result = str(data['result'])
        if 'method' in data:
            cls.method = str(data['method'])  # 请求方法
        if 'url' in data:
            cls.url = str(data['url'])
        if 'code1' in data:
            cls.code1 = str(data['code1'])
        if 'code2' in data:
            cls.code2 = str(data['code2'])
            setParameters.dataprint(cls.code2)
        if 'code3' in data:
            cls.code3 = str(data['code3'])
            setParameters.dataprint(cls.code3)
        if 'code4' in data:
            cls.code4 = str(data['code4'])
            setParameters.dataprint(cls.code4)
        if 'code5' in data:
            cls.code5 = str(data['code5'])
            setParameters.dataprint(cls.code5)
        if 'code6' in data:
            cls.code6 = str(data['code6'])
            setParameters.dataprint(cls.code6)
        if 'code7' in data:
            cls.code7 = str(data['code7'])
            setParameters.dataprint(cls.code7)
        if 'code8' in data:
            cls.code8 = str(data['code8'])
            setParameters.dataprint(cls.code8)
        if 'code9' in data:
            cls.code9 = str(data['code9'])
            setParameters.dataprint(cls.code9)
        if 'code10' in data:
            cls.code10 = str(data['code10'])
            setParameters.dataprint(cls.code10)
        if 'code11' in data:
            cls.code11 = str(data['code11'])
            setParameters.dataprint(cls.code11)
        if 'code12' in data:
            cls.code12 = str(data['code12'])
            setParameters.dataprint(cls.code12)
        if 'code13' in data:
            cls.code13 = str(data['code13'])
            setParameters.dataprint(cls.code13)
        if 'code14' in data:
            cls.code14 = str(data['code14'])
            setParameters.dataprint(cls.code14)
        if 'msg' in data:
            cls.msg = str(data['msg'])
        if 'data' in data:
            cls.dataExcel = str(data['data'])
        if 'data2' in data:
            cls.dataExcel2 = str(data['data2'])
        if 'data3' in data:
            cls.dataExcel3 = str(data['data3'])
        if 'data4' in data:
            cls.dataExcel4 = str(data['data4'])
        if 'data5' in data:
            cls.dataExcel5 = str(data['data5'])
        if 'data6' in data:
            cls.dataExcel6 = str(data['data6'])

        cls.data = {}  # 保存传输data数据
        cls.return_json = None  # 保存响应信息
        cls.info = None  # 返回json格式的响应信息

        print("第一步：设置访问的url")
        # cls.logger.info("第一步：设置访问的url")
        configHttp.set_url(cls.url)
        print("第一步：设置成功，访问的url为： " + configHttp.url)
        print("第二步：设置header(token等)")
        # cls.logger.info("第一步：设置成功，访问的url为： " + configHttp.url)
        # cls.logger.info("第二步：设置header(token等)")
        token = localReadConfig.get_headers("User-Agent")
        Authentication = BasePage.login()
        # set headers         设置请求头
        # respone = requests.get('http://114.115.173.141:8080/')
        headers = {
            "User-Agent": str(token),
            "Authentication": str(Authentication)
        }
        configHttp.set_headers(headers)
        # set Cookie          设置Cookie
        # Cookie = {"JSESSIONID":str(respone)}
        # cls.logger.info("第二步：设置成功，访问的header为： " + str(headers))

        return cls

    @staticmethod
    def dataprint(data):
        print(data)
        # logger.info(data)