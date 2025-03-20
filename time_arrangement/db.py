
# coding=utf-8
import os
import pymysql

MYSQLDB = {
    'time_arrange': {
        'host': 'localhost',
        'user': 'root',
        'password': 'tingting517',
        'port': 3306,
        'charset': 'utf8',
    }
}


class BaseDB:
    """用于连接数据库，并实现退出自动close"""

    def __init__(self,machine,cursor="Cursor",charset="utf8",database=''):
        db = MYSQLDB.get(machine)
        self.host = db.get("host")
        self.user = db.get("user")
        self.pwd = db.get("password")
        
        if cursor == "DictCursor":
            try:
                self.conn = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.pwd,
                    charset=charset,
                    autocommit=True,
                    db=database,
                    cursorclass=pymysql.cursors.DictCursor,
                )
                self.cur = self.conn.cursor()
            except Exception:
                conn = 0
        else:
            try:
                self.conn = pymysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.pwd,
                    charset=charset,
                    autocommit=True,
                    db=database,
                    cursorclass=pymysql.cursors.Cursor,  # 不写也行，默认就是Cursor
                )
                # my_logg.debug("打印sql连接")
                # my_logg.debug(conn)
                self.cur = self.conn.cursor()
            except:
                conn = 0

    def __enter__(self,charset="utf8", cursor="Cursor"):
        """登录数据库"""
        return self


    def query_one_and_one_field(self,sql,params=(),keyparams={}):
        """获取one并且获取第一个字段，sql中需用format形式传参"""
        res = self.cur.execute(sql.format(*params,**keyparams))
        if res:
            res1 = self.cur.fetchone()
            return res1[0]
        
    def query_one(self,sql,params=(),keyparams={}):
        """获取one并且获取所有字段"""
        # sql中需用format形式传参
        res = self.cur.execute(sql.format(*params,**keyparams))
        if res :
            res1 = self.cur.fetchone()
            return res1
        
    def query_all(self,sql,params=(),keyparams={}):
        """获取all"""
        print(sql.format(*params, **keyparams))
        if self.cur.execute(sql.format(*params,**keyparams)):
            return self.cur.fetchall()
        else:
            return []
        
    # def query_one(self,sql,params=(),keyparams={}):
    #     """获取one并且获取所有字段"""
    #     # sql中需用format形式传参
    #     self.cur.execute(sql.format(*params,**keyparams))

    def update(self,sql,params=(),keyparams={}):
        """更新sql语句"""
        print(sql.format(*params, **keyparams))
        self.cur.execute(sql.format(*params, **keyparams))
        self.conn.commit()

    def update_result(self, sql, params=(), keyparams={}):
        """
        更新sql语句并返回更新结果
        Args:
            sql:
            params:
            keyparams:

        Returns:

        """
        return self.cur.execute(sql.format(*params, **keyparams))

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
