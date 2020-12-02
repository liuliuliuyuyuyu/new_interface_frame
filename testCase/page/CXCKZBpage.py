
from common import configHttp,common
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


def checkResult(cls,response,setparam):
    """检查结果
    check test result
    :return:
    """
    common.show_return_msg(response)

    cls.assertEqual(response.status_code, int(setparam.code1),msg='Response code error,this time responsed code is：'+str('断言code为：%s' % setparam.code1 + '   响应code为：%s' %response.status_code))
    total = response.json()['data']['total']

    if setparam.result == '0':
        # 先断言是否存在查询数据
        cls.assertNotEqual(total, 0, msg='Response  error，' + str('断言查询数据条数不为：0   响应结果为：%s' % total))
        print('断言查询数据条数不为：0   响应结果为：%s' % total)

        for i in range(total):#最后两行是小计合总计，所以不需要遍历

            #断言出库类型
            info0 = response.json()['data']['rows'][i]['ml_bill_type#bill_type_name']
            cls.assertEqual(info0,setparam.code2,msg='Response  error，'+str('断言出库类型为：%s' % setparam.code2 + '   响应结果为：%s' % info0))
            print('断言出库类型为：%s'%setparam.code2+'   响应结果为：%s'%info0)
