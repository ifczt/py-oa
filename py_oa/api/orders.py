# -*- coding: UTF-8 -*-
from flask import Blueprint, request

from py_oa import db
from py_oa.models.Orders import Orders
from py_oa.models.Express import Express
from py_oa.models.Products import Products
from py_oa.utils.code_dict import Succ200, Error405
from py_oa.utils.common import login_required
from settings import METHODS

order = Blueprint("order", __name__)

@order.route('/order/list', methods=METHODS)
@login_required
def list(u_id):
    # print(request.get_json())
    return {
        'code': 200,
        'data': {
          'total': 0,
          'items': []
        }}

@order.route('/order/input', methods=METHODS)
@login_required
def input(u_id):
    """
    订单录入
    :return: {code}
    """
    res_dir = request.get_json()
    del res_dir['area']
    print(res_dir)
    _order = Orders(**res_dir)
    db.session.add(_order)
    db.session.commit()
    return Succ200.to_dict()


@order.route('/order/product_list', methods=METHODS)
def product_list():
    """
    获取产品列表
    :return: data=[{id,name,price}...]
    """
    items = Products.query.all()
    data = []
    for item in items:
        data.append(item.to_dict())
    Succ200.data = data
    return Succ200.to_dict()


@order.route('/order/express_list', methods=METHODS)
def express_list():
    """
    获取快递列表
    :return: data=[{id,name,price}...]
    """
    items = Express.query.all()
    data = []
    for item in items:
        data.append(item.to_dict())
    Succ200.data = data
    return Succ200.to_dict()


@order.route('/order/ppg_id_info', methods=METHODS)
@login_required
def ppg_id_info(u_id):
    a = {'123456':{'school':'abcdef'},'456321':{'school':'的东西学校'}}
    res_dir = request.get_json()
    ppg_id = res_dir.get('ppg_id')
    if ppg_id not in a:
        return Error405.to_dict()
    Succ200.data = a[ppg_id]
    return Succ200.to_dict()


