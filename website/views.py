from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import Car, Owner, Model, Color, User
from . import db
import json
views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
@login_required
def owners():
  page = request.args.get('page', 1, type=int)
  
  pagination = Owner.query.filter_by(status=True).paginate(page=page, per_page=10) 
  for owner in pagination.items:
    owner.car_number = len(owner.cars)

  return render_template("home.html", pagination=pagination, user=current_user)

@views.route('/owner', methods=['GET', 'POST'])
@login_required
def create_owner():

  id = request.args.get('id')

  if id is None:
      owner = None
      action = 'added'
  else:
    owner = Owner.query.get(id)
    action = 'updated'

  if request.method =='POST':
    if owner is None:
      owner = Owner()

    owner.gender
    owner.name = request.form.get('name')
    owner.gender = request.form.get('gender')
    owner.email = request.form.get('email')
    owner.phone = request.form.get('phone')
    owner.address = request.form.get('address')
    owner.user_id = current_user.id
    db.session.add(owner)
    db.session.commit()
    flash(f'Car owner {action}!', category='success')
    return redirect(f"/profile?id={owner.id}")
  return render_template("create_owner.html", owner=owner, user=current_user)

@views.route('/profile', methods=['GET'])
@login_required
def profile():
  owner = Owner.query.get(request.args.get('id')) 
  return render_template("profile.html", show_predictions_modal=True, owner=owner, user=current_user, sales_opportunity=3-len(owner.cars))

@views.route('/car', methods=['GET', 'POST'])
@login_required
def create_car():
  id = request.args.get('id')
  if id is None:
      car = None
      action = 'added'
  else:
    car = Car.query.get(id)
    action = 'updated'

  if request.method =='POST':
    owner = Owner.query.get(request.form.get('owner_id'))
    if car is None:
      car = Car()
    if len(owner.cars) >= 3 and action == 'added':
      flash(f'The owner can\'t have more cars.', category='error')
    else:
      car.owner_id = request.form.get('owner_id')
      car.color_id = request.form.get('color')
      car.model_id = request.form.get('model')
      
      db.session.add(car)
      db.session.commit()
      flash(f'Car {action}!', category='success')
  elif request.method =='GET':
    owner = Owner.query.get(request.args.get('owner_id'))
  
  models=Model.query.filter_by(status=True).all()
  colors=Color.query.filter_by(status=True).all()

  if len(models) == 0:
    model = Model()
    model.name = 'Convertible'
    db.session.add(model)
    model = Model()
    model.name = 'Hatch'
    db.session.add(model)
    model = Model()
    model.name = 'Sedan'
    db.session.add(model)
    db.session.commit()
    models=Model.query.filter_by(status=True).all()

  if len(colors) == 0:
    color = Color()
    color.name = 'Blue'
    db.session.add(color)
    color = Color()
    color.name = 'Gray'
    db.session.add(color)
    color = Color()
    color.name = 'Yellow'
    db.session.add(color)
    db.session.commit()
    colors=Color.query.filter_by(status=True).all()

  return render_template("create_car.html", car=car, owner=owner, user=current_user, models=models, colors=colors)

@views.route('/delete-owner', methods=['POST'])
def delete_owner():
  data = json.loads(request.data)
  owner = Owner.query.get(data['ownerId'])
  if owner:
    if owner.user_id == current_user.id:
      db.session.delete(owner)
      db.session.commit()
  return jsonify({})

@views.route('/delete-car', methods=['POST'])
def delete_car():
  data = json.loads(request.data)
  car = Car.query.get(data['carId'])
  if car:
    db.session.delete(car)
    db.session.commit()
  return jsonify({})
