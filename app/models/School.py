from app import db

Base = db.Model


class School(Base):
    __tablename__ = "school_info"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    school_code = db.Column(db.String(64))
    school_name = db.Column(db.String(24))
    school_address = db.Column(db.String(255))
    entry_clerk = db.Column(db.String(255))  # 录入员
    contact_info = db.Column(db.String(1024))  # 联系方式
    input_time = db.Column(db.DateTime())  # 录入时间
    update_time = db.Column(db.DateTime())  # 更新时间
    update_clerk = db.Column(db.String(255))  # 更新员
    region = db.Column(db.String(64))  # 组合区域汉字
    province = db.Column(db.String(16))
    city = db.Column(db.String(16))
    area = db.Column(db.String(16))
    simple_name = db.Column(db.String(64))  # 学校名称缩写
    quality = db.Column(db.String(8))  # 学校质量

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
