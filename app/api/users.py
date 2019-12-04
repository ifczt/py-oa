import random

from flask import Blueprint
from flask import request

from app.models.Users import Users
from app.utils.code_dict import *
from app.utils.common import create_token, login_required
from settings import METHODS, INPUT_STAFF, POWER_INTRODUCTION

user = Blueprint("user", __name__)


@user.route('/user/logout', methods=METHODS)
def logout():
    return Succ200.to_dict()


@user.route('/user/login', methods=METHODS)
def login():
    """
    用户登录
    :return: token
    """
    res_dir = request.get_json()
    if res_dir is None:
        return Error404

    # 获取前端传过来的参数
    username = res_dir.get("username")
    password = res_dir.get("password")

    # 校验参数
    if not all([username, password]):
        return Error404
    # noinspection PyBroadException
    try:
        user_info = Users.query.filter_by(username=username).first()
    except Exception:
        return Error4044.to_dict()
    if user_info is None or not user_info.check_password(password):
        return Error402.to_dict()

    # 获取用户id，传入生成token的方法，并接收返回的token
    u = {'u_id': user_info.u_id, 'power': user_info.power, 'name': user_info.username}
    token = create_token(u)
    Succ200.data = {'token': token}
    # 把token返回给前端
    return Succ200.to_dict()


@user.route('/user/info', methods=METHODS)
@login_required
def info(token):
    power = token['power']
    name = token['name']
    introduction = POWER_INTRODUCTION[power]
    avatar = 'http://zn.net/img/avatar/{}.gif'.format(random.randint(1, 8))
    data = {'roles': [power], 'introduction': introduction, 'name': name, 'avatar': avatar}
    Succ200.data = data
    return Succ200.to_dict()


# 获取用户名
def get_user_name(u_id):
    if u_id not in INPUT_STAFF:
        user_info = Users.query.filter_by(u_id=u_id).first()
        if user_info:
            INPUT_STAFF[u_id] = user_info.username
        else:
            return Error409.msg
    return INPUT_STAFF[u_id]
