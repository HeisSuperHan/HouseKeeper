from mail.mail import mail
from threading import Thread,Lock
import time
import schedule
from queue import Queue
from logger.log import send_log
from db_manger import db

send_queue = Queue()
email_account = ''
email_password = ''
email_host = ''



def job_1():
    '''
    {
        'xxx@qq.com':[{'miner_id':'miner_data'},...],
        ....
    }
    '''
    task_db = db()
    result = task_db.select_all_miner_info()
    if result['status'] == 0:
        data_list = {}
        for x in result['data']:
            data_list[x[1]] = []
        for y in result['data']:
            data_list[y[1]].append({y[0]:y[2]})
        if data_list:
            global send_queue
            for z in data_list:
                send_queue.put(z)
                return True
        else:
            send_log('job1 没有需要发送的矿机日报')
            return False
    else:
        send_log('job1 获取所有矿机信息失败')
        return False


def job_2(subject):
    global send_queue
    if send_queue.empty():
        send_log('job2 待发送队列为空')
    else:
        print('开始发送邮件')
        task_mail = mail(email_account,email_password,email_host)
        to_address = send_queue.get()
        try:
            task_mail.send_mail(subject,to_address)
            return True
        except Exception as e:
            send_log('job2 尝试发送邮件失败 - '+str(e))
            return False


def main(subject):
    job_1()
    job_2(subject)
    # t1 = Thread(target=job_1)
    # t2 = Thread(target=job_2,args=subject)
    # t1.start()
    # t1.join()
    # t2.start()


def test(z):
    print(z)



schedule.every().day.at('20:30').do(main,'小白秘书日报')
schedule.every().sunday.at('21:30').do(main,'小白秘书周报')


if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.time.sleep(1)


