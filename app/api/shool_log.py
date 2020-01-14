"""
    Created by IFCZT on  2020/1/14 10:52
"""
from app.models.School_log import School_log

__author__ = 'IFCZT'

from flask import Blueprint, request

from app import db
from settings import METHODS, PRODUCT_LIST, INSIDE
from app.utils.code_dict import Succ200, Error409
from app.utils.common import login_required, verify_param

school_log = Blueprint("school_log", __name__)

@school_log.route('/get_school_log',methods=METHODS)
@login_required()
@verify_param(['school_code'])
def get_school_log(token):
    u_id = token['u_id']
    res_dir = request.get_json()
    school_code = res_dir['school_code']
    data = []
    if 'id' in res_dir:
        o_id = res_dir['id']
        log = School_log.query.filter_by(school_code=school_code,u_id=u_id,status=1,id=o_id).first()
        data = log.to_dict()
    else:
        log = School_log.query.filter_by(school_code=school_code,u_id=u_id,status=1).all()
        for item in log:
            data.append(item.to_dict())

    Succ200.data = data
    return Succ200.to_dict()

@school_log.route('/add_school_log',methods=METHODS)
@login_required()
@verify_param(['title','content','school_code'])
def add_school_log(token):
    res_dir = request.get_json()
    title = res_dir['title']
    content = res_dir['content']
    school_code = res_dir['school_code']
    u_id = token['u_id']
    # noinspection PyBroadException
    try:
        Log = School_log()
        Log.school_code = school_code
        Log.u_id = u_id
        Log.title = title
        Log.content = content
        db.session.add(Log)
        db.session.flush()
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    data = {'input_time':Log.input_time,'id':Log.id}
    Succ200.data = data
    return Succ200.to_dict()

@school_log.route('/del_school_log',methods=METHODS)
@login_required()
@verify_param(['id'])
def del_school_log(token):
    u_id = token['u_id']
    res_dir = request.get_json()
    o_id = res_dir.get('id')
    _log = School_log.query.filter_by(id=o_id, u_id=u_id).first()
    # noinspection PyBroadException
    try:
        _log.status = 0
        db.session.flush()
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = None
    return Succ200.to_dict()


@school_log.route('/update_school_log',methods=METHODS)
@login_required()
@verify_param(['id','school_code'])
def update_school_log(token):
    res_dir = request.get_json()
    o_id = res_dir.get('id')
    u_id = token['u_id']
    if 'school_code' in res_dir:
        del res_dir['school_code']
    if 'id' in res_dir:
        del res_dir['id']
    # noinspection PyBroadException
    try:
        _log = School_log.query.filter_by(id=o_id, u_id=u_id,status=1).update(res_dir)
        db.session.flush()
        db.session.commit()
        _log = School_log.query.filter_by(id=o_id, u_id=u_id, status=1).first()
    except Exception:
        return Error409.to_dict()
    Succ200.data = _log.to_dict()
    return Succ200.to_dict()