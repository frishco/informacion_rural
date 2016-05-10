from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from flask.ext.mysql import MySQL
from flask.ext.sqlalchemy import SQLAlchemy
from .productos.controller import productos

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
#Blueprint

app.register_blueprint(productos)



from app import controller, model, resources
