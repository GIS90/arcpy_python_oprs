# -*- coding: utf-8 -*-

"""
------------------------------------------------
describe: 
------------------------------------------------
"""

__version__ = "v.10"
__author__ = "PyGo"
__time__ = "2016/12/2"


class DBType(object):
    MYSQL = 0
    SQL_SERVER = 1
    ORACLE = 2
    SQL_LITE = 3
    OTHER = 4


class DBHandler:
    def __init__(self, dbType, ip, port, user, passWord, default):
        self.mDbType = str(dbType).upper()
        self.mIP = ip
        self.mPort = int(port)
        self.mUser = user
        self.mPassword = passWord
        self.mDBDefault = default
        self.conn = None

    def open(self):
        try:
            return self.__open()
        except Exception as oe:
            raise Exception("DBHandler open got exception, error is " + str(oe))

            # 依据dbType的不同对数据库进行不同的connect
            # 连接成功返回connect对象，失败返回-1。，
            # def connect(self):

    def __open(self):
        if self.mDbType == 'MYSQL':
            import mysql.connector
            self.conn = mysql.connector.connect(host=self.mIP,
                                                port=self.mPort,
                                                user=self.mUser,
                                                passwd=self.mPassword,
                                                db=self.mDBDefault)
        elif self.mDbType == 'SQL_SERVER':
            import pyodbc
            Driver = '{SQL Server}'
            self.conn = pyodbc.connect(('DRIVER=%s;SERVER=%s;PORT=%s;DATABASE=%s;UID=%s;PWD=%s;TDS_Version=7.2'
                                        % (Driver, self.mIP, self.mPort, self.mDBDefault, self.mUser, self.mPassword)))

        elif self.mDbType == 'ORACLE':
            import cx_Oracle
            connParas = self.mUser + '/' + self.mPassword + '@' + self.mIP + '/' + 'orcl'
            self.conn = cx_Oracle.connect(connParas)

        elif self.mDbType == 'SQL_LITE':
            import sqlite3
            dbName = self.mDBDefault + '.db'
            self.conn = sqlite3.connect(dbName)

        else:
            raise Exception("unsupported DataBase")
        return self.conn

    def close(self):
        try:
            if self.conn is not None:
                self.conn.close()
        except Exception as ce:
            raise Exception("DBHandler close got exception, error is Close Failure , " + str(ce))

    def query(self, sql, retType, times=5):
        # returnType为1，返回值是1一个值，类型字符串
        # returnType为2，返回值列表
        assert isinstance(sql, basestring)
        assert isinstance(retType, int)
        assert retType in range(1, 3)
        if self.conn is None:
            for i in range(1, times, 1):
                if self.open():
                    break
                if i == times:
                    raise Exception('DBHandler query got exception, error is Open Failure')

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            retValues = cursor.fetchall()
            if not retValues:
                return "0" if 1 == retType else []
            if retType == 1:
                return str(retValues[0][0])
            elif retType == 2:
                return list(retValues)
        except Exception as qe:
            raise Exception('DBHandler query got exception, error is query Failure : ' + str(qe))
