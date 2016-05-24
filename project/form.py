#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Form
from flask.ext.wtf import Form # , RecaptchaField

# Import Form elements such as StringField and BooleanField (optional)
from wtforms import StringField, PasswordField, SelectField, DateTimeField, ValidationError # BooleanField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
# from wtforms_sqlalchemy.orm import model_form

# Import Form validators
from wtforms.validators import Required, Length, Email, EqualTo

from .model import Departamento, Provincia, Ciudad, Manager, Clima

# Query para los SelectField
def provincias_dep():
    return Provincia.query.filter_by(Departamento_idDepartamento=2)

# Formularios para el logeo de los managers

class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class LoginForm(Form):
    email = StringField('Email', validators=[Required(message='Ingrese su email')])
    password = PasswordField('Password', validators=[Required(message='Ingrese su password')])


class RegisterForm(Form):
    nombre = StringField(
        'nombre',
        validators=[Required(message='Debe ingresar el nombre'), Length(min=3, max=25)]
    )
    apellido = StringField(
        'apellido',
        validators=[Required(message='Debe ingresar el apellido'), Length(min=3, max=25)]
    )
    email = StringField(
        'email',
        validators=[Required(message='Debe ingresar un email'), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        'password',
        validators=[Required(message='Ingrese una password'), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Repeat password',
        validators=[
            Required(message='Confirme su contraseña'), EqualTo('password', message='Passwords must match.')
        ]
    )

# Formulario para el ingreso de mercados

class MercadoForm(Form):


    nombre = StringField('Nombre del mercado', [
                Required(message='Ingrese mercado')])

    capacidad = StringField('Capacidad del mercado', [
                Required(message='Ingrese la capacidad')])

    departamento = QuerySelectField(query_factory=lambda: Departamento.query.all(), allow_blank=True, blank_text='--seleccionar--')

    provincia = NonValidatingSelectField(u'', choices=(),
        validators=[Required(message='Seleccione una provincia')])

    ciudad = NonValidatingSelectField(u'', choices=())

    def validate_ciudad(self, field):

        if not Ciudad.query.filter_by(idCiudad=field.data).first():
            raise ValidationError('Seleccione una ciudad')

class CiudadForm(Form):

    nombre = StringField('Nombre de la ciudad', [
                Required(message='Ingrese el nombre de la ciudad')])

    latitud = StringField('Ingrese la longitud', [
                Required(message='Ingrese la longitud')])

    longitud = StringField('Ingrese la longitud', [
                Required(message='Ingrese la longitud')])

    Provincia_idProvincia = QuerySelectField(get_label='nombre')


class ClimaForm(Form):


    temperatura_maxima = StringField('Ingrese la temperatura maxima', [
                Required(message='ingrese dato')])

    temperatura_minima = StringField('Ingrese la temperatura minima', [
                Required(message='ingrese dato')])

    fecha = DateTimeField('Fecha pues', [
                Required(message='ingrese dato')])

    descripcion = StringField('Ingrese la descripcion', [
                Required(message='ingrese dato')])

    lluvia = StringField('Ingrese la lluvia', [
                Required(message='ingrese dato')])

    imagen = StringField('Ingrese la imagen', [
                Required(message='ingrese dato')])

    departamento = QuerySelectField(query_factory=lambda: Departamento.query.all(), allow_blank=True, blank_text='--seleccionar--')

    provincia = NonValidatingSelectField(u'', choices=(),
        validators=[Required(message='Seleccione una provincia')])

    ciudad = NonValidatingSelectField(u'', choices=())

    def validate_ciudad(self, field):

        if not Ciudad.query.filter_by(idCiudad=field.data).first():
            raise ValidationError('Seleccione una ciudad')
