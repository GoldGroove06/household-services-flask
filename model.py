from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

db = SQLAlchemy()

class users(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    service = db.Column(db.String(150), nullable=True)
    address = db.Column(db.String(150), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    reviews = db.Column(db.String(150), nullable=True)
    status = db.Column(db.String(50), nullable=False)
    s_status = db.Column(db.String(50), nullable=True)
    doc_loc = db.Column(db.String(150), nullable=True)
    


               

class services(db.Model):
    __tablename__ = 'services'
    service_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_name = db.Column(db.String(50), nullable=False)

class cities_list(db.Model):
    __tablename__ = 'cities_list'
    city_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'))
    city_name = db.Column(db.String(50), nullable=False)
    

class packages(db.Model):
    __tablename__ = 'packages'
    package_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    service_id = db.Column(db.Integer, db.ForeignKey('services.service_id'))
    package_name = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    price = db.Column(db.String(50), nullable=False)

class service_req(db.Model):
    __tablename__ = 'service_req'
    req_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cust_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    prof_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    package_id = db.Column(db.Integer, db.ForeignKey('packages.package_id'))
    service_name= db.Column(db.String, db.ForeignKey('services.service_name'))
    status = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    comments = db.Column(db.String(50), nullable=True)
    
