# coding:utf-8

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import threading
import readConfig as readConfig
from Log import MyLog
import zipfile
import glob

localReadConfig = readConfig.ReadConfig()                               #初始化读取配置信息的类


class Email:
    def __init__(self):                                                #初始化email配置信息
        global host, user, password, port, sender, title
        host = localReadConfig.get_email("mail_host")
        user = localReadConfig.get_email("mail_user")
        password = localReadConfig.get_email("mail_pass")
        port = localReadConfig.get_email("mail_port")
        sender = localReadConfig.get_email("sender")
        title = localReadConfig.get_email("subject")
        # content = localReadConfig.get_email("content")

        # get receiver list
        self.value = localReadConfig.get_email("receiver")            #获取接收邮箱
        self.receiver = []                                             #可能有多个邮箱，用列表存储
        for n in str(self.value).split("/"):
            self.receiver.append(n)

        # defined email subject
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")         #定义电子邮件主题
        self.subject = "接口测试报告" + " " + date                    #邮件名

        self.log = MyLog.get_log()
        self.logger = self.log.get_logger()
        self.msg = MIMEMultipart('related')                          #生成包括多个部分的邮件   邮件中有多个附件

    def config_header(self):
        """定义的电子邮件头包括主题，发件人和收件人
        defined email header include subject, sender and receiver
        :return:
        """
        self.msg['subject'] = self.subject                           #主题
        self.msg['from'] = sender                                    #发件人
        self.msg['to'] = ";".join(self.receiver)                     #收件人

    def config_content(self):
        """写电子邮件的内容
        write the content of email
        :return:
        """
        f = open(os.path.join(readConfig.proDir, 'testFile', 'emailStyle.txt'),encoding="utf-8")
        content = f.read()
        f.close()
        content_plain = MIMEText(content, 'html', 'UTF-8')
        self.msg.attach(content_plain)
        self.config_image()

    def config_image(self):
        """内容使用的配置图片
        config image that be used by content
        :return:
        """
        # defined image path  定义图像路径
        image1_path = os.path.join(readConfig.proDir, 'testFile', 'img', '测试账户.png')
        #打开图像路径
        fp1 = open(image1_path, 'rb')
        msgImage1 = MIMEImage(fp1.read())
        # self.msg.attach(msgImage1)
        fp1.close()

        # defined image id     定义图片名
        msgImage1.add_header('Content-ID', '<image1>')
        msgImage1["Content-Disposition"] = 'attachment; filename="testimage.png"'      #把图片文件格式从bin变成可识别的格式
        self.msg.attach(msgImage1)

        #第二张图片或其他附件，需要时再添加
        # image2_path = os.path.join(readConfig.proDir, 'testFile', 'img', 'logo.jpg')
        # fp2 = open(image2_path, 'rb')
        # msgImage2 = MIMEImage(fp2.read())
        # # self.msg.attach(msgImage2)
        # fp2.close()
        #
        # # defined image id     定义图片名
        # msgImage2.add_header('Content-ID', '<image2>')
        # self.msg.attach(msgImage2)

    def config_file(self):
        """配置邮件文件
        config email file
        :return:
        """

        # if the file content is not null, then config the email file          如果文件内容不为空，则配置电子邮件文件
        if self.check_file():

            reportpath = self.log.get_result_path()                             #在result中生成的test.zip文件
            zippath = os.path.join(readConfig.proDir, "result", "test.zip")

            # zip file
            files = glob.glob(reportpath + '\*')
            f = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
            for file in files:
                # 修改压缩文件的目录结构
                f.write(file, '/report/'+os.path.basename(file))
            f.close()

            reportfile = open(zippath, 'rb').read()                             #发送邮箱附件的test.zip文件
            filehtml = MIMEText(reportfile, 'base64', 'utf-8')
            filehtml['Content-Type'] = 'application/octet-stream'
            filehtml['Content-Disposition'] = 'attachment; filename="test.zip"'
            self.msg.attach(filehtml)

    def check_file(self):
        """检查测试报告
        check test report
        :return:
        """
        reportpath = self.log.get_report_path()
        if os.path.isfile(reportpath) and not os.stat(reportpath) == 0:
            return True
        else:
            return False

    def send_email(self):
        """发送邮件
        send email
        :return:
        """
        self.config_header()
        self.config_content()
        self.config_file()
        try:                                        #设置smtp信息
            smtp = smtplib.SMTP()
            smtp.connect(host)
            smtp.login(user, password)
            smtp.sendmail(sender, self.receiver, self.msg.as_string())
            smtp.quit()
            self.logger.info("The test report has send to developer by email.")                #发送成功提示
        except Exception as ex:
            self.logger.error(str(ex))


class MyEmail:
    email = None
    mutex = threading.Lock()                 #线程锁

    def __init__(self):
        pass

    @staticmethod
    def get_email():

        if MyEmail.email is None:
            MyEmail.mutex.acquire()           #线程调用acquire方法获得锁，锁进入locked状态
            MyEmail.email = Email()           #启动Email初始化
            MyEmail.mutex.release()
        return MyEmail.email


if __name__ == "__main__":
    email = MyEmail.get_email()
