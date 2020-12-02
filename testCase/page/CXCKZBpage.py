from common import configHttp
from common.setParameters import configHttp

def query(cls,setparam):
    cls.logger.info("第三步：设置发送请求的参数")
    string = setparam  # 把str类型转换为dict类型
    if 'true' in string:
        string = string.replace('true', 'True')
    if 'false' in string:
        string = string.replace('false', 'False')
    # if 'null' in string:
    #     string = string.replace('null', 'None')
    data = string
    data = eval(data)

    configHttp.set_data(data)
    cls.logger.info("第三步：设置成功，发送的请求参数为： " + str(data))
    # print("第三步：设置成功，发送的请求参数为： " + str(data))
    # test interface        发送请求
    cls.logger.info("第四步：发送请求")
    # print("第四步：发送" + self.setparam.method + "请求")
    response = configHttp.postWithJson()
    return response