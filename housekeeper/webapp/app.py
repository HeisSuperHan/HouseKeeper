
from flask import Flask,request,make_response
from safe.login_reg_detect import safelogin,saferegister
from authtoken.auth import auth
from db_manger import db
from logger.logger import logger
import json
import uuid
import time

app = Flask(__name__)


@app.route('/')
def index():
    pass



@app.route('/register',methods=['POST'])
def register():
    '''
    注册完毕，前端应该转移到登陆页面
    '''
    if saferegister(request):
        username = request.form['username']
        password = request.form['password']
        registertime = int(time.time())
        user_uuid = str(uuid.uuid1())
        create_authtoken = auth(username,user_uuid)
        cookies = create_authtoken.create_cookies()
        token = create_authtoken.create_token()
        task_db = db()
        result = task_db.insert_user(username,password,registertime,user_uuid,cookies,token)
        if result['status'] == 0:
            rtp = make_response(json.dumps({'status': 0, 'data': {'username': username}}))
            rtp.headers['Access-Control-Allow-Origin'] = '*'
            return rtp
        else:
            rtp = make_response(json.dumps({'status':-1,'errmsg':'insert database failed'}))
            rtp.headers['Access-Control-Allow-Origin'] = '*'
            return rtp
    else:
        rtp = make_response(json.dumps({'status':-1,'errmsg':'error input data'}))
        rtp.headers['Access-Control-Allow-Origin'] = '*'
        return rtp


@app.route('/login',methods=['POST'])
def login():
    '''
    登陆完毕，前端应该转移到Dashboard页面，api请求/user的相关信息
    '''
    if safelogin(request):
        username = request.form['username']
        password = request.form['password']
        task_db = db()
        result = task_db.auth_username_password(username,password)
        if result['status'] == 0:
            if result['data']:
                get_authtoken = task_db.select_user_authtoken(username)
                if get_authtoken['status'] == 0 and get_authtoken['data']:
                    rtp = make_response(json.dumps({'status':0,'data':{'username':username,'cookies':get_authtoken['data']['cookies'],'token':get_authtoken['data']['token']}}))
                    rtp.headers['Access-Control-Allow-Origin'] = '*'
                    return rtp
                else:
                    rtp = make_response(json.dumps({'status':-1,'errmsg':'get authtoken failed'}))
                    rtp.headers['Access-Control-Allow-Origin'] = '*'
                    return rtp
            else:
                rtp = make_response(json.dumps({'status':-1,'errmsg':'error username or password'}))
                rtp.headers['Access-Control-Allow-Origin'] = '*'
                return rtp
        else:
            rtp = make_response(json.dumps({'status':-1,'errmsg':'select database failed'}))
            rtp.headers['Access-Control-Allow-Origin'] = '*'
            return rtp
    else:
        rtp = make_response(json.dumps({'status': -1, 'errmsg': 'error input data'}))
        rtp.headers['Access-Control-Allow-Origin'] = '*'
        return rtp


@app.route('/user',methods=['GET'])
def user():
    '''
    用户登陆完毕后，api会请求相关信息,矿机数据
    '''
    cookies = request.cookies['user_cookies']
    task_db = db()
    result_1 = task_db.select_username_from_cookies(cookies)
    if result_1['status'] == 0:
        username = result_1['data']
        result_2 = task_db.select_miners_from_username(username)
        if result_2['status'] == 0:
            rtp = make_response(json.dumps({'status':0,'miners_number':result_2['miners_number'],'data':result_2['data']}))
            rtp.headers['Access-Control-Allow-Origin'] = '*'
            return rtp
        else:
            rtp = make_response(json.dumps({'status':0,'data':0}))
            rtp.headers['Access-Control-Allow-Origin'] = '*'
            return rtp
    else:
        rtp = make_response(json.dumps({'status': -1, 'errmsg': 'db error'}))
        rtp.headers['Access-Control-Allow-Origin'] = '*'
        return rtp



@app.route('/miner',methods=['POST'])
def miner():
    username = request.form['username']
    miner_data = request.form['data']
    miner_info = request.form['user_info']
    task_db = db()
    user_exist = task_db.check_user_miner(username)
    if user_exist['status'] == 0:
        if user_exist['data']:
            try:
                miner_id = json.loads(miner_info)['miner_id']
                owner = username
                miner_data = {'data':json.loads(miner_data),'info':json.loads(miner_info)}
                result = task_db.insert_miner_data(miner_id,owner,miner_data)
                if result['status'] == 0:
                    rtp = make_response(json.dumps({'status':0,'data':'insert finished'}))
                    rtp.headers['Access-Control-Allow-Origin'] = '*'
                    return rtp
                else:
                    rtp = make_response(json.dumps({'status': -1, 'errmsg': 'db insert miner failed'}))
                    rtp.headers['Access-Control-Allow-Origin'] = '*'
                    return rtp
            except Exception as e:
                logger('json miner data', str(e))
                rtp = make_response(json.dumps({'status': -1, 'errmsg': str(e)}))
                rtp.headers['Access-Control-Allow-Origin'] = '*'
                return rtp
        else:
            rtp = make_response(json.dumps({'status': -1, 'errmsg': 'this user not exist'}))
            rtp.headers['Access-Control-Allow-Origin'] = '*'
            return rtp
    else:
        rtp = make_response(json.dumps({'status': -1, 'errmsg': 'db error'}))
        rtp.headers['Access-Control-Allow-Origin'] = '*'
        return rtp




@app.route('/admin/login',methods=['POST'])
def admin_login():
    if safelogin(request):
        username = request.form['username']
        password = request.form['password']
        task_db = db()
        result = task_db.auth_admin(username,password)
        if result['status'] == 0:
            if result['data']:
                get_authtoken = task_db.select_admin_authtoken(username)
                if get_authtoken['status'] == 0 and get_authtoken['data']:
                    rtp = make_response(json.dumps({'status': 0,'data': {'username': username, 'cookies': get_authtoken['data']['cookies'],'token': get_authtoken['data']['token']}}))
                    rtp.headers['Access-Control-Allow-Origin'] = '*'
                    return rtp
                else:
                    rtp = make_response(json.dumps({'status': -1, 'errmsg': 'get authtoken failed'}))
                    rtp.headers['Access-Control-Allow-Origin'] = '*'
                    return rtp
        else:
            rtp = make_response(json.dumps({'status':-1,'errmsg':'select database failed'}))
            rtp.headers['Access-Control-Allow-Origin'] = '*'
            return rtp
    else:
        rtp = make_response(json.dumps({'status': -1, 'errmsg': 'error input data'}))
        rtp.headers['Access-Control-Allow-Origin'] = '*'
        return rtp



@app.route('/admin',methods=['POST'])
def admin():
    task_db = db()
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
            rtp = make_response(json.dumps({'status':0,'user_number':users_number,'miners_number':miners_number,'data':result_3}))
            rtp.headers['Access-Control-Allow-Origin'] = '*'
            return rtp
        else:
            rtp = make_response(json.dumps({'status': -1, 'errmsg': 'error db result 2'}))
            rtp.headers['Access-Control-Allow-Origin'] = '*'
            return rtp
    else:
        rtp = make_response(json.dumps({'status': -1, 'errmsg': 'error db result 1'}))
        rtp.headers['Access-Control-Allow-Origin'] = '*'
        return rtp







if __name__ == '__main__':
    app.run()
