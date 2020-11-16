import os
import unittest

import HTMLTestRunner
import HTMLReport
import readConfig
from Log import MyLog
from configEmail import MyEmail

localReadConfig = readConfig.ReadConfig()      #初始化读取配置信息的类

# 执行测试集
class AllTest:
    def __init__(self):
        global log, logger, resultPath, on_off  #初始化变量
        log = MyLog.get_log()                   #启动MyLog的
        # get_log方法开启锁，get_log中又启动Log进行初始化
        logger = log.get_logger()               #获取记录
        resultPath = log.get_report_path()      #生成报告路径
        on_off = localReadConfig.get_email("on_off")  #邮件开关
        self.caseListFile = os.path.join(readConfig.proDir, "caselist.txt")    #设置caselist路径，配置每次执行的case
        self.caseFile = os.path.join(readConfig.proDir, "testCase")            #设置testCase路径
        # self.caseFile = None
        self.caseList = []
        self.email = MyEmail.get_email()                                        #邮件操作

    def set_case_list(self):
        """设置case
        set case list
        :return:
        """
        fb = open(self.caseListFile,encoding='utf-8')                #打开case
        for value in fb.readlines():                #读取case数据
            data = str(value)
            if data != '' and not data.startswith("#"):
                self.caseList.append(data.replace("\n", ""))
        fb.close()                                  #关闭case

    def set_case_suite(self):
        """打开test文件测试
        set case suite
        :return:
        """
        self.set_case_list()
        test_suite = unittest.TestSuite()           #测试套件类    多个独立的测试用例（test case）或者多个独立的测试套件（test suite，可以理解为子套件）可以构成一个测试套件，那么我们写好了一个用例之后，如果去构建一个测试套件呢。下面介绍几种构建测试套件的方法：
                                                    # 通过unittest.TestSuite()类直接构建，或者通过TestSuite实例的addTests、addTest方法构建
        suite_module = []

        for case in self.caseList:                 #通过遍历获取需要执行的case
            case_name = case.split("/")[-1]        #读取的文件名带了user路径，使用split进行分割，[-1]最后一个值
            print(case_name+".py")                 #下面discover是用于批量调用遍历，执行testcase下的test.py文件
            discover = unittest.defaultTestLoader.discover(self.caseFile, pattern=case_name + '.py', top_level_dir=None)
            suite_module.append(discover)

        if len(suite_module) > 0:
                                                #构造测试套件
            for suite in suite_module:
                for test_name in suite:
                    test_suite.addTest(test_name)
        else:
            return None

        return test_suite

    def run(self):
        """执行测试
        run test
        :return:
        """
        try:
            suit = self.set_case_suite()                              #启动测试套件类
            if suit is not None:                                     #判断不为空执行
                logger.info("********TEST START********")          #测试开始的日志打印信息
                # fp = open(resultPath, 'wb')                           #打开报告
                # runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title='Test Report', description='Test Description')
                # runner.run(suit)                                           #写入报告
                runner = HTMLReport.TestRunner(suit)                   #使用HTML
                runner.run()                                           #写入报告
            else:
                logger.info("Have no case to test.")
        except Exception as ex:
            logger.error(str(ex))
        finally:
            logger.info("*********TEST END*********")
            # fp.close()
            # send test report by email                        #根据on_off状态判断要不要发送邮件
            if on_off == 'on':
                self.email.send_email()
            elif on_off == 'off':
                logger.info("Doesn't send report email to developer.")
            else:
                logger.info("Unknow state.")


if __name__ == '__main__':
    obj = AllTest()                    #初始化 runAll 的 AllTest类
    obj.run()                          #执行测试
