from flask import request, jsonify, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import functools
from py_oa.utils.code_dict import Error410, Error404
from settings import SECRET_KEY


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


def login_required(api_func):
    @functools.wraps(api_func)
    def verify_token(*args, **kwargs):
        try:
            # 在请求头上拿到token
            token = request.headers["X-Token"]
        except Exception:
            # 没接收的到token,给前端抛出错误
            return Error404.to_dict()
        s = Serializer(SECRET_KEY)
        try:
            u_id = s.loads(token)['u_id']
        except Exception:
            return Error410.to_dict()

        return api_func(u_id, **kwargs)

    return verify_token