# -*- coding: UTF-8 -*-
from flask import Blueprint, request

from app import db
from app.models.Products import Products
from settings import METHODS, PRODUCT_LIST, INSIDE
from app.utils.code_dict import Succ200, Error409
from app.utils.common import login_required, verify_param

product = Blueprint("products", __name__)


@product.route('/product/creat', methods=METHODS)
@login_required()
@verify_param(['name'])
def creat(token):
    """
    添加产品
    :param token:
    :return:
    """
    res_dir = request.get_json()
    # noinspection PyBroadException
    try:
        _product = Products(**res_dir)
        db.session.add(_product)
        db.session.flush()
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = {'id': _product.id, 'active': _product.active}
    return Succ200.to_dict()


@product.route('/product_list', methods=METHODS)
def product_list():
    """
    获取产品列表
    :return: data=[{id,name,price}...]
    """
    res_dir = request.get_json()
    if res_dir and 'ids' in res_dir:
        ids = res_dir['ids'].split(',')
        sql =Products.query.filter(Products.id.in_(ids))
    else:
        sql = Products.query
    items = sql.all()
    data = []
    for item in items:
        data.append(item.to_dict())
        PRODUCT_LIST[item.id] = item.name
    Succ200.data = data
    return Succ200.to_dict()


@product.route('/product/del', methods=METHODS)
@login_required(INSIDE)
@verify_param(['id'])
def del_product(token):
    """
    删除产品
    :param token:
    :return:
    """
    res_dir = request.get_json()
    p_id = res_dir['id']
    # noinspection PyBroadException
    try:
        _product = Products.query.filter_by(id=p_id).first()
        db.session.delete(_product)
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = None
    return Succ200.to_dict()


@product.route('/product/active', methods=METHODS)
@login_required(INSIDE)
@verify_param(['id', 'bool'])
def active(token):
    """
    是否激活产品
    :param token:
    :return:
    """
    res_dir = request.get_json()
    p_id = res_dir['id']
    e_bool = res_dir['bool']
    # noinspection PyBroadException
    try:
        _product = Products.query.filter_by(id=p_id).first()
        _product.active = e_bool
        db.session.flush()
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = None
    return Succ200.to_dict()


@product.route('/product/edit', methods=METHODS)
@login_required()
@verify_param(['id', 'name', 'price'])
def edit(token):
    res_dir = request.get_json()
    e_id = res_dir['id']
    e_name = res_dir['name']
    price = res_dir['price']
    # noinspection PyBroadException
    try:
        _product = Products.query.filter_by(id=e_id).first()
        _product.name = e_name
        _product.price = price
        db.session.commit()
    except Exception:
        return Error409.to_dict()
    Succ200.data = None
    return Succ200.to_dict()


def get_product_name(p_id):
    if p_id not in PRODUCT_LIST:
        product_info = Products.query.filter_by(id=p_id).first()
        PRODUCT_LIST[p_id] = product_info.name
    return PRODUCT_LIST[p_id]
