# -*- coding: UTF-8 -*-
import time

from flask import Blueprint, request
from sqlalchemy.sql import and_

from app import db
from app.models.Territory import Territory
from app.utils.code_dict import *
from app.utils.common import login_required
from settings import METHODS, PUBLICIST_PROVINCE, PUBLICIST_CITY, PUBLICIST, INSIDE_ADMIN
from utils.common import verify_param

territory = Blueprint("territory", __name__)


def remove_province(province, u_id):
    # noinspection PyBroadException
    try:
        terr = Territory.query.filter_by(publicist_id=u_id, province=province).first()
        db.session.delete(terr)
        db.session.commit()
    except Exception:
        print(Error409.msg)
    pass


@territory.route('/territory/remove_city', methods=METHODS)
@login_required(INSIDE_ADMIN)
@verify_param(['city', 'province', 'u_id'])
def remove_city(token):
    res_dir = request.get_json()
    u_id = res_dir['u_id']
    province = res_dir['province']
    city = res_dir['city']
    # noinspection PyBroadException
    try:
        terr = Territory.query.filter_by(publicist_id=u_id, province=province).first()
        city_list = terr.city.split(',')
        city_list.remove(city)
    except Exception:
        return Error409.to_dict()
    if city_list.__len__() == 0:
        remove_province(province, u_id)
    terr.city = ','.join(city_list)
    db.session.commit()
    Succ200.data = None
    return Succ200.to_dict()


@territory.route('/territory/get_list', methods=METHODS)
@login_required(INSIDE_ADMIN)
@verify_param(['u_id'])
def get_region(token):
    res_dir = request.get_json()
    u_id = res_dir['u_id']
    # noinspection PyBroadException
    try:
        sql = Territory.query.filter(and_(Territory.publicist_id == u_id, Territory.eff_time > time.localtime()))
        terr = sql.all()
    except Exception:
        return Error409.to_dict()
    data = {'item': [], 'total': sql.count()}
    for item in terr:
        data['item'].append({'province': item.province, 'city': item.city})
    Succ200.data = data
    return Succ200.to_dict()


@territory.route('/territory/province', methods=METHODS)
@login_required(PUBLICIST)
def get_province_region(token):
    """
    获取负责区域省份
    :param token:
    :return: [{label,key}....]
    """
    u_id = token['u_id']
    province = Territory.query.filter(and_(Territory.publicist_id == u_id, Territory.eff_time > time.localtime())).all()
    data = []
    for _p in province:
        if _p.province not in PUBLICIST_PROVINCE:
            PUBLICIST_PROVINCE.append(_p.province)
            if _p.city:
                if _p.province not in PUBLICIST_CITY:
                    PUBLICIST_CITY[_p.province] = []
                PUBLICIST_CITY[_p.province] = _p.city.split(',')
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
    Succ200.data = {'province': PUBLICIST_PROVINCE, 'city': PUBLICIST_CITY}
    return Succ200.to_dict()
