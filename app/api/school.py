# -*- coding: UTF-8 -*-
from flask import Blueprint
from flask import request
from sqlalchemy.sql import and_, or_

from api.orders import add_like
from app.models.School import School
from app.utils.code_dict import *
from app.utils.common import login_required
from settings import METHODS, SCHOOL, PUBLICIST_PROVINCE, PUBLICIST_AREA, PUBLICIST_CITY

school = Blueprint("school", __name__)


@school.route('/school/query_school', methods=METHODS)
@login_required
def query_school(token):
    u_id = token['u_id']
    res_dir = request.get_json()
    lists = School.query.filter(and_(
        School.school_name.ilike(add_like(res_dir['value'])),
        get_safety_list())).limit(20).all()
    print(School.query.filter(and_(
        School.school_name.ilike(add_like(res_dir['value'])),
        get_safety_list())))
    data = []
    for item in lists:
        data.append({
            'value': item.simple_name, 'region': item.region, 'school_code': item.school_code,
            'province': item.province, 'city': item.city, 'area': item.area})
    Succ200.data = data
    return Succ200.to_dict()


def get_school_name(sid):
    if sid not in SCHOOL:
        item = School.query.filter_by(school_code=sid).first()
        if item:
            SCHOOL[sid] = item.school_name
        else:
            return Error409.msg
    return SCHOOL[sid]


def get_safety_list():
    # condition = (School.province.in_(PUBLICIST_PROVINCE))
    condition = or_(
        and_(School.city.in_(PUBLICIST_CITY['340000']),
                    School.province.in_(PUBLICIST_PROVINCE[0])),
        (School.province.in_(PUBLICIST_PROVINCE[1]))
        )
    # for _p in PUBLICIST_PROVINCE:
    #     if _p in PUBLICIST_CITY:
    #         for _c in PUBLICIST_CITY:
    #             if _c in PUBLICIST_AREA:
    #                 condition_one = and_(School.area.in_(PUBLICIST_AREA[_c]))
    #             else:
    #                 condition_one = and_( School.city.in_(PUBLICIST_CITY[_p]))
    #     condition = or_(condition, condition_one)
    return condition
