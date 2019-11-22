from py_oa import db

Base = db.Model


class Orders(Base):
    __tablename__ = "order_info"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    ppg_id = db.Column(db.Numeric(8))
    school = db.Column(db.String(32))
    buy_product = db.Column(db.String(64))
    apply_discount_state = db.Column(db.Numeric(2))
    price = db.Column(db.DECIMAL(10))
    pay_method = db.Column(db.String(16))
    parent = db.Column(db.String(16))
    student = db.Column(db.String(16))
    consignee = db.Column(db.String(16))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(16))
    province = db.Column(db.String(16))
    publicist = db.Column(db.String(128))
    city = db.Column(db.String(16))
    area = db.Column(db.String(16))
    input_staff = db.Column(db.String(64))
    input_time = db.Column(db.DateTime())
    delivery = db.Column(db.Numeric(2))
    delivery_time = db.Column(db.DateTime())
    delivery_state = db.Column(db.Numeric(2))
