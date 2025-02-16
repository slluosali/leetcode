#coding=utf-8
import pymysql
from loghandle import logger
import settings
import sys

class MysqlService(object):
    """
    table list
    """
    ACCOUNT_INFO_TABLE = 'account_info'
    USER_LC_DAILY_INFO_TABLE = 'user_lc_daily_info'
    USER_LC_DAILY_INFO_FIELDS = ['user', 'total_solve', 'code_submit', 
            'problem_submit', 'rating_score', 'continue_days',
            'new_solve', 'date_time']
    ACCOUNT_INFO_FIELDS = ['user', 'git_account', 'medal', 'award', 'email']

    def __init__(self):
        self.port = 3306
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = 'qscool'
        self.db = 'leetcode'
        self.conn = None
        self.cur = None

    def _connect_mysql(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                db=self.db,
                port=self.port
                )
            self.cur = self.conn.cursor()
            return True
        except Exception as e:
            logger.error(e)
            self.conn = None
            self.cur = None
            return False
    
    def add_user_daily_info(self, date, datalist):
        if not self._connect_mysql():
            return False
        presql = "insert into " + self.USER_LC_DAILY_INFO_TABLE
        presql += " (" + ",".join(self.USER_LC_DAILY_INFO_FIELDS) + ")"   
        for data in datalist:
            user = data[0]
            total = int(data[1])
            code_submit = int(data[2])
            problem_submit = int(data[3])
            score = int(data[4])
            days = int(data[5])
            new_solve = int(data[6])
            sql = presql + "values ('%s',%s, %s, %s, %s, %s, %s, '%s')" % \
                (user, total, code_submit, problem_submit, score, \
                    days, new_solve, date)
            logger.info(sql)
            try:
                self.cur.execute(sql)
                self.conn.commit()
            except Exception as e:
                logger.error(e)
                self.conn.rollback()
                self.cur.close()
                self.conn.close()
                return False
        self.cur.close()
        self.conn.close()
        return True
    
    def add_single_user_daily_info(self, date, data):
        if not self._connect_mysql():
            return False
        presql = "insert into " + self.USER_LC_DAILY_INFO_TABLE
        presql += " (" + ",".join(self.USER_LC_DAILY_INFO_FIELDS) + ")"   
        user = data[0]
        total = int(data[1])
        code_submit = int(data[2])
        problem_submit = int(data[3])
        score = int(data[4])
        days = int(data[5])
        new_solve = int(data[6])
        sql = presql + "values ('%s',%s, %s, %s, %s, %s, %s, '%s')" % \
            (user, total, code_submit, problem_submit, score, \
                days, new_solve, date)
        logger.info(sql)
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            self.cur.close()
            self.conn.close()
            return False
        self.cur.close()
        self.conn.close()
        return True
    
    def update_single_user_daily_info(self, date, data):
        user = data[0]
        if not self._connect_mysql():
            return False
        sql = "update " + self.USER_LC_DAILY_INFO_TABLE + " set \
            total_solve=%s, code_submit=%s, problem_submit=%s, rating_score=%s, \
            continue_days=%s, new_solve=%s where user = '%s' and  date_time ='%s'" % (data[1],\
            data[2], data[3], data[4], data[5], data[6], data[0], date)
        try:
            self.cur.execute(sql)
            self.conn.commit()
            self.cur.close()
            self.conn.close()
            return True
        except Exception as e:
            logger.error(e)
            self.cur.close()
            self.conn.close()
            return False

    def serach_single_user_daily_info(self, user, date):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.USER_LC_DAILY_INFO_FIELDS) + \
            " from " + self.USER_LC_DAILY_INFO_TABLE + \
            " where user = '%s' and date_time = '%s'" % (user, date)
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            self.cur.close()
            self.conn.close()
            if len(data) > 0:
                return data[0]
            return None
        except Exception as e:
            logger.error(e)
            self.cur.close()
            self.conn.close()
            return None

    def load_all_user_daily_info_by_day(self, date):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.USER_LC_DAILY_INFO_FIELDS) + \
            " from " + self.USER_LC_DAILY_INFO_TABLE + " where date_time = '%s'" % date
        try:
            self.cur.execute(sql)
            res = {}
            for data in self.cur.fetchall():
                res[data[0]] = data
            self.cur.close()
            self.conn.close()
            return res
        except Exception as e:
            logger.error(e)
            self.cur.close()
            self.conn.close()
            return None

    def update_user_medal(self, user, medal):
        if not self._connect_mysql():
            return False
        sql = "update " + self.ACCOUNT_INFO_TABLE + " set medal = %s \
            where user = '%s'" % (medal, user)
        try:
            self.cur.execute(sql)
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            self.cur.close()
            self.conn.close()
            return False

    def update_user_email(self, user, email):
        if not self._connect_mysql():
            return False
        sql = "update " + self.ACCOUNT_INFO_TABLE + " set email = '%s' \
            where user = '%s'" % (email, user)
        try:
            self.cur.execute(sql)
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            self.cur.close()
            self.conn.close()
            return False

    def update_user_git_account(self, user, git_account):
        if not self._connect_mysql():
            return False
        sql = "update " + self.ACCOUNT_INFO_TABLE + " set git_account = '%s' \
            where user = '%s'" % (git_account, user)
        try:
            self.cur.execute(sql)
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            self.cur.close()
            self.conn.close()
            return False

    def update_user_award(self, user, val):
        if not self._connect_mysql():
            return False
        sql = "update " + self.ACCOUNT_INFO_TABLE + " set award = %s \
            where user = '%s'" % (val, user)
        try:
            self.cur.execute(sql)
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            self.cur.close()
            self.conn.close()
            return False

    def add_account_info(self, user, git_user='', email='', award=0, medal=0):
        if not self._connect_mysql():
            return False
        sql = "insert into " + self.ACCOUNT_INFO_TABLE + " (" + \
            ",".join(self.ACCOUNT_INFO_FIELDS) + ") values('%s', '%s', %s, %s, '%s')" \
                % (user, git_user, award, medal, email)
        try:
            self.cur.execute(sql)
            self.conn.commit()
            self.cur.close()
            self.conn.close()
        except Exception as e:
            logger.error(e)
            self.conn.rollback()
            self.cur.close()
            self.conn.close()
            return False

    def search_account(self, user):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.ACCOUNT_INFO_FIELDS)  + " from "+ \
            self.ACCOUNT_INFO_TABLE + " where user = '%s'" % user
        try:
            self.cur.execute(sql)
            data = self.cur.fetchall()
            self.cur.close()
            self.conn.close()
            if len(data) > 0:
                return data[0]
            return None
        except Exception as e:
            logger.error(e)
            self.cur.close()
            self.conn.close()
            return None

    def load_account_info(self):
        if not self._connect_mysql():
            return False
        sql = "select " + ",".join(self.ACCOUNT_INFO_FIELDS) + \
            " from " + self.ACCOUNT_INFO_TABLE
        try:
            self.cur.execute(sql)
            user_to_git = {}
            user_medal = {}
            user_award = {}
            user_email = {}
            for data in self.cur.fetchall():
                if data[1] != '':
                    user_to_git[data[0]] = data[1]
                user_medal[data[0]] = data[2]
                user_award[data[0]] = data[3]
                if data[4] != '':
                    user_email[data[0]] = data[4]
            self.cur.close()
            self.conn.close()
            return user_to_git, user_medal, user_award, user_email
        except Exception as e:
            logger.error(e)
            self.cur.close()
            self.conn.close()
            return None, None, None, None

if __name__ == '__main__':
    obj = MysqlService()
    date = '2022-09-17'
    # obj.update_user_award('smilecode-2', 1)
    # res = obj.load_account_info()
    # print(res)
    # print(obj.search_account('smilecode-2'))
    # obj.add_account_info('smilecode-22', 'xx', 'xx')
    # res = obj.serach_single_user_daily_info('smilecode-2', date)
    # print(res)
    # data = ['smilecode-2', 687, 1491, 12, 1731, 0, 0]
    # obj.add_single_user_daily_info(date, data)
    # res = obj.serach_single_user_daily_info('smilecode-2', date)
    # print(res)