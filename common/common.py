import requests
import readConfig
import os
import re
from xlrd import open_workbook
from xml.etree import ElementTree as ElementTree
import configHttp
from Log import MyLog
import json

localReadConfig = readConfig.ReadConfig()            #初始化读取配置信息的类
proDir = readConfig.proDir                           #读取配置信息类中，根目录地址相当于这里的接口测试文档框架路径
localConfigHttp = configHttp.ConfigHttp()            #配置接口类，进行接口配置信息初始化
log = MyLog.get_log()                                #启动MyLog的get_log方法开启锁，get_log中又启动Log进行初始化
logger = log.get_logger()                            #获取记录     log最后代码一样

caseNo = 0


def get_visitor_token():
    """为访问者创建一个令牌
    create a token for visitor
    :return:
    """                                                #相当于先用get去获取网站的访问令牌
    host = localReadConfig.get_http("BASEURL")         #获取路径
    port = localReadConfig.get_http("port")             #获取端口
    url = get_url_from_xml('login')              #端口后路径
    response = requests.get(host+':'+port+'/'+url)
    info = response.json()
    token = info.get("info")
    logger.debug("Create token:%s" % (token))
    return token


def set_visitor_token_to_config():
    """将为访问者创建的令牌设置到config中
    set token that created for visitor to config
    :return:
    """
    token_v = get_visitor_token()
    localReadConfig.set_headers("TOKEN_V", token_v)


def get_value_from_return_json(json, name1, name2):
    """通过key获取值
    get value by key
    :param json:                json为响应结果，根据传入的name值查找响应数据中对应的内容
    :param name1:
    :param name2:
    :return:
    """
    info = json['info']
    group = info[name1]
    value = group[name2]
    return value


def show_return_msg(response):
    """显示响应细节
    show msg detail
    :param response:
    :return:
    """
    print("显示响应细节")
    url = response.url
    msg = response.text
    print("\n响应地址："+url)
    # 可以显示中文                                             不使用ascii码而是显示中文    按字典顺序输出  indent 缩进位数
    print("\n请求返回值："+'\n'+json.dumps(json.loads(msg), ensure_ascii=False, sort_keys=True, indent=4))
    # print("\n响应信息：" + '\n' + msg+'\n')

# ****************************** read testCase excel ********************************

def recode(response):
    """从响应中获取断言数据
    :return:
    """
    return re.findall(r'<span class="mr-name">(.+?)</span>', response.text)[0]


def get_xls(xls_name, sheet_name):
    """从excel文件中读取测试用例
    get interface data from xls file
    :return:
    """
    cls = []                                    #存放从xls中获取的数据
    # get xls file's path   获取xls路径
    xlsPath = os.path.join(proDir, "testFile", 'case', xls_name)
    # open xls file         打开xls
    file = open_workbook(xlsPath)
    # get sheet by name     获取sheet
    sheet = file.sheet_by_name(sheet_name)
    # get one sheet's rows   获取sheet的行列
    nrows = sheet.nrows
    if nrows > 1 :
        keys = sheet.row_values(0)
        for i in range(1,nrows):
            value = sheet.row_values(i)
            # if sheet.row_values(i)[0] != u'case_name':
            api_dict = dict(zip(keys,value))
            cls.append(api_dict)
        # print('*****获取的xls文件中的数据*****',cls)
        return cls
    else:
        print("表格无数据")
        return None

# ****************************** read SQL xml ********************************
database = {}     #存放数据库


def set_xml():
    """从SQL.xml文件中读取sql语句
    set sql xml
    :return:
    """
    if len(database) == 0:
        sql_path = os.path.join(proDir, "testFile", "SQL.xml")    #获取xml文件路径
        tree = ElementTree.parse(sql_path)                          #载入数据，通过ElementTree对xml文件进行操作，然后通过我们自定义的方法，根据传递不同的参数取得不（想）同（要）的值。
        for db in tree.findall("database"):                       #查找当前元素下tag或path能够匹配的直系节点。
            db_name = db.get("name")
            # print(db_name)
            table = {}
            for tb in db.getchildren():
                table_name = tb.get("name")
                # print(table_name)
                sql = {}
                for data in tb.getchildren():
                    sql_id = data.get("id")
                    # print(sql_id)
                    sql[sql_id] = data.text
                table[table_name] = sql
            database[db_name] = table
    print('*****获取的xml文件中的sql*****')

def get_xml_dict(database_name, table_name):
    """通过给定的名字得到 存放sql语句的字典，下面会引用set方法
    get db dict by given name
    :param database_name:
    :param table_name:
    :return:
    """
    set_xml()
    database_dict = database.get(database_name).get(table_name)
    print('*****获取存放sql语句字典*****' + database_dict)
    return database_dict


def get_sql(database_name, table_name, sql_id):
    """通过给定的数据库、table名称和sql_id获取sql语句
    get sql by given name and sql_id
    :param database_name:
    :param table_name:
    :param sql_id:
    :return:
    """
    db = get_xml_dict(database_name, table_name)
    sql = db.get(sql_id)
    print('*****获取的sql*****' + sql)
    return sql
# ****************************** read interfaceURL xml ********************************


def get_url_from_xml(name):
    """通过名称从interfaceURL.xml获取url
    By name get url from interfaceURL.xml
    :param name: interface's url name
    :return: url
    """
    url_list = []
    url_path = os.path.join(proDir, 'testFile', 'interfaceURL.xml')    #获取路径
    tree = ElementTree.parse(url_path)                                    #载入数据
    for u in tree.findall('url'):                                        #查找当前元素下tag或path能够匹配的直系节点。
        url_name = u.get('name')                                         #interfaceURL.xml中的url 的 name属性值
        if url_name == name:                                             #interfaceURL.xml中的url 的 name属性值与传入该函数的name比较确定
            for c in u.getchildren():                                    #获取所有子元素并保存到url_list中
                url_list.append(c.text)

    url = '/'.join(url_list)
    # print('*****通过xml文件获取的url后面路径*****'+url)
    return url

if __name__ == "__main__":
    print(get_xls("login"))                                             #从excel表中读取login的数据
    set_visitor_token_to_config()
