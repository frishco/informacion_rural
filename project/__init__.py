from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask.ext.mysql import MySQL
from flask.ext.sqlalchemy import SQLAlchemy
from .productos.controller import productos
#from .mercados.controller import mercados

import os



app = Flask(__name__)
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


from project import controller, model, resources

#Blueprint
app.register_blueprint(productos)
#app.register_blueprint(mercados)
