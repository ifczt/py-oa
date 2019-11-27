# -*- coding: UTF-8 -*-

DIALECT = 'mysql'
DRIVER = 'pymysql'
# USERNAME = 'ifczt'
# PASSWORD = 'ifczt'
# HOST = '112.74.59.83'
# PORT = '3333'
USERNAME = 'root'
PASSWORD = '123123'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'oa'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
)
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

METHODS = ['POST', 'GET']

SECRET_KEY = 'IFCZT900308'

DELIVERY_STATE = ['未发货', '已签收', '换货', '退货', '在投', '再投', '问题件', '取消']

INPUT_STAFF = {}

EXPRESS_NAME = {}

PRODUCT_LIST = {}

