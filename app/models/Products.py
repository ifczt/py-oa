from app import db

Base = db.Model


class Products(Base):
    __tablename__ = "product_info"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    sub_product = db.Column(db.String(255))
    price = db.Column(db.Integer)
    convert = db.Column(db.Float)
    cost = db.Column(db.Float)
    active = db.Column(db.Integer, default=1)
    orders = db.relationship("Orders", backref='product', lazy='dynamic')  # 关联订单表

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
