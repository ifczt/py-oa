from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from settings import SQLALCHEMY_DATABASE_URI
db = SQLAlchemy()
if db:
    from .api.users import user
    from .api.orders import order


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    # SQLALCHEMY_POOL_SIZE 配置 SQLAlchemy 的连接池大小
    app.config["SQLALCHEMY_POOL_SIZE"] = 5
    # SQLALCHEMY_POOL_TIMEOUT 配置 SQLAlchemy 的连接超时时间
    app.config["SQLALCHEMY_POOL_TIMEOUT"] = 15
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # 初始化SQLAlchemy , 本质就是将以上的配置读取出来
    db.init_app(app)
    app.register_blueprint(user)
    app.register_blueprint(order)
    return app
