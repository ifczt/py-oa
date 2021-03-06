# -*- coding: UTF-8 -*-

DIALECT = 'mysql'
DRIVER = 'mysqlconnector'
# USERNAME = 'ifczt'
# PASSWORD = 'ifczt'
# HOST = '112.74.59.83'
# PORT = '3333'
USERNAME = 'root'
PASSWORD = '123123'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'oa'
SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8&auth_plugin=mysql_native_password'.format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
)
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

METHODS = ['POST', 'GET']

SECRET_KEY = 'IFCZT900308'

DELIVERY_STATE = ['未发货', '已签收', '换货', '退货', '在投', '再投', '问题件', '取消']

SCHOOL = {}

INPUT_STAFF = {}

EXPRESS_NAME = {}

PRODUCT_LIST = {}
#                     上帝        超级管理员      管理员      财务          加盟商            电销
POWER_ROLES = ['IFCZT', 'SUPER_ADMIN', 'ADMIN', 'FINANCE', 'PUBLICIST', 'INPUT_STAFF']
POWER_ROLES_DICT = [{'name': '上帝', 'id': 'IFCZT'}, {'name': '超级管理员', 'id': 'SUPER_ADMIN'},
                    {'name': '管理员', 'id': 'ADMIN'}, {'name': '财务', 'id': 'FINANCE'},
                    {'name': '加盟商', 'id': 'PUBLICIST'}, {'name': '电销', 'id': 'INPUT_STAFF'}]
POWER_INTRODUCTION = {
    'IFCZT': '上帝', 'SUPER_ADMIN': '超级管理员', 'ADMIN': '客服',
    'FINANCE': '财务', 'PUBLICIST': '加盟商', 'INPUT_STAFF': '电销'
}
IFCZT = POWER_ROLES[0]
PUBLICIST = POWER_ROLES[4]  # 加盟商
INSIDE = POWER_ROLES[0:4]  # 公司内部群组
INSIDE_ADMIN = POWER_ROLES[0:2]  # 公司内部管理群组
ADMIN = POWER_ROLES[0:5]  # 除了电销以为 都是管理者
FINANCE = POWER_ROLES[1:4:2]  # 财务组

LEGEND = []
TIME_STR = '%Y-%m-%d %H:%M:%S'
