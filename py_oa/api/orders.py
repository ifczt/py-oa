import time

from flask import Blueprint, request

from py_oa.models.Express import Express
from py_oa.models.Products import Products
from py_oa.utils.code_dict import Succ200
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
    print(request.get_json())
    return {'code':999,'msg':'fuck'}


@order.route('/order/product_list', methods=METHODS)
def product_list():
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




