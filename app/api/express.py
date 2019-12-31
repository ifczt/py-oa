# -*- coding: UTF-8 -*-
from flask import Blueprint
from flask import request

from app import db
from app.models.Express import Express
from settings import METHODS, EXPRESS_NAME, INSIDE
from app.utils.code_dict import Succ200, Error409
from app.utils.common import login_required, verify_param

express = Blueprint("express", __name__)


# region 获取快递列表
@express.route('/express_list', methods=METHODS)
def express_list():
    items = Express.query.filter_by(active=1).all()
    data = []
    for item in items:
        data.append(item.to_dict())
    Succ200.data = data
    return Succ200.to_dict()
# endregion
# region 添加快递公司
@express.route('/express/creat', methods=METHODS)
@login_required()
@verify_param(['name'])
def creat(token):
    res_dir = request.get_json()
    # noinspection PyBroadException
    try:
        _express = Express(**res_dir)
        db.session.add(_express)
        db.session.flush()
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = {'id': _express.id, 'active': _express.active}
    return Succ200.to_dict()
# endregion
# region 是否激活快递公司
@express.route('/express/active', methods=METHODS)
@login_required(INSIDE)
@verify_param(['id', 'bool'])
def active(token):
    res_dir = request.get_json()
    e_id = res_dir['id']
    e_bool = res_dir['bool']
    # noinspection PyBroadException
    try:
        _express = Express.query.filter_by(id=e_id).first()
        _express.active = e_bool
        db.session.flush()
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = None
    return Succ200.to_dict()
# endregion
# region 删除快递公司
@express.route('/express/del', methods=METHODS)
@login_required(INSIDE)
@verify_param(['id'])
def del_express(token):
    res_dir = request.get_json()
    e_id = res_dir['id']
    # noinspection PyBroadException
    try:
        _express = Express.query.filter_by(id=e_id).first()
        db.session.delete(_express)
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = None
    return Succ200.to_dict()
# endregion
# region 更新
@express.route('/express/edit', methods=METHODS)
@login_required()
@verify_param(['id', 'name'])
def edit(token):
    res_dir = request.get_json()
    e_id = res_dir['id']
    e_name = res_dir['name']
    # noinspection PyBroadException
    try:
        _express = Express.query.filter_by(id=e_id).first()
        _express.name = e_name
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = None
    return Succ200.to_dict()
# endregion
# region 获取快递名字 （非路由函数）
def get_express_name(id):
    if id not in EXPRESS_NAME:
        express_info = Express.query.filter_by(id=id).first()
        if not express_info:
            return
        EXPRESS_NAME[id] = express_info.name
    return EXPRESS_NAME[id]
# endregion
