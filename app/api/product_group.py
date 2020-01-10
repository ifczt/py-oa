"""
    Created by IFCZT on  2020/1/9 16:13
"""
__author__ = 'IFCZT'
from flask import Blueprint, request

from app import db
from app.models.Product_group import Product_group
from settings import METHODS, PRODUCT_LIST, INSIDE
from app.utils.code_dict import Succ200, Error409
from app.utils.common import login_required, verify_param

product_group = Blueprint("product_group", __name__)

@product_group.route('/product_group_list', methods=METHODS)
def product_group_list():
    """
    获取产品分类列表
    :return: data=[{id,name,price}...]
    """
    items = Product_group.query.all()
    data = []
    for item in items:
        data.append(item.to_dict())
    Succ200.data = data
    return Succ200.to_dict()