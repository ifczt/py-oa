import functools

from flask import request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app.utils.code_dict import Error410, Error404, Error408
from settings import SECRET_KEY, IFCZT


def create_token(user_info):
    """
    生成token
    :param user_info:用户信息
    :return: token
    """
    s = Serializer(SECRET_KEY, expires_in=3600)
    # 接收用户id转换与编码
    token = s.dumps(user_info).decode("ascii")
    return token


def login_required(power_group=None):
    def token_required(api_func):
        @functools.wraps(api_func)
        def verify_token(*args, **kwargs):
            # noinspection PyBroadException
            try:  # 在请求头上拿到token
                token = request.headers["X-Token"]
            except Exception:
                # 没接收的到token,给前端抛出错误
                return Error404.to_dict()
            s = Serializer(SECRET_KEY)
            # noinspection PyBroadException
            try:  # 获取参数
                u_id = s.loads(token)['u_id']
                power = s.loads(token)['power']
                name = s.loads(token)['name']
            except Exception:
                return Error410.to_dict()
            if power_group is not None:  # 如果传进来权限群组了 则判断是否在权限范围内
                if power not in power_group and power not in IFCZT:
                    return Error408.to_dict()
            return api_func({'u_id': u_id, 'power': power, 'name': name}, **kwargs)

        return verify_token

    return token_required


def verify_param(rules):
    def decorator(api_func):
        @functools.wraps(api_func)
        def wrapper(*args, **kwargs):
            res_dir = request.get_json()
            print(res_dir, 'verify_param')
            if not res_dir:
                return Error404.to_dict()
            for rule in rules:
                if type(res_dir[rule]) is not int:
                    if rule not in res_dir or res_dir[rule] is None or len(res_dir[rule]) == 0:
                        return Error404.to_dict()
            return api_func(*args, **kwargs)

        return wrapper

    return decorator
