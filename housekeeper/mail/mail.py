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
        self.random_seed = [0,1,2,3,4,5,6,7,8,9]


    def get_random_number(self):
        try:
            confirm_code1=random.sample(self.random_seed,4)
            confirm_code = ''
            for x in confirm_code1:
                confirm_code += x
            return confirm_code
        except:return False


    def send_mail(self,confirm_code,subject,to_email):
        mail_bot = yagmail.SMTP(user=self.email_account,password=self.email_password,host=self.email_host)
        body = '-来自xxx-：你的验证码是是{confirm_code}'.format(confirm_code=confirm_code)
        try:
            mail_bot.send(to=to_email,subject=subject,contents=[body])
            return True
        except:
            return False
