from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from flask.ext.mysql import MySQL
from flask.ext.sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_object('config')
mysql = MySQL()
mysql.init_app(app)
db = SQLAlchemy(app)
api = Api(app)

from app import controller, model
