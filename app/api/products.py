# -*- coding: UTF-8 -*-
from flask import Blueprint
from models.Products import Products
from settings import METHODS, PRODUCT_LIST
from utils.code_dict import Succ200

product = Blueprint("products", __name__)


@product.route('/product_list', methods=METHODS)
def product_list():
    """
    获取产品列表
    :return: data=[{id,name,price}...]
    """
    items = Products.query.all()
    data = []
    for item in items:
        data.append(item.to_dict())
        PRODUCT_LIST[item.id] = item.name
    Succ200.data = data
    return Succ200.to_dict()


def get_product_name(id):
    if id not in PRODUCT_LIST:
        product_info = Products.query.filter_by(id=id).first()
        PRODUCT_LIST[id] = product_info.name
    return PRODUCT_LIST[id]
