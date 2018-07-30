import yagmail
import random

class mail():
    '''
    发送邮件验证码的邮件对象，验证码为0-9的四位随机整数
    '''

    def __init__(self,email_account,email_password,host):
        self.email_account = email_account
        self.email_password = email_password
        self.email_host = host


    def send_mail(self,subject,to_email):
        mail_bot = yagmail.SMTP(user=self.email_account,password=self.email_password,host=self.email_host)
        body = '''
            <html>
                <h5>小白秘书，矿机日报</h5>
            </html>
        '''
        try:
            mail_bot.send(to=to_email,subject=subject,contents=[body])
            return True
        except:
            return False
