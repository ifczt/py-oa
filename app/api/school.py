# -*- coding: UTF-8 -*-
import time
import uuid

from flask import Blueprint
from flask import request
from sqlalchemy.sql import and_, or_

from app import db
from app.api.orders import add_like
from app.api.territory import get_region_all
from app.models.School import School
from app.utils.code_dict import *
from app.utils.common import login_required
from app.utils.common import verify_param
from settings import METHODS, SCHOOL, PUBLICIST, INSIDE

school = Blueprint("school", __name__)


# region 添加学校
@school.route('/school/add', methods=METHODS)
@login_required()
@verify_param(['school_name', 'province', 'city', 'area', 'region'])
def add(token):
    u_id = token['u_id']
    res_dir = request.get_json()
    if 'school_code' in res_dir:
        return Error401.to_dict()
    res_dir['school_code'] = str(uuid.uuid1())
    res_dir['entry_clerk'] = u_id
    res_dir['input_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    res_dir['simple_name'] = res_dir['school_name']
    _school = School(**res_dir)
    db.session.add(_school)
    db.session.flush()
    db.session.commit()
    Succ200.data = None
    return Succ200.to_dict()


# endregion
# region 编辑学校
@school.route('/school/edit', methods=METHODS)
@login_required(INSIDE)
@verify_param(['school_code'])
def edit(token):
    u_id = token['u_id']
    res_dir = request.get_json()
    school_code = res_dir['school_code']
    del res_dir['school_code']
    res_dir['update_clerk'] = u_id
    res_dir['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for item in list(res_dir.keys()):  # 把传进来为空的 不修改 去掉 以免空值覆盖
        if not res_dir[item] and res_dir[item] is not 0:
            del res_dir[item]
    # noinspection PyBroadException
    try:
        School.query.filter_by(school_code=school_code).update(res_dir)
        db.session.flush()
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    return Succ200.to_dict()


# endregion
# region 联想搜索 只能搜索到其负责区域有效期内的学校
@school.route('/school/query_school', methods=METHODS)
@login_required(PUBLICIST)
@verify_param(['value'])
def query_school(token):
    res_dir = request.get_json()
    lists = School.query.filter(and_(
        School.school_name.ilike(add_like(res_dir['value'])),
        get_safety_list())).limit(20).all()
    data = []
    for item in lists:
        data.append({
            'value': item.simple_name, 'region': item.region, 'school_code': item.school_code, 'quality': item.quality,
            'province': item.province, 'city': item.city, 'area': item.area, 'school_address': item.school_address,
            'contact_info': item.contact_info})
    Succ200.data = data
    return Succ200.to_dict()


# endregion
# region 获取所负责区域的学校
@school.route('/school/get_region_school', methods=METHODS)
@login_required(PUBLICIST)
@verify_param(['page', 'limit'])
def get_region_school(token):
    res_dir = request.get_json()
    page_index = res_dir.get('page')  # 页数
    limit = res_dir.get('limit')  # 一页多少条
    province = res_dir.get('province')
    city = res_dir.get('city')
    quality = res_dir.get('quality')
    school_name = res_dir.get('school_name')
    condition = (School.id > 0)
    if city:
        condition = and_(condition, School.city == city)
    elif province:
        condition = and_(condition, School.province == province)
    if quality:
        condition = and_(condition, School.quality == quality)
    if school_name:
        condition = and_(condition, School.school_name.ilike(add_like(school_name)))
    sql = School.query.filter(get_safety_list()).filter(condition)
    items = sql.limit(limit).offset((page_index - 1) * limit)
    total = sql.count()
    data = {'items': [], 'total': total}
    for item in items:
        data['items'].append({'region': item.region, 'school_address': item.school_address,
                              'school_name': item.school_name, 'quality': item.quality,
                              'contact_info': item.contact_info, 'school_code': item.school_code})
    Succ200.data = data
    return Succ200.to_dict()


# endregion


# region 根据ID获取学校名字 （缓存函数）
def get_school_name(sid):
    if sid not in SCHOOL:
        item = School.query.filter_by(school_code=sid).first()
        if item:
            SCHOOL[sid] = item.school_name
        else:
            return Error409.msg
    return SCHOOL[sid]


# endregion
# region SQL语句处理
def get_safety_list():
    # condition = (School.province.in_(PUBLICIST_PROVINCE))
    data = get_region_all(request)  # 调用URL接口
    if data['code'] is not Succ200.code:
        return data
    data = data['data']
    province = data['province']
    city = data['city']
    good_c = None
    for _p in province:
        condition = (School.province == _p)
        if _p in city:
            condition = and_(condition, School.city.in_(city[_p]))
        good_c = or_(good_c, condition) if good_c is not None else condition
    return good_c
# endregion
