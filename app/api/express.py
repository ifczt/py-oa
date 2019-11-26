# -*- coding: UTF-8 -*-
from flask import Blueprint
from models.Express import Express
from settings import METHODS, EXPRESS_NAME
from utils.code_dict import Succ200

express = Blueprint("express", __name__)


@express.route('/express_list', methods=METHODS)
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


def get_express_name(id):
    if id not in EXPRESS_NAME:
        express_info = Express.query.filter_by(id=id).first()
        if not express_info:
            return
        EXPRESS_NAME[id] = express_info.name
    return EXPRESS_NAME[id]

