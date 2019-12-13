# -*- coding: UTF-8 -*-
import time

from flask import Blueprint, request

from api.school import get_school_name
from app import db
from app.utils.code_dict import *
from app.utils.common import login_required
from models.Promotion import Promotion
from settings import METHODS, PUBLICIST
from utils.common import verify_param

promotion = Blueprint("promotion", __name__)


@promotion.route('/school_ext/get_ppg_id', methods=METHODS)
@login_required(PUBLICIST)
@verify_param(['page', 'limit'])
def get_ppg_id(token):
    """
    获取宣传ID
    :param token:
    :return:
    """
    u_id = token['u_id']
    power = token['power']
    res_dir = request.get_json()
    page_index = res_dir.get('page')  # 页数
    limit = res_dir.get('limit')  # 一页多少条
    if 'province' in res_dir:
        sql = Promotion.query.filter_by(publicist_id=u_id, province=res_dir['province'])
    else:
        sql = Promotion.query.filter_by(publicist_id=u_id)
    # noinspection PyBroadException
    try:
        items = sql.limit(limit).offset((page_index - 1) * limit)
        total = sql.count()
    except Exception:
        return Error409.to_dict()
    data = {'items': [], 'total': total}
    for item in items:
        item = item.to_dict()
        item['id'] = str(item['id']).zfill(6)
        item['school_code'] = get_school_name(item['school_code'])
        data['items'].append(item)
    Succ200.data = data
    return Succ200.to_dict()


@promotion.route('/school_ext/input_ext', methods=METHODS)
@login_required(PUBLICIST)
@verify_param(['school_code'])
def input_ext(token):
    """
    新增学校宣传
    :param token:
    :return:
    """
    u_id = token['u_id']
    res_dir = request.get_json()
    res_dir['publicist_id'] = u_id
    res_dir['promotion_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # noinspection PyBroadException
    try:
        _terr = Promotion(**res_dir)
        db.session.add(_terr)
        db.session.flush()
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    return Succ200.to_dict()
