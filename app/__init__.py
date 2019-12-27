from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from settings import SQLALCHEMY_DATABASE_URI

# region 导入API
db = SQLAlchemy()
if db:
    from .api.users import user
    from .api.orders import order
    from .api.express import express
    from .api.products import product
    from .api.territory import territory
    from .api.promotion import promotion
    from .api.school import school
    from .api.data_show import data_show
    from models import Login_info
# endregion


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
    # region 注入蓝图
    app.register_blueprint(user)
    app.register_blueprint(order)
    app.register_blueprint(express)
    app.register_blueprint(product)
    app.register_blueprint(territory)
    app.register_blueprint(promotion)
    app.register_blueprint(school)
    app.register_blueprint(data_show)
    # endregion
    return app
