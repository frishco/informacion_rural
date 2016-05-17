# Import Form and RecaptchaField (optional)
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField # BooleanField

# Import Form validators
from wtforms.validators import Required


# Define the login form (WTForms)

class MercadoForm(Form):
    #email    = TextField('Email Address', [Email(),
    #            Required(message='Forgot your email address?')])

    #password = PasswordField('Password', [
    #            Required(message='Must provide a password. ;-)')])

    nombre = TextField('Nombre del mercado', [
                Required(message='Ingrese mercado')])
    capacidad = TextField('Capacidad del mercado', [
                Required(message='Ingrese la capacidad')])