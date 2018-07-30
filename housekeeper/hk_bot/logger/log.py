import time


def send_log(error_desc):
    with open('log/send_log.txt','a') as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+8*3600)))
        f.write(' [-] ')
        f.write('  描述：')
        f.write(str(error_desc))
        f.write('\n')


def db_log(error_desc):
    with open('log/db_log.txt','a') as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()+8*3600)))
        f.write(' [-] ')
        f.write('  记录：')
        f.write(str(error_desc))
        f.write('\n')

