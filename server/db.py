# https://docs.sqlalchemy.org/en/13/core/type_basics.html
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "app_user"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    token = db.Column(db.String(50))
    login = db.Column(db.Integer)
    is_admin = db.Column(db.Integer)

    def __init__(self, name, user_id, token, login, is_admin):
        self.name = name
        self.user_id = user_id
        self.token = token
        self.login = login
        self.is_admin = is_admin

class Scanner(db.Model):
    __tablename__ = "scanner"
    id = db.Column(db.Integer, primary_key = True)
    device_id = db.Column(db.Integer)
    device_name = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, device_id, device_name, user_id):
        self.device_id = device_id
        self.device_name = device_name
        self.user_id = user_id

class ScannerReading(db.Model):
    __tablename__ = "scanner_reading"
    id = db.Column(db.Integer, primary_key = True)
    scanner_id = db.Column(db.Integer, db.ForeignKey("scanner.id"))
    scan_time = db.Column(db.DateTime)
    temperature = db.Columnn(db.Float)

    def __init__(self, scanner_id, scan_time, temperature):
        self.scanner_id = scanner_id
        self.scan_time = scan_time
        self.temperature = temperature



def login_user(user_id):
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return None
    else:
        row.login = 1
        db.session.commit()
    