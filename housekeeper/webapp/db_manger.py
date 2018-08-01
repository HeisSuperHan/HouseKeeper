

import sqlite3
import json
from logger.logger import logger

class db(object):

    def __init__(self):
        self.conn = sqlite3.connect('../database/user.db')
        self.cursor = self.conn.cursor()


    def close_db(self):
        self.cursor.close()
        self.conn.close()

    def insert_user(self,username,password,registertime,user_uuid,cookies,token):
        try:
            sql = 'insert into account values(?,?,?,?,?,?)'
            self.cursor.execute(sql,(username,password,registertime,user_uuid,cookies,token))
            self.conn.commit()
            self.close_db()
            return {'status':0}
        except Exception as e:
            logger('database - insert user',str(e))
            return {'status':-1,'errmsg':str(e)}

    def auth_username_password(self,username,password):
        try:
            sql = 'select password from account where username=?'
            a = self.cursor.execute(sql,(username,))
            b = a.fetchall()[0][0]
            if b == password:
                return {'status':0,'data':True}
            else:
                return {'status':0,'data':False}
        except Exception as e:
            logger('database - select password', str(e))
            return {'status': -1, 'errmsg': str(e)}

    def select_user_authtoken(self,username):
        try:
            sql = 'select cookies,token from account where username=?'
            a = self.cursor.execute(sql,(username,))
            b = a.fetchall()
            cookies = b[0][0]
            token = b[0][1]
            if cookies and token:
                return {'status':0,'data':{'cookies':cookies,'token':token}}
            else:
                return {'status':0,'data':False}
        except Exception as e:
            logger('database - get authtoken', str(e))
            return {'status': -1, 'errmsg': str(e)}


    def select_username_from_cookies(self,cookies):
        sql = 'select username from account where cookies=?'
        try:
            a = self.cursor.execute(sql,(cookies,))
            b = a.fetchall()[0][0]
            if b:
                return {'status':0,'data':b}
            else:
                return {'status':-1}
        except Exception as e:
            logger('database - select username from cookies', str(e))
            return {'status': -1, 'errmsg': str(e)}

    def select_miners_from_username(self,username):
        sql = 'select * from miners where owner=?'
        try:
            a = self.cursor.execute(sql, (username,))
            b = a.fetchall()
            miners_number = len(b)   # 矿机数量
            if b:
                return {'status': 0, 'data': b,'miners_number':miners_number}
            else:
                return {'status': -1}
        except Exception as e:
            logger('database - select username from cookies', str(e))
            return {'status': -1, 'errmsg': str(e)}



    # miner
    def check_user_miner(self,username):
        '''
        客户端向服务端传输数据时的数据有用户名和矿机data，检查account表中是否有这个用户
        '''
        sql = 'select username from account where username=?'
        try:
            a = self.cursor.execute(sql,(username,))
            user_exist = a.fetchall()
            if user_exist:
                return {'status':0,'data':True}
            else:
                return {'status':0,'data':False}
        except Exception as e:
            logger('database - check user miner', str(e))
            return {'status': -1, 'errmsg': str(e)}

    def check_minerid_exist(self,miner_id):
        '''
        查询数据库中是否有这个矿机id，有则可以更新，没有则插入
        '''
        sql = 'select * from miners where miner_id=?'
        try:
            a = self.cursor.execute(sql,(miner_id,))
            user_exist = a.fetchall()
            if user_exist:
                return {'status':0,'data':True}
            else:
                return {'status':0,'data':False}
        except Exception as e:
            logger('database - check_minerid_exist', str(e))
            return {'status': -1, 'errmsg': str(e)}



    def insert_miner_data(self,miner_id,owner,miner_data):
        sql = 'insert into miners values(?,?,?)'
        try:
            self.cursor.execute(sql,(miner_id,owner,miner_data))
            self.conn.commit()
            self.close_db()
            return {'status':0}
        except Exception as e:
            logger('database - insert user',str(e))
            return {'status':-1,'errmsg':str(e)}

    def update_miner_status(self,miner_id,status):
        sql = 'update miners set status=? where miner_id=?'
        try:
            self.cursor.execute(sql,(miner_id,status))
            self.conn.commit()
            self.close_db()
        except Exception as e:
            logger('database - update_miner_status', str(e))
            return {'status': -1, 'errmsg': str(e)}

    def select_status_from_miner_id(self,miner_id):
        sql = 'select miner_data from miners where miner_id=?'
        try:
            a = self.cursor.execute(sql,(miner_id,))
            b = a.fetchall()
            c = b[0][0]
            return {'status':0,'data':json.loads(c)}
        except Exception as e:
            logger('database - select_miner_status_from_miner_id', str(e))
            return {'status': -1, 'errmsg': str(e)}


    # admin
    def auth_admin(self,username,password):
        try:
            sql = 'select password from admin where username=?'
            a = self.cursor.execute(sql,(username,))
            b = a.fetchall()[0][0]
            if b == password:
                return {'status':0,'data':True}
            else:
                return {'status':0,'data':False}
        except Exception as e:
            logger('database - select admin password', str(e))
            return {'status': -1, 'errmsg': str(e)}

    def select_admin_authtoken(self,username):
        try:
            sql = 'select cookies,token from admin where username=?'
            a = self.cursor.execute(sql,(username,))
            b = a.fetchall()
            cookies = b[0][0]
            token = b[0][1]
            if cookies and token:
                return {'status':0,'data':{'cookies':cookies,'token':token}}
            else:
                return {'status':0,'data':False}
        except Exception as e:
            logger('database - get authtoken', str(e))
            return {'status': -1, 'errmsg': str(e)}


    def auth_admin_cookies(self,cookies):
        try:
            sql = 'select * from admin where cookies=?'
            a = self.cursor.execute(sql,(cookies,))
            b = a.fetchall()
            if b:
                return {'status': 0, 'data': True}
            else:
                return {'status': 0, 'data': False}
        except Exception as e:
            logger('database - auth_admin_cookies', str(e))
            return {'status': -1, 'errmsg': str(e)}


    def select_users_miners(self):
        '''
        统计用户数以及矿机数
        '''
        user_sql = 'select username from account'
        miner_sql = 'select miner_id from miners'
        try:
            a = self.cursor.execute(user_sql)
            b = len(a.fetchall())
            c = self.cursor.execute(miner_sql)
            d = len(c.fetchall())
            return {'status':0,'data':{'users':b,'miners':d}}
        except Exception as e:
            logger('database - select user miner', str(e))
            return {'status': -1, 'errmsg': str(e)}


    def select_all_miner_info(self):
        '''
        查找所有矿机信息
        '''
        sql = 'select * from miners'
        try:
            a = self.cursor.execute(sql)
            b = a.fetchall()
            return {'status':0,'data':b}
        except Exception as e:
            logger('database - select all miner', str(e))
            return {'status': -1, 'errmsg': str(e)}














