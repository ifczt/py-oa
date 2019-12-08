from app import db

Base = db.Model


class Orders(Base):
    __tablename__ = "order_info"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    ppg_id = db.Column(db.Integer)
    school = db.Column(db.String(32))
    buy_product = db.Column(db.Integer, db.ForeignKey('product_info.id'))  # 设置Product的外键
    apply_discount_state = db.Column(db.Integer)
    price = db.Column(db.Float(10))
    pay_method = db.Column(db.String(16))
    parent = db.Column(db.String(16))
    student = db.Column(db.String(16))
    consignee = db.Column(db.String(16))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(16))
    publicist = db.Column(db.String(128))
    province = db.Column(db.String(16))
    city = db.Column(db.String(16))
    area = db.Column(db.String(16))
    input_staff = db.Column(db.String(64))
    input_time = db.Column(db.DateTime())  # 订单录入时间
    delivery = db.Column(db.Integer)  # 派送方式
    delivery_time = db.Column(db.DateTime())  # 派送时间
    delivery_state = db.Column(db.Integer)
    update_staff = db.Column(db.String(64))
    update_time = db.Column(db.DateTime())
    courier_code = db.Column(db.String(255))

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
