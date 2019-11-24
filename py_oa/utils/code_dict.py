# coding=utf-8
class CodeDict(Exception):
    code = -1
    msg = '服务器异常'
    data = None
    @classmethod
    def to_dict(cls, error=None):
        return dict(msg=cls.msg, code=cls.code, data=cls.data)

    pass


class Succ200(CodeDict):
    code = 200
    msg = '成功'
    pass


class Error401(CodeDict):
    code = 401
    msg = '参数错误'
    pass


class Error402(CodeDict):
    code = 402
    msg = '账号与密码不匹配'
    pass


class Error403(CodeDict):
    code = 403
    msg = '找不到该用户'
    pass


class Error4044(CodeDict):
    code = 4044
    msg = '链接数据库失败'
    pass


class Error404(CodeDict):
    code = 404
    msg = '参数不完整'
    pass


class Error410(CodeDict):
    code = 410
    msg = '登录已过期'
    pass


class Error405(CodeDict):
    code = 405
    msg = '宣传编号不存在，请与上级核实。'
    pass