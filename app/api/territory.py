# -*- coding: UTF-8 -*-
import time
from datetime import datetime

from flask import Blueprint, request
from sqlalchemy.sql import and_

from api.products import get_product_name
from app import db
from app.models.Territory import Territory
from app.utils.code_dict import *
from app.utils.common import login_required
from settings import METHODS, PUBLICIST, INSIDE_ADMIN, ADMIN
from utils.common import verify_param

territory = Blueprint("territory", __name__)


# region 删除省份 -- 删除一条合约
@territory.route('/territory/remove_province', methods=METHODS)
@login_required(INSIDE_ADMIN)
@verify_param(['province', 'u_id'])
def remove_province(token):
    res_dir = request.get_json()
    u_id = res_dir['u_id']
    province = res_dir['province']
    # noinspection PyBroadException
    try:
        terr = Territory.query.filter_by(publicist=u_id, province=province).first()
        db.session.delete(terr)
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    return Succ200.to_dict()


# endregion
# region 删除产品
@territory.route('/territory/remove_product', methods=METHODS)
@login_required(INSIDE_ADMIN)
@verify_param(['product', 'province', 'u_id'])
def remove_product(token):
    res_dir = request.get_json()
    u_id = res_dir['u_id']
    province = res_dir['province']
    product = res_dir['product']
    # noinspection PyBroadException
    try:
        terr = Territory.query.filter_by(publicist=u_id, province=province).first()
        product_list = terr.product.split(',')
        product_list.remove(product)
    except Exception:
        return Error409.to_dict()
    if product_list.__len__() == 0:
        code = remove_province(request)
        if code['code'] is not Succ200.code:  # 如果删除省份出错 抛出错误
            return Error409.to_dict()
    terr.product = ','.join(product_list)
    db.session.commit()
    Succ200.data = None
    return Succ200.to_dict()


# endregion
# region 删除城市
@territory.route('/territory/remove_city', methods=METHODS)
@login_required(INSIDE_ADMIN)
@verify_param(['province', 'u_id'])
def remove_city(token):
    res_dir = request.get_json()
    u_id = res_dir['u_id']
    province = res_dir['province']
    city = res_dir['city']
    city_list = []
    # noinspection PyBroadException
    try:
        terr = Territory.query.filter_by(publicist=u_id, province=province).first()
        if terr.city:
            city_list = terr.city.split(',')
            city_list.remove(city)
    except Exception:
        return Error409.to_dict()
    if city_list.__len__() == 0:
        code = remove_province(request)
        if code['code'] is not Succ200.code:  # 如果删除省份出错 抛出错误
            return Error409.to_dict()
    terr.city = ','.join(city_list)
    db.session.commit()
    Succ200.data = None
    return Succ200.to_dict()


# endregion
# region 获取负责区域信息列表
@territory.route('/territory/get_list', methods=METHODS)
@login_required(ADMIN)
@verify_param(['u_id'])
def get_region(token):
    res_dir = request.get_json()
    u_id = res_dir['u_id']
    return get_region_tender(u_id)


# endregion


@territory.route('/territory/province', methods=METHODS)
@login_required(PUBLICIST)
def get_province_region(token):
    """
    获取负责区域省份
    :param token:
    :return: [{label,key}....]
    """
    u_id = token['u_id']
    # noinspection PyBroadException
    try:
        province = Territory.query.filter(
            and_(Territory.publicist == u_id, Territory.eff_time > time.localtime())).all()
    except Exception:
        return Error409.to_dict()
    data = []
    for _p in province:
        data.append({'label': _p.province, 'key': _p.province})
    Succ200.data = data
    return Succ200.to_dict()


@territory.route('/territory/get_region_options', methods=METHODS)
@login_required()
def get_region_all(token):
    """
    获取负责的所有区域
    :param token:
    :return:
    """
    u_id = token['u_id']
    terr = Territory.query.filter(and_(Territory.publicist == u_id, Territory.eff_time > time.localtime())).all()
    province = []
    city = {}
    for item in terr:
        province.append(item.province)
        if item.city:
            city[item.province] = item.city.split(',')
    Succ200.data = {'province': province, 'city': city}
    return Succ200.to_dict()


@territory.route('/territory/input', methods=METHODS)
@login_required(INSIDE_ADMIN)
@verify_param(['product', 'province', 'eff_time', 'start_time', 'publicist'])
def input_terr(token):
    res_dir = request.get_json()
    _terr = Territory.query.filter_by(publicist=res_dir['publicist'], province=res_dir['province']).first()
    if _terr:
        return edit_terr(request)
    # noinspection PyBroadException
    try:
        _terr = Territory(**res_dir)
        db.session.add(_terr)
        db.session.flush()
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = None
    return Succ200.to_dict()


@territory.route('/territory/edit', methods=METHODS)
@login_required(INSIDE_ADMIN)
@verify_param(['product', 'province', 'eff_time', 'start_time', 'publicist'])
def edit_terr(token):
    res_dir = request.get_json()
    publicist = res_dir['publicist']
    province = res_dir['province']
    del res_dir['publicist']
    del res_dir['province']
    # noinspection PyBroadException
    try:
        _terr = Territory.query.filter_by(publicist=publicist, province=province).update(res_dir)
        db.session.flush()
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = None
    return Succ200.to_dict()


def get_region_tender(u_id, time_limit=True):
    # noinspection PyBroadException
    try:
        if time_limit:
            sql = Territory.query.filter(and_(Territory.publicist == u_id, Territory.eff_time > time.localtime(),
                                              Territory.start_time < time.localtime()))
        else:
            sql = Territory.query.filter(Territory.publicist == u_id)
        terr = sql.all()
    except Exception:
        return Error409.to_dict()
    data = {'item': [], 'total': sql.count()}
    for item in terr:
        product = []
        product_list = item.product.split(',')
        time_slot = datetime.strftime(item.start_time, '%Y-%m-%d') + '-' + datetime.strftime(item.eff_time, '%Y-%m-%d')
        for _p in product_list:
            product.append({'name': get_product_name(_p), 'id': _p})
        if time_limit:
            data['item'].append(
                {'province': item.province, 'city': item.city, 'product': product, 'time_slot': time_slot,
                 'product_list': product_list})
        else:
            data['item'].append(
                {'province': item.province, 'city': item.city, 'product': product, 'time_slot': time_slot,
                 'product_list': product_list,'start_time':item.start_time,'eff_time':item.eff_time})
    Succ200.data = data
    return Succ200.to_dict()
