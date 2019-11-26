# -*- coding: UTF-8 -*-
import time
from flask import Blueprint, request
from api.express import get_express_name
from api.products import get_product_name
from api.users import get_user_name
from app import db
from app.models.Orders import Orders
from app.utils.code_dict import Succ200, Error405
from app.utils.common import login_required
from settings import METHODS, DELIVERY_STATE
from utils.code_dict import Error406

order = Blueprint("order", __name__)


@order.route('/order/list', methods=METHODS)
@login_required
def order_list(u_id):
    """
    获取订单列表
    :param u_id:
    :return: items
    """
    items = Orders.query.filter_by(input_staff=u_id).all()
    data = {'items': [], 'total': Orders.query.filter_by(input_staff=u_id).count()}
    for item in items:
        item = to_html_list_data_handle(item.to_dict(), u_id)
        data['items'].append(item)
    Succ200.data = data
    return Succ200.to_dict()


# 列表数据插入前处理
def list_data_handle(data, u_id, is_input=True):
    if 'area' in data and data['area']:
        data['province'] = data['area'][0]
        if len(data['area']) > 1:
            data['city'] = data['area'][1]
        if len(data['area']) > 2:
            data['area'] = data['area'][2]
    else:
        del data['area']
    # 录入员转换为u_id 传进来的是name
    if 'input_staff' in data:
        if is_input:
            data['input_staff'] = u_id
        else:
            del data['input_staff']
    if is_input:
        # 物流状态 默认为0 未发货
        data['delivery_state'] = 0
        # 订单录入时间
        data['input_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    else:
        if 'input_time' in data:
            del data['input_time']
        data['delivery_state'] = DELIVERY_STATE.index(data['delivery_state'])
        data['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data['update_staff'] = u_id
    if 'id' in data and is_input:
        del data['id']
    return data


# 列表数据返回前处理
def to_html_list_data_handle(data, u_id):
    if 'delivery_state' in data:
        data['delivery_state'] = DELIVERY_STATE[int(data['delivery_state'] if data['delivery_state'] else 0)]
    if 'input_staff' in data and data['input_staff']:
        data['input_staff'] = get_user_name(data['input_staff'])
    else:
        data['input_staff'] = get_user_name(u_id)
    if 'delivery' in data:
        data['delivery'] = get_express_name(data['delivery'])
    if 'buy_product' in data:
        data['buy_product'] = get_product_name(data['buy_product'])
    return data


@order.route('/order/input', methods=METHODS)
@login_required
def order_input(u_id):
    """
    订单录入
    :return: {code}
    """
    res_dir = list_data_handle(request.get_json(), u_id)
    _order = Orders(**res_dir)
    db.session.add(_order)
    db.session.flush()
    Succ200.data = {'id': _order.id, 'delivery_state': '未发货'}
    db.session.commit()
    return Succ200.to_dict()


@order.route('/order/update_list', methods=METHODS)
@login_required
def update_list(u_id):
    """
    更新订单
    :param u_id:
    :return: code_dict
    """
    res_dir = list_data_handle(request.get_json(), u_id, False)
    print(res_dir)
    _order = Orders.query.filter_by(id=res_dir.get('id'), input_staff=u_id).update(res_dir)
    db.session.flush()
    db.session.commit()
    Succ200.data = None
    return Succ200.to_dict()


@order.route('/order/del_list', methods=METHODS)
@login_required
def del_list(u_id):
    """
    删除订单
    :param u_id:
    :return: code_dict
    """
    res_dir = request.get_json()
    o_id = res_dir.get('id')
    _order = Orders.query.filter_by(id=o_id, input_staff=u_id).first()
    if not _order:
        return Error406.to_dict()
    db.session.delete(_order)
    db.session.commit()
    Succ200.data = None
    return Succ200.to_dict()


@order.route('/order/ppg_id_info', methods=METHODS)
@login_required
def ppg_id_info(u_id):
    """
    宣传编号信息
    :param u_id:
    :return: {学校,宣传人}
    """
    a = {'123456': {'school': '好学校', 'publicist': '陈大海'}, '456321': {'school': '的东西学校', 'publicist': '陈大海'}}
    res_dir = request.get_json()
    ppg_id = res_dir.get('ppg_id')
    if ppg_id not in a:
        return Error405.to_dict()
    Succ200.data = a[ppg_id]
    return Succ200.to_dict()
