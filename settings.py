# -*- coding: UTF-8 -*-

DIALECT = 'mysql'
DRIVER = 'pymysql'
# USERNAME = 'ifczt'
# PASSWORD = 'ifczt'
# HOST = '112.74.59.83'
# PORT = '3333'
USERNAME = 'root'
PASSWORD = 'ifczt'
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

PUBLICIST_PROVINCE = []
PUBLICIST_CITY = {}


DELIVERY_STATE = ['未发货', '已签收', '换货', '退货', '在投', '再投', '问题件', '取消']

SCHOOL = {}

INPUT_STAFF = {}

EXPRESS_NAME = {}

PRODUCT_LIST = {}
#                          上帝        超级管理员      管理员      财务          加盟商            电销
POWER_ROLES = ['IFCZT', 'SUPER_ADMIN', 'ADMIN', 'FINANCE', 'PUBLICIST', 'INPUT_STAFF']
POWER_INTRODUCTION = {
    'IFCZT': '上帝', 'SUPER_ADMIN': '超级管理员', 'ADMIN': '客服',
    'FINANCE': '财务', 'PUBLICIST': '加盟商', 'INPUT_STAFF': '电销'
}

CAN_SEE_ALL_ORDERS = POWER_ROLES[0:4]
