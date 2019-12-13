from app import db

Base = db.Model


class Orders(Base):
    __tablename__ = "order_info"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    ppg_id = db.Column(db.Integer)
    school_code = db.Column(db.String(64), db.ForeignKey('school_info.school_code'))  # ѧУ��� ���ѧУ��Ϣ��SCHOOL_CODE
    buy_product = db.Column(db.Integer, db.ForeignKey('product_info.id'))  # ����Product�����
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
    input_staff = db.Column(db.String(64), db.ForeignKey('user_info.u_id'))  # �������ӵ�USER_INFO���
    input_time = db.Column(db.DateTime())  # ����¼��ʱ��
    delivery = db.Column(db.Integer)  # ���ͷ�ʽ
    delivery_time = db.Column(db.DateTime())  # ����ʱ��
    delivery_state = db.Column(db.Integer)
    update_staff = db.Column(db.String(64))
    update_time = db.Column(db.DateTime())
    courier_code = db.Column(db.String(255))

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
