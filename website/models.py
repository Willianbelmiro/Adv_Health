from . import db

from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(150), unique=True)
  password = db.Column(db.String(150))
  first_name = db.Column(db.String(150))
  car_owners = db.relationship('Owner')

class Owner(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(150))
  gender = db.Column(db.String(150))
  email = db.Column(db.String(150))
  phone = db.Column(db.String(150))
  address = db.Column(db.String(150))
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  status = db.Column(db.Boolean, default=True)
  cars = db.relationship('Car')

class Car(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))
  color_id = db.Column(db.Integer, db.ForeignKey('color.id'))
  model_id = db.Column(db.Integer, db.ForeignKey('model.id'))
  model = db.relationship('Model')
  color = db.relationship('Color')
  status = db.Column(db.Boolean, default=True)

class Model(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(150))
  status = db.Column(db.Boolean, default=True)

class Color(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(150))
  status = db.Column(db.Boolean, default=True)