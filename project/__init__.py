from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask.ext.mysql import MySQL
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from .productos.controller import productos
#from .mercados.controller import mercados
import os

app = Flask(__name__)
# encriptacion para el uso de password
bcrypt = Bcrypt(app)
# usado para el logeo
login_manager = LoginManager()
login_manager.init_app(app)
#configuracion
app.config.from_object('config')

#configuracion de la BD MySql
mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()

#SQl alchemy config
db = SQLAlchemy(app)
# Api congig
api = Api(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
  return response

from project import controller, model, resources, importapi

#Blueprint
app.register_blueprint(productos)
#app.register_blueprint(mercados)
from model import Manager

@login_manager.user_loader
def load_user(user_id):
    return Manager.query.filter(Manager.idManager == int(user_id)).first()
