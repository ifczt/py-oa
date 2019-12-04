# -*- coding: UTF-8 -*-
import time

from flask import Blueprint, request
from sqlalchemy.sql import and_
from api.users import get_user_name
from app import db
from app.models.Orders import Orders
from app.utils.code_dict import Succ200, Error405, Error406
from app.utils.common import login_required
from models.Users import Users
from settings import METHODS, CAN_SEE_ALL_ORDERS, POWER_ROLES
from utils.code_dict import Error409

order = Blueprint("order", __name__)


@order.route('/order/list', methods=METHODS)
@login_required
def order_list(token):
    """
    获取订单列表
    :param token:
    :return: items
    """
    u_id = token['u_id']
    res_dir = request.get_json()
    page_index = res_dir.get('page')  # 页数
    limit = res_dir.get('limit')  # 一页多少条

    if 'manage' in res_dir and res_dir.get('manage'):  # 管理页面请求拦截
        search_var(res_dir)
        sql = Orders.query.filter(get_safety_list(**res_dir, token=token))
    else:
        sql = Orders.query.filter_by(input_staff=u_id)
    items = sql.limit(limit).offset((page_index - 1) * limit)
    total = sql.count()
    data = {'items': [], 'total': total}
    for item in items:
        item = item.to_dict()
        item['input_staff'] = get_user_name(item['input_staff'] or u_id)
        item['id'] = str(item['id']).zfill(6)
        data['items'].append(item)
    Succ200.data = data
    return Succ200.to_dict()


# 列表数据插入前处理
def list_data_handle(data, u_id, is_input=True):
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
        data['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data['update_staff'] = u_id
    if 'id' in data and is_input:
        del data['id']
    return data


@order.route('/order/input', methods=METHODS)
@login_required
def order_input(token):
    """
    订单录入
    :return: {code}
    """
    u_id = token['u_id']
    res_dir = list_data_handle(request.get_json(), u_id)
    _order = Orders(**res_dir)
    db.session.add(_order)
    db.session.flush()
    Succ200.data = {'id': _order.id, 'delivery_state': '未发货'}
    db.session.commit()
    return Succ200.to_dict()


@order.route('/order/update_list', methods=METHODS)
@login_required
def update_list(token):
    """
    更新订单
    :param token:
    :return: code_dict
    """
    u_id = token['u_id']
    power = token['power']
    res_dir = list_data_handle(request.get_json(), u_id, False)
    if power not in CAN_SEE_ALL_ORDERS:
        _order = Orders.query.filter_by(id=res_dir.get('id'), input_staff=u_id).update(res_dir)
    else:
        _order = Orders.query.filter_by(id=res_dir.get('id')).update(res_dir)
    db.session.flush()
    db.session.commit()
    Succ200.data = None
    return Succ200.to_dict()


@order.route('/order/del_list', methods=METHODS)
@login_required
def del_list(token):
    """
    删除订单
    :param token:
    :return: code_dict
    """
    res_dir = request.get_json()
    o_id = res_dir.get('id')
    power = token['power']
    u_id = token['u_id']
    if power not in CAN_SEE_ALL_ORDERS:  # 如果不在可以看到所有订单的群组里 就添加搜索条件
        _order = Orders.query.filter_by(id=o_id, input_staff=u_id).first()
    else:
        _order = Orders.query.filter_by(id=o_id).first()
    if not _order:
        return Error406.to_dict()
    db.session.delete(_order)
    db.session.commit()
    Succ200.data = None
    return Succ200.to_dict()


@order.route('/order/apply_discount_state_change', methods=METHODS)
@login_required
def apply_discount_state_change(token):
    power = token['power']
    res_dir = request.get_json()
    if power in CAN_SEE_ALL_ORDERS:
        _order = Orders.query.filter_by(id=res_dir.get('id')).update({
            'apply_discount_state': res_dir['apply_discount_state'],
            'price': res_dir['price']})
        db.session.flush()
        db.session.commit()
    else:
        return Error409.to_dict()
    Succ200.data = None
    return Succ200.to_dict()


@order.route('/order/ppg_id_info', methods=METHODS)
@login_required
def ppg_id_info(token):
    """
    宣传编号信息
    :param token:
    :return: {学校,宣传人}
    """
    a = {'123456': {'school': '好学校', 'publicist': '陈大海'}, '456321': {'school': '的东西学校', 'publicist': '陈大海'}}
    res_dir = request.get_json()
    ppg_id = res_dir.get('ppg_id')
    if ppg_id not in a:
        return Error405.to_dict()
    Succ200.data = a[ppg_id]
    return Succ200.to_dict()


# 搜索条件去空值
def search_var(data):
    del data['page']
    del data['limit']
    del data['manage']
    return data


def get_safety_list(courier_code, delivery_state, buy_product, input_staff,
                    area, time_slot_value, type_time_slot, delivery, phone, parent, token):
    u_id = token['u_id']
    power = token['power']
    condition = (Orders.id > 0)
    if power not in CAN_SEE_ALL_ORDERS:  # 如果不在可以看到所有订单的群组里 就添加搜索条件
        if power == POWER_ROLES[4]:  # 如果是加盟商的话就添加宣传编号ppg_id[...多个]搜索条件
            pass
        else:  # 否则就是电销员 添加input_staff的搜索条件
            condition = and_(condition, Orders.input_staff == u_id)
    if courier_code:  # 快递单号
        condition = and_(condition, Orders.courier_code.ilike(add_like(courier_code)))
        return condition
    if buy_product and type(buy_product) is list:  # 购买产品
        condition = and_(condition, Orders.buy_product.in_(buy_product))
    if delivery_state and type(delivery_state) is list:  # 物流状态
        condition = and_(condition, Orders.delivery_state.in_(delivery_state))
    if delivery and type(delivery) is list:  # 派送方式
        condition = and_(condition, Orders.delivery.in_(delivery))
    if area and type(area) is list:  # 省市区查询
        if area[0]:  # 省
            condition = and_(condition, Orders.province == area[0])
            if area[1]:  # 市
                condition = and_(condition, Orders.city == area[1])
                if area[2]:  # 区
                    condition = and_(condition, Orders.area == area[2])
    if phone:
        condition = and_(condition, Orders.phone == phone)
    if parent:
        condition = and_(condition, Orders.parent == parent)
    if input_staff:
        condition = and_(condition, Orders.input_staff == input_staff)
    if type_time_slot:
        if type_time_slot == '1':
            condition = and_(condition, Orders.delivery_time.between(time_slot_value[0], time_slot_value[1]))
        if type_time_slot == '4':
            condition = and_(condition, Orders.input_time.between(time_slot_value[0], time_slot_value[1]))
    return condition


def add_like(val):
    return '%' + val + '%'
