from app import db

Base = db.Model


class School(Base):
    __tablename__ = "school_info"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    school_code = db.Column(db.String(64))
    school_name = db.Column(db.String(24))
    school_address = db.Column(db.String(255))
    entry_clerk = db.Column(db.String(255))  # ¼��Ա
    contact_info = db.Column(db.String(1024))  # ��ϵ��ʽ
    input_time = db.Column(db.DateTime())  # ¼��ʱ��
    update_time = db.Column(db.DateTime())  # ����ʱ��
    update_clerk = db.Column(db.String(255))  # ����Ա
    region = db.Column(db.String(64))  # ���������
    province = db.Column(db.String(16))
    city = db.Column(db.String(16))
    area = db.Column(db.String(16))
    simple_name = db.Column(db.String(64))  # ѧУ������д
    quality = db.Column(db.String(8))  # ѧУ����

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
