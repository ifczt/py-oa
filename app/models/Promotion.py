from app import db

Base = db.Model


class Promotion(Base):
    __tablename__ = "promotion_info"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    publicist_id = db.Column(db.String(64))  # ������
    sales_nums = db.Column(db.Integer)  # �ǵ���
    dosage = db.Column(db.Integer)  # ������
    school_code = db.Column(db.String(32))
    promotion_time = db.Column(db.DateTime())  # ��������
    province = db.Column(db.String(24))
    city = db.Column(db.String(1024))
    area = db.Column(db.String(1024))

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict