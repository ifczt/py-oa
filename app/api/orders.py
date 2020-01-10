# -*- coding: UTF-8 -*-
import time
from datetime import datetime

from flask import Blueprint, request
from sqlalchemy import extract
from sqlalchemy.sql import and_,or_

from app.api.territory import  get_region_tender
from app.api.users import get_user_name
from app import db
from app.models.Orders import Orders
from app.models.Users import Users
from app.utils.code_dict import Succ200, Error405, Error406
from app.utils.common import login_required
from app.models.Products import Products
from app.models.Promotion import Promotion
from settings import METHODS, INSIDE, POWER_ROLES, TIME_STR, FINANCE, DELIVERY_STATE, PUBLICIST
from app.utils.code_dict import Error409
from app.utils.common import verify_param

order = Blueprint("order", __name__)


# region 下载财务数据表格
@order.route('/order/down_finance', methods=METHODS)
@login_required(FINANCE)
def down_finance(token):
    res_dir = request.get_json()
    # 产品ID 回款情况 回款日期 收费
    # 负责人 订单录入员 发单日期 物流状态
    # 省 市 产品 数量 收件人
    # 收件人号码 收件人地址 快递单号 退货单号
    # 换货单号
    sql = db.session.query(
        Orders.id, Orders.payment_state, Orders.refund_time, Orders.payment,
        Users.username, Orders.input_staff, Orders.delivery_time, Orders.delivery_state,
        Orders.province, Orders.city, Products.name, Orders.buy_num, Orders.consignee,
        Orders.phone, Orders.address, Orders.courier_code, Orders.courier_code_return,
        Orders.courier_code_relapse) \
        .join(Users, Users.u_id == Orders.publicist) \
        .join(Products) \
        .filter(get_safety_list(**res_dir, token=token))
    data = []
    items = sql.all()
    keys = ['id', 'payment_state', 'refund_time', 'payment',
            'username', 'input_staff', 'delivery_time', 'delivery_state',
            'province', 'city', 'name', 'buy_num', 'consignee',
            'phone', 'address', 'courier_code', 'courier_code_return',
            'courier_code_relapse']
    for item in items:
        obj = {}
        for index, key in enumerate(keys):
            if key.find('time') != -1:
                obj[key] = datetime.strftime(item[index], "%Y-%m-%d") if item[index] else '暂未回款'
            elif key == 'input_staff':
                obj[key] = get_user_name(item[index])
            elif key == 'payment_state':
                obj[key] = '已结算' if item[index] == 1 else '暂未回款'
            elif key == 'delivery_state':
                obj[key] = DELIVERY_STATE[item[index]]
            else:
                obj[key] = item[index]
        data.append(obj)
    Succ200.data = data
    return Succ200.to_dict()


# endregion
# region update_logistics 批量更新物流状态 （也可用于更新Orders其他数据） 参数格式[{id....},{},{},{}]
@order.route('/order/update_logistics', methods=METHODS)
@login_required(INSIDE)
@verify_param(['list'])
def update_logistics(token):
    res_dir = request.get_json()
    logistics_list = res_dir['list']
    db.session.bulk_update_mappings(Orders, logistics_list)
    # noinspection PyBroadException
    try:
        db.session.bulk_update_mappings(Orders, logistics_list)
        db.session.flush()
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    return Succ200.to_dict()


# endregion
# region list 获取订单列表 （新单导出）
@order.route('/order/list', methods=METHODS)
@login_required()
@verify_param(['page', 'limit'])
def order_list(token):
    u_id = token['u_id']
    res_dir = request.get_json()
    page_index = res_dir.get('page')  # 页数
    limit = res_dir.get('limit')  # 一页多少条
    power = token['power']
    day = str(datetime.now().day)
    if 'manage' in res_dir and res_dir.get('manage'):  # 管理页面请求拦截
        search_var(res_dir)
        if limit < 100:
            if power in PUBLICIST:
                # sql = Orders.query.filter(get_safety_list(**res_dir, token=token)).filter(publicist_safety(u_id))
                sql = Orders.query.filter(get_safety_list(**res_dir, token=token)).filter(Orders.publicist==u_id)
            else:
                sql = Orders.query.filter(get_safety_list(**res_dir, token=token))
        else:
            sql = Orders.query.with_entities(Orders.buy_product, Orders.parent, Orders.phone,
                                             Orders.address, Orders.price, Orders.buy_num, Orders.pay_method,
                                             Orders.remarks, Orders.id).filter(Orders.delivery_state==0,Orders.apply_discount_state!=1,extract('day', Orders.delivery_time) <= day)
    else:
        sql = Orders.query.filter(Orders.input_staff==u_id, Orders.delivery_state==0)
    # noinspection PyBroadException
    try:
        items = sql.limit(limit).offset((page_index - 1) * limit)
        total = sql.count()
    except Exception:
        return Error409.to_dict()
    data = {'items': [], 'total': total}
    if limit < 100:
        for item in items:
            dict_item = item.to_dict()
            dict_item['input_staff'] = get_user_name(dict_item['input_staff'] or u_id)
            dict_item['id'] = str(dict_item['id']).zfill(6)
            dict_item['ppg_id'] = str(dict_item['ppg_id']).zfill(6)
            dict_item['school'] = item.orders_school.school_name
            dict_item['publicist'] = get_user_name(dict_item['publicist'])
            data['items'].append(dict_item)
    else:
        for item in items:
            data['items'].append(
                {'buy_product': item[0], 'parent': item[1], 'phone': item[2], 'address': item[3], 'price': item[4],
                 'buy_num': item[5], 'pay_method': item[6], 'remarks': item[7], 'id': str(item[8]).zfill(6)})
    Succ200.data = data
    return Succ200.to_dict()


# endregion
# region 列表数据插入前处理
def list_data_handle(data, u_id, is_input=True):
    if 'input_staff' in data:
        if is_input:
            data['input_staff'] = u_id
        else:
            del data['input_staff']
    if is_input:
        # 物流状态 默认为0 未发货
        data['delivery_state'] = 0
        # 订单录入时间
        data['input_time'] = time.strftime(TIME_STR, time.localtime())
    else:
        if 'input_time' in data:
            del data['input_time']
        data['update_time'] = time.strftime(TIME_STR, time.localtime())
        data['update_staff'] = u_id
    if 'id' in data and is_input:
        del data['id']
    if 'school' in data:
        del data['school']
    return data


# endregion
# region input 订单录入
@order.route('/order/input', methods=METHODS)
@login_required()
def order_input(token):
    u_id = token['u_id']
    res_dir = list_data_handle(request.get_json(), u_id)
    # noinspection PyBroadException
    try:
        _order = Orders(**res_dir)
        db.session.add(_order)
        db.session.flush()
        db.session.commit()
    except Exception:
        print(Exception.__dict__)
        return Error409.to_dict()
    Succ200.data = {'id': str(_order.id).zfill(6), 'delivery_state': '未发货'}
    return Succ200.to_dict()


# endregion
# region update_list 更新订单 （单条数据更新）
@order.route('/order/update_list', methods=METHODS)
@login_required()
@verify_param(['id'])
def update_list(token):
    u_id = token['u_id']
    power = token['power']
    res_dir = list_data_handle(request.get_json(), u_id, False)
    # noinspection PyBroadException
    try:
        if power not in INSIDE:
            _order = Orders.query.filter_by(id=res_dir.get('id'), input_staff=u_id, delivery_state=0).update(res_dir)
        else:
            _order = Orders.query.filter(Orders.id == res_dir.get('id'), Orders.delivery_state != 3).update(res_dir)
        db.session.flush()
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = None
    return Succ200.to_dict()


# endregion
# region del_list 删除订单
@order.route('/order/del_list', methods=METHODS)
@login_required()
@verify_param(['id'])
def del_list(token):
    res_dir = request.get_json()
    o_id = res_dir.get('id')
    power = token['power']
    u_id = token['u_id']
    if power not in INSIDE:  # 如果不在可以看到所有订单的群组里 就添加搜索条件
        _order = Orders.query.filter_by(id=o_id, input_staff=u_id).first()
    else:
        _order = Orders.query.filter_by(id=o_id).first()
    if not _order:
        return Error406.to_dict()
    # noinspection PyBroadException
    try:
        db.session.delete(_order)
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = None
    return Succ200.to_dict()


# endregion
# region apply_discount_state_change 处理折扣申请
@order.route('/order/apply_discount_state_change', methods=METHODS)
@login_required(INSIDE)
@verify_param(['apply_discount_state', 'price'])
def apply_discount_state_change(token):
    power = token['power']
    res_dir = request.get_json()
    # noinspection PyBroadException
    try:
        _order = Orders.query.filter_by(id=res_dir.get('id')).update({
            'apply_discount_state': res_dir['apply_discount_state'],
            'price': res_dir['price']})
        db.session.flush()
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = None
    return Succ200.to_dict()


# endregion
# region ppg_id_info 根据宣传ID返回{school、publicist:[id,name],school_code}
@order.route('/order/ppg_id_info', methods=METHODS)
@login_required()
@verify_param(['ppg_id'])
def ppg_id_info(token):
    res_dir = request.get_json()
    ppg_id = res_dir.get('ppg_id')
    # noinspection PyBroadException
    try:
        _promotion = Promotion.query.filter_by(id=ppg_id).first()
    except Exception:
        return Error409.to_dict()
    if not _promotion:
        return Error405.to_dict()
    if not _promotion.promotion_user or not _promotion.promotion_school:
        return Error409.to_dict()
    Succ200.data = {'school': _promotion.promotion_school.school_name,
                    'publicist': [_promotion.publicist, _promotion.promotion_user.username],
                    'school_code': _promotion.promotion_school.school_code}
    return Succ200.to_dict()


# endregion
# region 删除掉数据库没有的键值 （页数、一页多少条等）
def search_var(data):
    del data['page']
    del data['limit']
    del data['manage']
    return data


# endregion
# region 搜索条件转SQL查询处理
def get_safety_list(courier_code, delivery_state, buy_product,
                    area, time_slot_value, type_time_slot, delivery, phone, parent,
                    token, payment_state, apply_discount_state,input_staff=None):
    u_id = token['u_id']
    power = token['power']
    condition = (Orders.id > 0)
    if power not in INSIDE:  # 如果不在可以看到所有订单的群组里 就添加搜索条件
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
        condition = and_(condition, Orders.parent.ilike(add_like(parent)))
    if input_staff:
        condition = and_(condition, Orders.input_staff == input_staff)
    if type_time_slot:
        time_slot_value[1] = datetime.strptime(time_slot_value[1] + ' 23:59:59', "%Y-%m-%d %H:%M:%S")
        if type_time_slot == '1':
            condition = and_(condition, Orders.delivery_time.between(time_slot_value[0], time_slot_value[1]))
        elif type_time_slot == '2':
            condition = and_(condition, Orders.refund_time.between(time_slot_value[0], time_slot_value[1]))
        elif type_time_slot == '4':
            condition = and_(condition, Orders.input_time.between(time_slot_value[0], time_slot_value[1]))
    if len(apply_discount_state) > 0:
        condition = and_(condition, Orders.apply_discount_state == apply_discount_state)
    if len(payment_state) > 0:
        condition = and_(condition, Orders.payment_state == payment_state)
    return condition


# endregion
# region 加盟商合约内订单搜索
def publicist_safety(u_id,time_limit=True):
    condition = (Orders.publicist == u_id)
    return condition
    # region 旧算法 按签约的区域时间来取 但是没什么用 因为订单里面有publicist 直接取即可
    # data = get_region_tender(u_id,time_limit)
    # if data['code'] == Succ200.code:
    #     data = data['data']['item']
    # or_condition = None
    # for item in data:
    #     condition = and_(Orders.province==item['province'])
    #     if len(item['city'])>1:
    #         condition = and_(condition,Orders.city.in_(item['city']))
    #     if not time_limit:
    #         condition = and_(condition, Orders.input_time.between(item['start_time'],item['eff_time']))
    #     condition = and_(condition,Orders.buy_product.in_(item['product_list']))
    #     or_condition = or_(or_condition,condition) if or_condition is not None else condition
    # return or_condition
    # endregion
# endregion


def add_like(val):
    return '%' + val + '%'
