import unittest
import readConfig
from common.Log import MyLog
from common import common
from ddt import ddt,data,unpack
from common.setParameters import setParameters, configHttp
from testCase.page.CXCKZBpage import query,checkResult

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
        #发送请求数据获取响应数据
        self.return_json = query(self,self.setparam.dataExcel)
        self.logger.info("第四步：发送请求成功")
        # print("第四步：发送请求成功")
        print("*******************************************************************************************************")
        print("检查结果,响应断言")
        self.logger.info("第五步：检查结果,响应断言")
        #响应断言
        checkResult(self,self.return_json,self.setparam)
        print("\n第五步：断言结束")
        self.logger.info("第五步：断言结束")

    def tearDown(self):
        self.log.build_case_line(self.setparam.case_name, self.setparam.msg)
        self.logger.info("*********CASE END*********")
        print("*******************************************************************************************************")
        print("测试结束，输出log完结\n\n")



