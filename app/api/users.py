import datetime
import random
import time
import uuid

from flask import Blueprint
from flask import request
from sqlalchemy import func, extract
from sqlalchemy.sql import and_, or_

from app import db
from app.models.Orders import Orders
from app.models.Users import Users
from app.utils.code_dict import *
from app.utils.common import create_token, login_required
from models.Login_info import Login_info
from settings import METHODS, INPUT_STAFF, POWER_INTRODUCTION, POWER_ROLES, POWER_ROLES_DICT, TIME_STR, INSIDE, IFCZT, \
    PUBLICIST, ADMIN, INSIDE_ADMIN
from utils.common import verify_param

user = Blueprint("user", __name__)


# region 退出登录 没啥用的接口
@user.route('/user/logout', methods=METHODS)
def logout():
    return Succ200.to_dict()


# endregion
# region 用户登录
@user.route('/user/login', methods=METHODS)
def login():
    res_dir = request.get_json()
    if res_dir is None:
        return Error404

    # 获取前端传过来的参数
    username = res_dir.get("username")
    password = res_dir.get("password")
    # 校验参数
    if not all([username, password]):
        return Error404
    user_info = Users.query.filter_by(username=username).first()
    # noinspection PyBroadException
    try:
        user_info = Users.query.filter_by(username=username).first()
    except Exception:
        return Error4044.to_dict()
    if user_info is None or not user_info.check_password(password):
        return Error402.to_dict()
    if not user_info.active:  # 账号是否禁用
        return Error4011.to_dict()
    # 获取用户id，传入生成token的方法，并接收返回的token
    # noinspection PyBroadException
    try:
        u = {'u_id': user_info.u_id, 'power': user_info.power, 'name': user_info.username}
    except Exception:
        return Error409.to_dict()
    _login_info = Login_info(u_id=user_info.u_id, login_time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    db.session.add(_login_info)
    db.session.flush()
    db.session.commit()
    token = create_token(u)
    Succ200.data = {'token': token}
    # 把token返回给前端
    return Succ200.to_dict()


# endregion
# region 获取用户信息{roles:[],introduction:权限介绍 没啥用,name:名字,avatar:头像}
@user.route('/user/info', methods=METHODS)
@login_required()
def info(token):
    power = token['power']
    name = token['name']
    # noinspection PyBroadException
    try:
        introduction = POWER_INTRODUCTION[power]
    except Exception:
        return Error409.to_dict()
    avatar = 'http://zn.net/img/avatar/{}.gif'.format(random.randint(1, 8))
    data = {'roles': [power], 'introduction': introduction, 'name': name, 'avatar': avatar}
    Succ200.data = data
    return Succ200.to_dict()


# endregion
# region 修改密码
@user.route('/user/edit_password', methods=METHODS)
@login_required()
@verify_param(['password_old', 'password_new'])
def edit_password(token):
    u_id = token['u_id']
    res_dir = request.get_json()
    password_old = res_dir['password_old']
    password_new = res_dir['password_new']
    if len(password_new) < 6:
        return Error4010.to_dict()
    # noinspection PyBroadException
    try:
        _user = Users.query.filter_by(u_id=u_id).first()
    except Exception:
        return Error4044.to_dict()
    if not _user:
        return Error403.to_dict()
    if not _user.check_password(password_old):
        return Error402.to_dict()
    _user.password = password_new
    db.session.commit()
    return Succ200.to_dict()


# endregion
# region 获取用户可创建群组
@user.route('/user/get_power_group', methods=METHODS)
@login_required()
def get_power_group(token):
    power = token['power']
    data = []
    if power in POWER_ROLES and power != POWER_ROLES[3]:
        index = POWER_ROLES.index(power) + (1 if power in INSIDE_ADMIN else 2)
        if power == POWER_ROLES[POWER_ROLES.__len__() - 1] or power == POWER_ROLES[POWER_ROLES.__len__() - 2]:
            index = POWER_ROLES.__len__() - 1
        for i in range(index, POWER_ROLES_DICT.__len__()):
            data.append({'name': POWER_ROLES_DICT[i]['name'], 'id': POWER_ROLES_DICT[i]['id']})
    Succ200.data = data
    return Succ200.to_dict()


# endregion
# region 获取用户列表 加盟商及电销只能看到自己创建的账号
@user.route('/user/get_list', methods=METHODS)
@login_required()
@verify_param(['page', 'limit'])
def get_list(token):
    power = token['power']
    u_id = token['u_id']
    res_dir = request.get_json()
    page_index = res_dir.get('page')  # 页数
    limit = res_dir.get('limit')  # 一页多少条
    if power not in INSIDE:
        sql = Users.query.filter(or_(Users.superior == u_id, Users.u_id == u_id))
    else:
        if power not in IFCZT:
            roles = POWER_ROLES[POWER_ROLES.index(power)+1:]
            sql = Users.query.filter(Users.power.in_(roles))
        else:
            sql = Users.query
    if 'search_str' in res_dir:
        sql = sql.filter(Users.username.ilike('%' + res_dir['search_str'] + '%'))
    user_list = sql.limit(limit).offset((page_index - 1) * limit)
    data = {'total': sql.count(), 'items': []}
    year = str(datetime.datetime.now().year)
    for item in user_list:
        sales_volume = db.session.query(func.sum(Orders.price)).filter(
            and_(Orders.input_staff == item.u_id, Orders.delivery_state == 1)).scalar() or 0
        yeah_sales_volume = db.session.query(func.sum(Orders.price)).filter(
            and_(Orders.input_staff == item.u_id, Orders.delivery_state == 1,
                 extract('year', Orders.input_time) == year)).scalar() or 0
        signing = item.orders.filter_by(delivery_state=1).count()
        all_orders = item.orders.count()
        if all_orders is not 0:
            signing_rate = '%.f%%' % (signing / all_orders * 100)
        else:
            signing_rate = '暂未出单'
        login_time = item.login.order_by(Login_info.login_time.desc()).first()  # 取出最新的一条登录记录
        login_time = login_time.login_time.strftime(TIME_STR) if login_time else '暂未使用'
        # noinspection PyBroadException
        try:
            data['items'].append(
                {'id': item.id, 'username': item.username, 'active': item.active,
                 'power': POWER_INTRODUCTION[item.power],
                 'sales_volume': sales_volume, 'yeah_sales_volume': yeah_sales_volume, 'signing_rate': signing_rate,
                 'login_time': login_time, 'u_id': item.u_id})
        except Exception:
            return Error4012.to_dict()
    Succ200.data = data
    return Succ200.to_dict()


# endregion
# region 是否激活用户
@user.route('/user/active', methods=METHODS)
@login_required(INSIDE)
@verify_param(['id', 'bool'])
def active(token):
    res_dir = request.get_json()
    u_id = res_dir['id']  # 这里不是U_ID 是一个简单的编号
    e_bool = res_dir['bool']
    # noinspection PyBroadException
    try:
        _user = Users.query.filter_by(id=u_id).first()
        _user.active = e_bool
        db.session.flush()
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = None
    return Succ200.to_dict()


# endregion
# region 删除用户
@user.route('/user/del', methods=METHODS)
@login_required(IFCZT)
@verify_param(['id'])
def del_user(token):
    res_dir = request.get_json()
    u_id = res_dir['id']  # 这里不是U_ID 是一个简单的编号
    # noinspection PyBroadException
    try:
        _user = Users.query.filter_by(id=u_id).first()
        if _user.u_id == token['u_id']:
            return Error4013.to_dict()
        db.session.delete(_user)
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = None
    return Succ200.to_dict()


# endregion
# region 添加用户
@user.route('/user/add', methods=METHODS)
@login_required()
@verify_param(['username', 'password', 'power'])
def creat(token):
    res_dir = request.get_json()
    res_dir['superior'] = token['u_id']
    res_dir['u_id'] = str(uuid.uuid1())
    # noinspection PyBroadException
    try:
        _user = Users(**res_dir)
        db.session.add(_user)
        db.session.flush()
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    if res_dir['power'] not in POWER_INTRODUCTION:  # 判断是否存在该权限
        return Error4014.to_dict()
    res_dir.update(
        {'id': _user.id, 'yeah_sales_volume': 0, 'signing_rate': '暂未出单', 'sales_volume': 0, 'login_time': '暂未使用',
         'active': 1, 'power': POWER_INTRODUCTION[res_dir['power']], 'u_id': _user.u_id})
    Succ200.data = res_dir
    return Succ200.to_dict()


# endregion
# region 编辑用户
@user.route('/user/edit', methods=METHODS)
@login_required()
@verify_param(['u_id', 'password', 'power'])
def edit(token):
    res_dir = request.get_json()
    u_id = res_dir['u_id']  # 这里不是U_ID 是一个简单的编号
    password = res_dir['password']
    power = res_dir['power']
    # noinspection PyBroadException
    try:
        _user = Users.query.filter_by(u_id=u_id).first()
        _user.password = password
        _user.power = power
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = POWER_INTRODUCTION[power]
    return Succ200.to_dict()


# endregion
# region 获取加盟商用户列表
@user.route('/user/get_publicist_list', methods=METHODS)
@login_required(ADMIN)
def get_publicist_list(token):
    items = Users.query.filter_by(power=PUBLICIST).all()
    data = []
    for item in items:
        data.append({'u_id': item.u_id, 'username': item.username})
    Succ200.data = data
    return Succ200.to_dict()


# endregion
# region 获取用户名 （非路由函数）
def get_user_name(u_id):
    if u_id not in INPUT_STAFF:
        user_info = Users.query.filter_by(u_id=u_id).first()
        if user_info:
            INPUT_STAFF[u_id] = user_info.username
        else:
            return Error409.msg
    return INPUT_STAFF[u_id]


# endregion
# region 联想搜索用户名
@user.route('/user/query_name', methods=METHODS)
@login_required()
@verify_param(['value'])
def query_name(token):
    res_dir = request.get_json()
    lists = Users.query.filter(Users.username.ilike('%' + res_dir['value'] + '%')).limit(20).all()
    data = []
    for item in lists:
        data.append({'value': item.username, 'id': item.u_id})
    Succ200.data = data
    return Succ200.to_dict()
# endregion
