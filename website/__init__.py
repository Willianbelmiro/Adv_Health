from re import S
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "carford_database.db"


def create_app(test_config=None):
  app = Flask(__name__)

  app.config['SECRET_KEY'] = ';laskfgaso123r2inqwe321243aaasdf2'
  app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
  db.init_app(app)

  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  from .models import Car, Owner, Model, Color, User

  create_database(app)

  login_manager = LoginManager()
  login_manager.login_view = 'auth.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(id):
    return User.query.get(int(id))

  return app

def create_database(app):
  if not os.path.exists(f'website/{DB_NAME}'):
    db.create_all(app=app)
    print('Created database!')