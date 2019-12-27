# -*- coding: UTF-8 -*-
import calendar
import datetime

from flask import Blueprint, request
from sqlalchemy import func, extract
from sqlalchemy.sql import and_

from api.orders import publicist_safety
from app import db
from app.models.Orders import Orders
from app.models.Users import Users
from models.Products import Products
from settings import METHODS, INSIDE, PUBLICIST, LEGEND
from utils.code_dict import Succ200, Error4015, Error4016, Error4019, Error4017, Error4018
from utils.common import login_required

data_show = Blueprint("data_show", __name__)


# region 获取销售额 公司内部可看到全市场 加盟商可看到负责区域 电销可看到自己名下及所创建
@data_show.route('/data_show/get_sales_volume', methods=METHODS)
@login_required()
def get_sales_volume(token):
    year = str(datetime.datetime.now().year)
    power = token['power']
    u_id = token['u_id']
    income = 0
    # noinspection PyBroadException
    try:
        master_sql = db.session.query(Products.name.label('product'),
                                      func.sum(Orders.buy_num), Products.price, Products.convert, Products.cost,func.sum(Orders.payment)).join(
            Products, Products.id == Orders.buy_product).group_by('product').filter(
            and_(Orders.delivery_state == 1, extract('year', Orders.input_time) == year))
        if power in INSIDE:
            payment_list = master_sql.all()
            # 把扣取用户的费用也给加上 退货产生的费用
            charge = db.session.query(func.sum(Orders.payment)).filter(
                and_(Orders.delivery_state != 1, extract('year', Orders.input_time) == year)).all()
            charge = charge[0]
            for li in payment_list:
                num = int(li[1])
                income += num * (li[2] * li[3]) + num * (li[4] or 0)
            payment = int(income) + int(charge[0] or 0)
        else:
            payment_list_0 = power_sql(master_sql, token).filter(Orders.payment == 0).all()
            payment_list_1 = power_sql(master_sql, token).filter(Orders.payment != 0).all()
            # 计算运费
            sql = db.session.query(func.sum(Orders.freight)).filter(extract('year', Orders.input_time) == year)
            freight = power_sql(sql, token).all()
            for li in payment_list_0:
                num = int(li[1])
                income += num * (li[2] * (1 - li[3])) - num * (li[4] or 0)
            for li in payment_list_1:
                income += int(li[5])
            freight = freight[0][0] or 0 if freight[0] else 0
            print(freight)
            payment = int(income)-int(freight)
            # master_sql = db.session.query(func.sum(Orders.payment)).filter(
            #     and_(Orders.delivery_state == 1, extract('year', Orders.input_time) == year))
            # payment = power_sql(master_sql, token).scalar() or 0
        Succ200.data = payment
    except Exception:
        return Error4016.to_dict()
    return Succ200.to_dict()


# endregion
# region 获取年度销量 规则同上
@data_show.route('/data_show/get_sales_year', methods=METHODS)
@login_required()
def get_sales_year(token):
    year = str(datetime.datetime.now().year)
    power = token['power']
    # noinspection PyBroadException
    try:
        master_sql = db.session.query(func.sum(Orders.buy_num)).filter(
            and_(Orders.delivery_state == 1, extract('year', Orders.input_time) == year))
        buy_num = power_sql(master_sql, token).scalar() or 0
        Succ200.data = int(buy_num)
    except Exception:
        return Error4015.to_dict()
    return Succ200.to_dict()


# endregion
# region 获取今日销售套数
@data_show.route('/data_show/get_sales_today', methods=METHODS)
@login_required()
def get_sales_today(token):
    day = str(datetime.datetime.now().day)
    # noinspection PyBroadException
    try:
        master_sql = db.session.query(func.sum(Orders.buy_num)).filter(extract('day', Orders.input_time) == day)
        buy_num = power_sql(master_sql, token).scalar() or 0
        Succ200.data = int(buy_num)
    except Exception:
        return Error4017.to_dict()
    return Succ200.to_dict()


# endregion
# region 获取遗留问题件
@data_show.route('/data_show/get_problem_info', methods=METHODS)
@login_required()
def get_problem_info(token):
    # noinspection PyBroadException
    try:
        master_sql = Orders.query.filter_by(delivery_state=6)
        error_num = power_sql(master_sql, token).count()
        Succ200.data = error_num
    except Exception:
        return Error4018.to_dict()
    return Succ200.to_dict()


# endregion
# region 根据用户群组 处理SQL 返回 （非路由函数）
def power_sql(master_sql, token):
    # noinspection PyBroadException
    try:
        power = token['power']
        u_id = token['u_id']
        if power in INSIDE:
            sql = master_sql
        elif power in PUBLICIST:
            sql = master_sql.filter(publicist_safety(u_id, False))
            # sql = master_sql.filter_by(publicist=u_id)
        else:
            sql = master_sql.filter(Orders.input_staff==u_id)
    except:
        return Error4019.to_dict()
    return sql


# endregion
# region 获取LINE-OPTIONS
# region 获取标题
def get_title(month):
    return '%s月数据' % month


# endregion
# region 生成日历
def get_xAxis(month=datetime.datetime.now().month):
    year = datetime.datetime.now().year
    data = []
    if month == datetime.datetime.now().month:
        day = datetime.datetime.now().day + 1
        return list(range(1, day))
    else:
        day = calendar.monthrange(year, 1)[1]
        return list(range(1, day))


# endregion
# region 生成产品线
def get_legend(need_id=False):
    if len(LEGEND) > 0:
        return LEGEND
    data = Products.query.with_entities(Products.name, Products.id).all()
    legend = []
    for item in data:
        if need_id:
            legend.append(item[0:2])
        else:
            legend.append(item[0])
    return legend


# endregion
@data_show.route('/data_show/get_line_options', methods=METHODS)
@login_required()
def get_line_options(token):
    get_line_data()
    res_dir = request.get_json()
    month = res_dir['month'] if res_dir and 'month' in res_dir else datetime.datetime.now().month
    title = get_title(month)
    days = get_xAxis(month)
    legend = get_legend()
    data = {
        'title': title,
        'xAxis': days,
        'legend': legend
    }
    Succ200.data = data
    return Succ200.to_dict()


# endregion
# region 按天 按产品获取数据
@data_show.route('/data_show/get_line_data', methods=METHODS)
@login_required()
def get_line_data(token):
    get_pie_data()
    res_dir = request.get_json()
    month = res_dir['month'] if res_dir and 'month' in res_dir else datetime.datetime.now().month
    master_sql = db.session.query(func.date_format(Orders.input_time, '%d').label('date'),
                                  func.sum(Orders.buy_num)).group_by('date').order_by(
        Orders.input_time).filter(extract('month', Orders.input_time) == month)

    master_sql = power_sql(master_sql, token)
    legend = get_legend(True)
    data = []
    for item in legend:
        _line_data = master_sql.filter(Orders.buy_product == item[1]).all()
        day = get_xAxis(month)
        _data = []
        for i in range(0, len(day)):
            _data.append(0)
        for i in _line_data:
            _data[int(i[0]) - 1] = int(i[1])
        data.append({'name': item[0], 'data': _data, 'type': 'line', 'animationEasing': 'cubicInOut'})
    Succ200.data = data
    return Succ200.to_dict()


# endregion
# region 获取加盟商销售数据
@data_show.route('/data_show/get_pie_data', methods=METHODS)
@login_required()
def get_pie_data(token):
    users = db.session.query(Users.username.label('publicist'),
                             func.sum(Orders.buy_num)).join(Users, Users.u_id == Orders.publicist).group_by(
        'publicist').all()
    legend = []
    data = {'legend': [], 'data': []}
    for item in users:
        data['legend'].append(item[0])
        data['data'].append({'value': int(item[1]), 'name': item[0]})
    Succ200.data = data
    return Succ200.to_dict()
# endregion
