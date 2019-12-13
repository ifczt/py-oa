from app import db

Base = db.Model


class Express(Base):
    __tablename__ = "express_info"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))
    freight = db.Column(db.Float(24))
    active = db.Column(db.Integer, default=1)

    def to_dict(self):
        model_dict = dict(self.__dict__)
        del model_dict['_sa_instance_state']
        return model_dict
