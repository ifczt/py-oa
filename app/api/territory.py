# -*- coding: UTF-8 -*-
import time

from flask import Blueprint
from sqlalchemy.sql import and_

from app.models.Territory import Territory
from app.utils.code_dict import *
from app.utils.common import login_required
from settings import METHODS, PUBLICIST_PROVINCE, PUBLICIST_CITY

territory = Blueprint("territory", __name__)


@territory.route('/territory/region', methods=METHODS)
@login_required
def get_region(token):
    """
    获取负责区域
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
@login_required
def get_region_all(token):
    """
    获取负责的所有区域
    :param token:
    :return:
    """
    Succ200.data = {'province': PUBLICIST_PROVINCE, 'city': PUBLICIST_CITY}
    return Succ200.to_dict()
