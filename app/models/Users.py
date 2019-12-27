from werkzeug.security import generate_password_hash, check_password_hash

from app import db


Base = db.Model


class Users(Base):
    __tablename__ = "user_info"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.String(64))
    username = db.Column(db.String(32))
    _password = db.Column("password", db.String(128))
    power = db.Column(db.String(8))
    active = db.Column(db.Integer, default=1)
    superior = db.Column(db.String(64))
    promotion = db.relationship("Promotion", backref='promotion_user', lazy='dynamic')  # 产品宣传
    login = db.relationship("Login_info", backref='login_user', lazy='dynamic')  # 登录表 操作
    orders = db.relationship("Orders", backref='orders_user', lazy='dynamic')  # 产品列表

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
