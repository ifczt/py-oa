DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'ifczt'
PASSWORD = 'ifczt'
HOST = '112.74.59.83'
PORT = '3333'
DATABASE = 'oa'

SQLALCHEMY_DATABASE_URI = '{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(
    DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
)
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

METHODS = ['POST','GET']

SECRET_KEY = 'IFCZT900308'
