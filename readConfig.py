import os
import codecs
import configparser
#将读取配置信息ini的过程封装成一个类
proDir = os.path.split(os.path.realpath(__file__))[0]    #根目录地址相当于这里的接口测试文档框架路径
configPath = os.path.join(proDir, "config.ini")         #存放在根目录下文件名是config.ini的文件，配置文件的完整地址

class ReadConfig():
    def __init__(self):
        fd = open(configPath ,encoding="utf-8")          #打开配置文件
        data = fd.read()               #读取配置文件

        #  remove BOM                  #判断文件中是否有数据
        if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
            file = codecs.open(configPath, "w")
            file.write(data)
            file.close()
        fd.close()

        self.cf = configparser.ConfigParser()   #调用读取配置模块的类
        self.cf.read(configPath,encoding="utf-8")                #读取文件

#获取emall、http、database分组下指定的name值
    def get_email(self, name):
        value = self.cf.get("EMAIL", name)
        return value

    def get_http(self, name):
        value = self.cf.get("HTTP", name)
        return value

    def get_headers(self, name):
        value = self.cf.get("HEADERS", name)
        return value

    def set_headers(self, name, value):
        self.cf.set("HEADERS", name, value)
        with open(configPath, 'w+') as f:
            self.cf.write(f)

    def get_url(self, name):
        value = self.cf.get("URL", name)
        return value

    def get_db(self, name):
        value = self.cf.get("DATABASE", name)
        return value


#修改http分组下指定name的值value   现阶段还未使用
    def set_http(self,name,value):
        cfg = self.cf.set("HTTP",name,value)
        fp = open(r'config.ini','w')
        cfg.write(fp)