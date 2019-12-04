# -*- coding: UTF-8 -*-
from flask import Blueprint
from app.models.Territory import Territory
from app.utils.code_dict import *
from app.utils.common import login_required
from settings import METHODS, PUBLICIST_PROVINCE, PUBLICIST_CITY, PUBLICIST_AREA
from sqlalchemy.sql import and_

territory = Blueprint("territory", __name__)


@territory.route('/territory/region', methods=METHODS)
@login_required
def get_region(token):
    u_id = token['u_id']
    province = Territory.query.filter_by(publicist_id=u_id).all()
    data = []
    for _p in province:
        if _p.province not in PUBLICIST_PROVINCE:
            PUBLICIST_PROVINCE.append(_p.province)
            if _p.city:
                PUBLICIST_CITY[_p.province] = _p.city
            if _p.area:
                PUBLICIST_AREA[_p.city] = _p.area
        data.append({'label': _p.province, 'key': _p.province})
    Succ200.data = data
    return Succ200.to_dict()
