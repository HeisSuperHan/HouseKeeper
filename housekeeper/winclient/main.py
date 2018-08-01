#!/usr/bin/env python


import requests
import re
import json
import uuid
import time

def get_data():
    pth = r'\{.*\}'
    try:
        r = requests.get('http://127.0.0.1:3333',timeout=10)
        re_data = re.search(pth, r.text).group()
        data = json.loads(re_data)
        now_time = int(time.time())
        # 币种
        coin = data['result'][0]
        # 总算力
        all_speed = data['result'][2]
        # 各卡算力
        detail_speed = data['result'][3]
        # 温度转速
        temp_zs = data['result'][6]
        # 矿池
        pool = data['result'][7]
        data_1 = {now_time:[coin,all_speed,detail_speed,temp_zs,pool]}
        return {'status':0,'data':data_1}
    except Exception as e:
        return {'status':-1,'errmsg':str(e)}


def send_data(data):
    url = 'http://118.24.115.49:8888/api/miner'
    headers = {'Content-Type': 'application/json'}
    playload = json.dumps({'data':data})
    logger('playload',playload)
    try:
        r = requests.post(url,headers=headers,data=playload,timeout=10)
        if r.status_code == 200:
            logger('response content:',r.text)
            return {'status':0}
        else:
            logger('response content:',r.text)
            return {'status':-1,'errmsg':r.status_code}
    except Exception as e:
        return {'status':-1,'errmsg':str(e)}



def logger(log_type,logged):
    with open('log.txt','a') as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        f.write(' [-] ')
        f.write(log_type)
        f.write(' [-] ')
        f.write(str(logged))
        f.write('\n')


def auth_user():
    try:
        with open('xiaobai.json', 'r') as f:
            user = f.read()
    except Exception as e:
        return {'status': -1, 'errmsg': str(e)}
    try:
        user_data = json.loads(user)
        return {'status':0,'data':user_data}
    except Exception as e:
        return {'status':-1,'errmsg':str(e)}


def main():
    check_user = auth_user()
    if check_user['status'] == 0:
        print('小白秘书已启动，运行中...')
        miner_id = check_user['data']['miner_id']
        owner = check_user['data']['username']
        while True:
            task_get_data = get_data()
            if task_get_data['status'] == 0:
                need_be_send = {'miner_id':miner_id,'owner':owner,'miner_data':task_get_data['data']}
                task_send_data = send_data(need_be_send)
                if task_send_data['status'] == 0:
                    time.sleep(10)
                else:
                    logger('error',task_send_data)
                    time.sleep(10)
            else:
                logger('error',task_get_data)
                time.sleep(10)
    else:
        # 判断为未登记用户后要求输入邮箱号，并生成登记信息
        username = input('请输入您在小白秘书的邮箱号：')
        miner_id = str(uuid.uuid1())
        register_time = time.time()
        xiaobai = {'username':username,'register_time':register_time,'miner_id':miner_id,'other_data':[]}
        with open('xiaobai.json','w+') as f:
            f.write(json.dumps(xiaobai))
    main()




if __name__ == '__main__':
    main()








