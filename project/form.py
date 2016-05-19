# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import StringField, PasswordField # BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
#from wtforms_sqlalchemy.orm import model_form
# Import Form validators
from wtforms.validators import Required

from .model import Departamento, Provincia


def provincias_dep():
    return Provincia.query.filter_by(Departamento_idDepartamento=2)


# Define the login form (WTForms)

class MercadoForm(Form):


    nombre = StringField('Nombre del mercado', [
                Required(message='Ingrese mercado')])

    capacidad = StringField('Capacidad del mercado', [
                Required(message='Ingrese la capacidad')])

    departamento = QuerySelectField(query_factory=lambda: Departamento.query.all())

    provincia = QuerySelectField(query_factory = provincias_dep)


class CiudadForm(Form):

    nombre = StringField('Nombre de la ciudad', [
                Required(message='Ingrese el nombre de la ciudad')])

    latitud = StringField('Ingrese la longitud', [
                Required(message='Ingrese la longitud')])

    longitud = StringField('Ingrese la longitud', [
                Required(message='Ingrese la longitud')])

    Provincia_idProvincia = QuerySelectField(get_label='nombre')
