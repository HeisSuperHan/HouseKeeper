import sqlite3
from logger.log import db_log

class db():
    def __init__(self):
        self.conn = sqlite3.connect('../database/user.db')
        self.cursor = self.conn.cursor()

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
            db_log('database - select all miner', str(e))
            return {'status': -1, 'errmsg': str(e)}