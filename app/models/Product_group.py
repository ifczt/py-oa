"""
    Created by IFCZT on  2020/1/9 16:12
"""
__author__ = 'IFCZT'
from app import db

Base = db.Model


class Product_group(Base):
    __tablename__ = "product_group_info"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    sub_product = db.Column(db.String(255))


    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
