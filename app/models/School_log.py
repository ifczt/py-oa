"""
    Created by IFCZT on  2020/1/9 16:12
"""
import time

from settings import TIME_STR

__author__ = 'IFCZT'
from app import db

Base = db.Model


class School_log(Base):
    __tablename__ = "school_log"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.String(128))
    school_code = db.Column(db.String(128))
    title = db.Column(db.String(255))
    content = db.Column(db.String())
    status = db.Column(db.Integer, default=1)
    input_time = db.Column(db.DateTime(), default=time.strftime(TIME_STR, time.localtime()))

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
