
from flask import Flask,request,make_response,render_template
from flask_cors import CORS
from safe.login_reg_detect import safelogin,saferegister
from authtoken.auth import auth
from db_manger import db
from logger.logger import logger
import json
import uuid
import time
import sqlite3

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/api/register',methods=['POST'])
def register():
    '''
    注册完毕，前端应该转移到登陆页面
    '''
    if saferegister(request):
        username = request.json['username']
        password = request.json['password']
        registertime = int(time.time())
        user_uuid = str(uuid.uuid1())
        create_authtoken = auth(username,user_uuid)
        cookies = create_authtoken.create_cookies()
        token = create_authtoken.create_token()
        task_db = db()
        result = task_db.insert_user(username,password,registertime,user_uuid,cookies,token)
        if result['status'] == 0:
            return json.dumps({'status': 0, 'data': {'username': username}})
        else:
            return json.dumps({'status':-1,'errmsg':'insert database failed'})
    else:
        return json.dumps({'status':-1,'errmsg':'error input data'})


@app.route('/api/login',methods=['POST'])
def login():
    '''
    登陆完毕，前端应该转移到Dashboard页面，api请求/user的相关信息
    '''
    if safelogin(request):
        username = request.json['username']
        password = request.json['password']
        task_db = db()
        result = task_db.auth_username_password(username,password)
        if result['status'] == 0:
            if result['data']:
                get_authtoken = task_db.select_user_authtoken(username)
                if get_authtoken['status'] == 0 and get_authtoken['data']:
                    return json.dumps({'status':0,'data':{'username':username,'cookies':get_authtoken['data']['cookies'],'token':get_authtoken['data']['token']}})
                else:
                    return json.dumps({'status':-1,'errmsg':'get authtoken failed'})
            else:
                return json.dumps({'status':-1,'errmsg':'error username or password'})
        else:
            return json.dumps({'status':-1,'errmsg':'select database failed'})
    else:
        return json.dumps({'status': -1, 'errmsg': 'error input data'})


@app.route('/api/user/<cookies_value>',methods=['GET'])
def user(cookies_value):
    '''
    用户登陆完毕后，api会请求相关信息,矿机数据
    '''
    cookies = cookies_value
    task_db = db()
    result_1 = task_db.select_username_from_cookies(cookies)
    if result_1['status'] == 0:
        username = result_1['data']
        result_2 = task_db.select_miners_from_username(username)
        if result_2['status'] == 0:
            return json.dumps({'status':0,'miners_number':result_2['miners_number'],'data':result_2['data']})
        else:
            return json.dumps({'status':0,'data':0})
    else:
        return json.dumps({'status': -1, 'errmsg': 'db error'})



@app.route('/api/miner',methods=['POST'])
def miner():
    miner_data = request.json
    owner = miner_data['data']['owner']
    miner_id = miner_data['data']['miner_id']
    now_miner_status = miner_data['data']['miner_data']
    task_db = db()
    user_exist = task_db.check_user_miner(owner)      # 确认是否有这个用户
    if user_exist['status'] == 0:
        if user_exist['data']:          # 有这个用户
            try:
                miner_exist = task_db.check_minerid_exist(miner_id)     # 检查是否有这个矿机id
                if miner_exist['data']:        # 矿机已存在  更新矿机状态即可
                    before_status = task_db.select_status_from_miner_id(str(miner_id))['data']
                    for x in now_miner_status:
                        before_status[x] = now_miner_status[x]
                    result = task_db.update_miner_status(str(miner_id),json.dumps(before_status))
                    if result['status'] == 0:
                        return json.dumps({'status':0,'data':'update finished'})
                    else:
                        return json.dumps({'status': -1, 'errmsg': 'db update miner status failed','db:':result})
                else:                            # 矿机id不存在，新矿机，插入第一次矿机数据
                    result = task_db.insert_miner_data(str(miner_id), str(owner), json.dumps(now_miner_status))
                    if result['status'] == 0:
                        return json.dumps({'status': 0, 'data': 'insert finished'})
                    else:
                        return json.dumps({'status': -1, 'errmsg': 'db insert miner status failed','db:':result})
            except Exception as e:
                logger('json miner data', str(e))
                return json.dumps({'status': -1, 'errmsg': str(e)})
        else:
            return json.dumps({'status': -1, 'errmsg': 'this user not exist'})
    else:
        return json.dumps({'status': -1, 'errmsg': 'db error'})




@app.route('/api/miner/info/<miner_id>',methods=['GET'])
def miner_speed(miner_id):
    '''
    根据矿机id，返回前端算力曲线
    '''
    conn = sqlite3.connect('../database/user.db')
    cursor = conn.cursor()
    sql = 'select miner_data from miners where miner_id=?'
    a = cursor.execute(sql,(str(miner_id),))
    b_1 = a.fetchall()
    b = json.loads(b_1[0][0])
    data_list = {'data':{}}
    for x in b:
        data_list['data'][x] = {'Temperature':b[x][3].split(';')[::2],'Calculate_force':b[x][2].split(';'),'Speed':b[x][3].split(';')[1::2]}
    return json.dumps(data_list)


@app.route('/api/admin/login',methods=['POST'])
def admin_login():
    if safelogin(request):
        username = request.json['username']
        password = request.json['password']
        task_db = db()
        result = task_db.auth_admin(username,password)
        if result['status'] == 0:
            if result['data']:
                get_authtoken = task_db.select_admin_authtoken(username)
                if get_authtoken['status'] == 0 and get_authtoken['data']:
                    return json.dumps({'status': 0,'data': {'username': username, 'cookies': get_authtoken['data']['cookies'],'token': get_authtoken['data']['token']}})
                else:
                    return json.dumps({'status': -1, 'errmsg': 'get authtoken failed'})
        else:
            return json.dumps({'status':-1,'errmsg':'select database failed'})
    else:
        return json.dumps({'status': -1, 'errmsg': 'error input data'})



@app.route('/api/admin/<cookies_value>',methods=['GET'])
def admin(cookies_value):
    cookies = cookies_value
    task_db = db()
    a = task_db.auth_admin_cookies(cookies)
    if a['status'] == 0 and a['data']:
        result_1 = task_db.select_users_miners()
        if result_1['status'] == 0:
            users_number = result_1['data']['users']
            miners_number = result_1['data']['miners']
            result_2 = task_db.select_all_miner_info()
            if result_2['status'] == 0:
                result_3 = {}
                for x in result_2['data']:
                    result_3[x[1]] = []
                for y in result_2['data']:
                    result_3[y[1]].append({y[0]:y[2]})
                return json.dumps({'status':0,'user_number':users_number,'miners_number':miners_number,'data':result_3})
            else:
                return json.dumps({'status': -1, 'errmsg': 'error db result 2'})
        else:
            return json.dumps({'status': -1, 'errmsg': 'error db result 1'})
    else:
        return json.dumps({'status':-1,'errmsg':'erroe cookies'})







if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8888)
