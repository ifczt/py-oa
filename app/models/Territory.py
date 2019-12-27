from app import db

Base = db.Model


class Territory(Base):
    __tablename__ = "territory_info"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    publicist = db.Column(db.String(64))
    province = db.Column(db.String(16))
    city = db.Column(db.String(1024))
    product = db.Column(db.String(255))
    eff_time = db.Column(db.DateTime())
    start_time = db.Column(db.DateTime())

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
