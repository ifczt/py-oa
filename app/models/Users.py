from werkzeug.security import generate_password_hash, check_password_hash
from app import db

Base = db.Model


class Users(Base):
    __tablename__ = "user_info"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.String(64))
    username = db.Column(db.String(32))
    _password = db.Column("password", db.String(128))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)