# https://docs.sqlalchemy.org/en/13/core/type_basics.html
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "app_user"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    token = db.Column(db.String(50))
    login = db.Column(db.Integer)
    is_admin = db.Column(db.Integer)

    def __init__(self, name, email, password, token, login, is_admin):
        self.name = name
        self.email = email
        self.password = password
        self.token = token
        self.login = login
        self.is_admin = is_admin

class Scanner(db.Model):
    __tablename__ = "scanner"
    id = db.Column(db.Integer, primary_key = True)
    device_id = db.Column(db.Integer)
    device_name = db.Column(db.String(50))
    user_email = db.Column(db.Integer, db.ForeignKey("app_user.email"))
    max_temp = db.Column(db.Float)
    min_temp = db.Column(db.Float)

    def __init__(self, device_id, device_name, user_email, min_temp, max_temp):
        self.device_id = device_id
        self.device_name = device_name
        self.user_email = user_email
        self.min_temp = min_temp
        self.max_temp = max_temp

class ScannerReading(db.Model):
    __tablename__ = "scanner_reading"
    id = db.Column(db.Integer, primary_key = True)
    scanner_id = db.Column(db.Integer, db.ForeignKey("scanner.id"))
    scan_time = db.Column(db.DateTime)
    temperature = db.Column(db.Float)

    def __init__(self, scanner_id, scan_time, temperature):
        self.scanner_id = scanner_id
        self.scan_time = scan_time
        self.temperature = temperature



def find_user_if_exists(email):
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    else:
        user.login = 1
        db.session.commit()
        return user
    

def register_new_user(name, email, password_hash):
    existing_user = User.query.filter_by(email=email).first()
    if not existing_user:
        new_user = User(name, email, password_hash, "", 1, 0)
        db.session.add(new_user)
        db.session.commit()
        return True
    else:
        return False
    

def get_user_scanners(email):
    try:
        scanners_query = Scanner.query.filter_by(user_email=email).all()
        scanners_res = []
        for scanner in scanners_query:
            scanner_dict = {
                "id": scanner.id,
                "device_id": scanner.device_id,
                "device_name": scanner.device_name,
                "user_email": scanner.user_email,
                "min_temp": scanner.min_temp,
                "max_temp": scanner.max_temp
            }
            scanners_res.append(scanner_dict)
        return scanners_res
    except:
        return []


def write_temp(time, scanner, temperature):
    try:
        new_record = ScannerReading(scanner, time, temperature)
        db.session.add(new_record)
        db.session.commit()
        print("Record Added")
        return redirect("/sensors")
    except:
        print("Error")


def update_sensor(id, name, min_temp, max_temp):
    try:
        scanner = Scanner.query.filter_by(device_id=int(id)).first()
        scanner.device_name = name
        scanner.min_temp = min_temp
        scanner.max_temp = max_temp
        db.session.commit()
        print("db ")

    except Exception as e:
        print(e)