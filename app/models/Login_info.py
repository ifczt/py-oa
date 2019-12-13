from app import db

Base = db.Model


class Login_info(Base):
    __tablename__ = "login_info"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.String(64), db.ForeignKey('user_info.u_id'))
    login_time = db.Column(db.DateTime())

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
