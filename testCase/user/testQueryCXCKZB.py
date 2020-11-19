import unittest
import readConfig
from common.Log import MyLog
from common import common
from ddt import ddt,data,unpack
from common.setParameters import setParameters, configHttp

data_dict = common.get_xls("userCase.xlsx", "QueryCXCKZB")         #根据sheet名读取数据，这里就是excel中sheet名为Updatename的数据
localReadConfig = readConfig.ReadConfig()                      #初始化读取配置信息类


@ddt
class QueryCXCKZB(unittest.TestCase):
    def setUp(self):
        """测试开始前的准备工作"""
        self.log = MyLog.get_log()                       #启动log初始化
        self.logger = self.log.get_logger()                  #获取数据
        self.logger.info("测试开始前准备")

    @data(*data_dict)
    def testcase(self, data):
        """出库总表--查询"""
        #初始化
        self.setparam = setParameters.setParameters(self,data)

        self.logger.info("第三步：设置发送请求的参数")
        string = self.setparam.dataExcel # 把str类型转换为dict类型
        if 'true' in string:
            string = string.replace('true', 'True')
        if 'false' in string:
            string = string.replace('false', 'False')
        # if 'null' in string:
        #     string = string.replace('null', 'None')
        data = string
        data = eval(data)

        configHttp.set_data(data)
        self.logger.info("第三步：设置成功，发送的请求参数为： " + str(data))
        print("第三步：设置成功，发送的请求参数为： " + str(data))
        # test interface        发送请求
        self.logger.info("第四步：发送" + self.setparam.method + "请求")
        print("第四步：发送" + self.setparam.method + "请求")
        self.return_json = configHttp.postWithJson()
        method = str(self.return_json.request)[
                 int(str(self.return_json.request).find('[')) + 1:int(str(self.return_json.request).find(']'))]
        self.logger.info("第四步：发送" + method + "请求成功")
        print("第四步：发送" + method + "请求成功")
        # check result         检查结果
        print("*******************************************************************************************************")
        print("检查结果,响应断言")
        self.logger.info("第五步：检查结果,响应断言")

        #响应断言
        self.checkResult()
        print("\n第五步：断言结束")
        self.logger.info("第五步：断言结束")

    def tearDown(self):
        self.log.build_case_line(self.setparam.case_name, self.setparam.msg)
        self.logger.info("*********CASE END*********")
        print("*******************************************************************************************************")
        print("测试结束，输出log完结\n\n")

    def checkResult(self):
        """检查结果
        check test result
        :return:
        """
        self.info = self.return_json
        common.show_return_msg(self.info)

        self.assertEqual(self.return_json.status_code, int(self.code1),msg='Response code error,this time responsed code is：'+str('断言code为：%s' % self.code1 + '   响应code为：%s' %self.info.status_code))
        total = self.info.json()['data']['total']
        total2 = len(self.info.json()['data']['rows'])

        if self.result == '0':
            # 先断言是否存在查询数据
            self.assertNotEqual(total, 0, msg='Response  error，' + str('断言查询数据条数不为：0   响应结果为：%s' % total))
            print('断言查询数据条数不为：0   响应结果为：%s' % total)

            for i in range(total):#最后两行是小计合总计，所以不需要遍历

                #断言出库类型
                info0 = self.info.json()['data']['rows'][i]['ml_bill_type#bill_type_name']
                self.assertEqual(info0,self.setparam.code2,msg='Response  error，'+str('断言出库类型为：%s' % self.setparam.code2 + '   响应结果为：%s' % info0))
                print('断言出库类型为：%s'%self.setparam.code2+'   响应结果为：%s'%info0)

        #         #断言科室
        #         info1 = self.info.json()['data']['rows'][i]['ml_stock_outstore#dept_name']
        #         self.assertEqual(info1, self.code3, msg='Response  error，' + str('断言科室为：%s' % self.code3 + '   响应结果为：%s' % info1))
        #         print('断言科室为：%s' % self.code3 + '   响应结果为：%s' % info1)
        #
        #         # 断言业务时间
        #         info0 = self.info.json()['data']['rows'][i]['ml_stock_outstore#business_time'][0:10]
        #         self.assertEqual(info0, self.code5,
        #                          msg='Response  error，' + str('断言业务日期为：%s' % self.code5 + '   响应结果为：%s' % info0))
        #         print('断言业务日期为：%s' % self.code5 + '   响应结果为：%s' % info0)
        #
        #
        #     #断言小计是否正确
        #     sum_amount1 = 0.0
        #     sum_amount2 = self.info.json()['data']['rows'][total]['sum_amount']
        #     sum_quantity1 = 0.0
        #     sum_quantity2 = self.info.json()['data']['rows'][total]['sum_quantity']
        #     for i in range(total):
        #         sum_amount1 = sum_amount1 + float(self.info.json()['data']['rows'][i]['sum_amount'])
        #         sum_quantity1 = sum_quantity1 + float(self.info.json()['data']['rows'][i]['sum_quantity'])
        #
        #     self.assertEqual(float(sum_amount1),float(sum_amount2), msg='Response  error，' + str('单据总数量为：%s' % sum_amount1 + '   小计总数量为：%s' % sum_amount2))
        #     print('单据总数量为：%s' % sum_amount1 + '   小计总数量为：%s' % sum_amount2)
        #
        #     self.assertEqual(float(sum_quantity1), float(sum_quantity2), msg='Response  error，' + str('单据总金额为：%s' % sum_quantity1 + '   小计总金额为：%s' % sum_quantity2))
        #     print('单据总金额为：%s' % sum_quantity1 + '   小计总金额为：%s' % sum_quantity2)
        #
        #     #断言总计是否正确
        #     sum_amount1 = self.info.json()['data']['rows'][total]['sum_amount']
        #     sum_amount2 = self.info.json()['data']['rows'][total+1]['sum_amount']
        #     self.assertEqual(float(sum_amount1), float(sum_amount2),msg='Response  error，' + str('小计总数量为：%s' % sum_amount1 + '   总计总数量为：%s' % sum_amount2))
        #     print('小计总数量为：%s' % sum_amount1 + '   总计总数量为：%s' % sum_amount2)
        #
        #     sum_quantity1 = self.info.json()['data']['rows'][total]['sum_quantity']
        #     sum_quantity2 = self.info.json()['data']['rows'][total+1]['sum_quantity']
        #     self.assertEqual(float(sum_quantity1), float(sum_quantity2),msg='Response  error，' + str('小计总金额为：%s' % sum_quantity1 + '   总计总金额为：%s' % sum_quantity2))
        #     print('小计总金额为：%s' % sum_quantity1 + '   总计总金额为：%s' % sum_quantity2)
        #
        # elif self.result == '1':
        #     self.assertGreaterEqual(total, 10, msg='Response  error，' + str('断言查询数据条数大于：10' + '   响应结果为：%s' % total))
        #     print('断言查询数据条数大于：10' + '   响应结果为：%s' % total)
        #
        # elif self.result == '2':
        #     self.assertNotEqual(total, 0, msg='Response  error，' + str('断言查询数据条数不为：0   响应结果为：%s' % total))
        #     print('断言查询数据条数不为：0   响应结果为：%s' % total)
        #     for i in range(total2):
        #         if self.info.json()['data']['rows'][i]['ml_stock_outstore#code'] not in ['小计', '总计']:
        #             if self.code2 != 'null':
        #                 info0 = self.info.json()['data']['rows'][i]['ml_bill_type#bill_type_name']
        #                 self.assertEqual(info0, self.code2,
        #                                  msg='Response  error，' + str('断言出库类型为：%s' % self.code2 + '   响应结果为：%s' % info0))
        #                 print('断言出库类型为：%s' % self.code2 + '   响应结果为：%s' % info0)
        #             elif self.code3 != 'null':
        #                 info1 = self.info.json()['data']['rows'][i]['ml_stock_outstore#dept_name']
        #                 self.assertEqual(info1, self.code3,
        #                                  msg='Response  error，' + str('断言科室为：%s' % self.code3 + '   响应结果为：%s' % info1))
        #                 print('断言科室为：%s' % self.code3 + '   响应结果为：%s' % info1)
        #             elif self.code5 != 'null':
        #                 info0 = self.info.json()['data']['rows'][i]['ml_stock_outstore#business_time'][0:10]
        #                 self.assertEqual(info0, self.code5,
        #                                  msg='Response  error，' + str('断言业务日期为：%s' % self.code5 + '   响应结果为：%s' % info0))
        #                 print('断言业务日期为：%s' % self.code5 + '   响应结果为：%s' % info0)
        #
        # elif self.result == '3':
        #     self.assertEqual(total, 0, msg='Response  error，' + str('断言查询条数为：0' + '   响应结果条数为：%s' % total))
        #     print('断言查询条数为：0' + '   响应结果条数为：%s' % total)

