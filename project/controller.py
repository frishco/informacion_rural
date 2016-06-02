#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, flash, request, url_for, redirect
from project import app, db
from flask.ext.login import login_user, login_required, logout_user, current_user
from flask.ext.user import roles_required
from .model import Departamento, Provincia, Ciudad, Manager, Mercado, Clima, Producto, Variedad, Precio, Noticia, bcrypt
from .resources import GetDepartamentos, GetProvincias
from .form import MercadoForm, CiudadForm, RegisterForm, LoginForm, PrecioForm, VariedadForm, NoticiaForm
from sqlalchemy import desc
from datetime import datetime
from .parser import fecha_parser


@app.route('/')
@app.route('/home')
def homepage():
    return render_template("main.html")

@app.route('/dep')
def departament():
    #cursor = conn.cursor()
    #cursor.callproc('ir_obtenerDepart')
    #data = cursor.fetchall()"""
    data = Departamento.query.all()
    regions = []
    for item in data:
        i = {
            'Id' : item.idDepartamento,
            'Departamento' : item.nombre,
            'Descripcion' : item.ubicacion,
            'Superficie' : item.superficie

        }
        regions.append(i)

    return render_template("regions/departament.html", regions = regions)

@app.route('/prov/<int:dep_id>')
def provincias(dep_id):
    #cursor = conn.cursor()
    #cursor.callproc('ir_obtenerProvincias',(dep_id,))
    #data = cursor.fetchall()
    departamento = Departamento.query.filter(Departamento.idDepartamento==dep_id).first()
    data = Provincia.query.filter_by(Departamento_idDepartamento=dep_id)
    regions = []
    f = 1
    for item in data:
        i = {
            'IdDepartamento' : item.Departamento_idDepartamento,
            'Id' : item.idProvincia,
            'Numero' : f,
            'Nombre' : item.nombre,
        }
        regions.append(i)
        f = f + 1
    return render_template("regions/provincias.html", regions = regions, departamento = departamento)

@app.route('/ciudades/<int:prov_id>')
def ciudades(prov_id):

    provincia = Provincia.query.filter(Provincia.idProvincia==prov_id).first()
    data = Ciudad.query.filter_by(Provincia_idProvincia=prov_id)
    regions = []
    f = 1
    for item in data:
        i = {
            'Id' : item.idCiudad,
            'Numero' : f,
            'Nombre' : item.nombre,
            'Latitud' : item.latitud,
            'Longitud' : item.longitud
        }
        regions.append(i)
        f = f + 1
    return render_template("regions/ciudades.html", regions = regions, provincia = provincia)

@app.route('/ciudad/<int:ciudad_id>', methods=['GET', 'POST'])
def edit_ciudad(ciudad_id):

    ciudad = Ciudad.query.get(ciudad_id)
    provincia = ciudad.Provincia_idProvincia
    form = CiudadForm(obj=ciudad)
    form.Provincia_idProvincia.query = Provincia.query.filter(Provincia.idProvincia==ciudad.Provincia_idProvincia)

    if form.validate_on_submit():
        form.populate_obj(ciudad)
        ciudad.Provincia_idProvincia = form.Provincia_idProvincia.data.idProvincia
        db.session.commit()
        flash("Success")
        return redirect(url_for("ciudades", prov_id = provincia))

    return render_template("regions/registro.html", action="Edit", form=form)

@app.route('/mercados/', methods=['GET', 'POST'])
@login_required
def mercados():
    data = Mercado.query.all()
    mercados = []
    for item in data:
        ciudad = Ciudad.query.get(item.ciudad_idciudad)
        i = {
            'IdCiudad': item.ciudad_idciudad,
            'Id' : item.idMercado,
            'Nombre' : item.nombre,
            'Capacidad' : item.capacidad,
            'Ciudad': ciudad.nombre,
        }
        mercados.append(i)
    return render_template("mercados/mercados.html", mercados = mercados)

@app.route('/mercados/registro', methods=['GET', 'POST'])
@login_required
def registro_mercado():
    form = MercadoForm()
    if form.validate_on_submit():
        mercado = Mercado(
            nombre = form.nombre.data,
            capacidad = form.capacidad.data,
            ciudad_idciudad = form.ciudad.data,
        )
        db.session.add(mercado)
        db.session.commit()
        flash("Success")
        return redirect(url_for("mercados"))
    return render_template("mercados/registro.html", form=form)

@app.route('/precios/', methods=['GET', 'POST'])
def precios():
    data = Precio.query.order_by(desc(Precio.fecha))
    precios = []
    for item in data:
        mercado = Mercado.query.get(item.Mercado_idMercado)
        ciudad = Ciudad.query.get(mercado.ciudad_idciudad)
        variedad = Variedad.query.get(item.variedad_idvariedad)
        producto = Producto.query.get(variedad.Producto_idProducto)
        i = {
            'Fecha' : item.fecha,
            'Ciudad': ciudad.nombre,
            'Mercado': mercado.nombre,
            'Id' : item.idPrecio,
            'precio_max' : item.precio_max,
            'precio_min' : item.precio_min,
            'precio_promedio' : item.precio_promedio,
            'Variedad' : variedad.nombre,
            'Producto' : producto.nombre,
        }
        precios.append(i)
    return render_template("precios/precios.html", precios = precios)


@app.route('/precios/registro', methods=['GET', 'POST'])
@login_required
def registro_precio():
    form = PrecioForm()
    if form.validate_on_submit():
        precio = Precio(
            precio_promedio = form.precio_promedio.data,
            precio_max = form.precio_max.data,
            precio_min = form.precio_min.data,
            fecha = form.fecha.data,
            variedad_idvariedad = form.variedad.data,
            Mercado_idMercado = form.mercado.data.idMercado,
        )
        db.session.add(precio)
        db.session.commit()
        flash("Success")
        return redirect(url_for("precios"))
    return render_template("precios/registro.html", form=form)

@app.route('/precios/editar/<int:precio_id>', methods=['GET', 'POST'])
@login_required
def editar_precio(precio_id):
    precio = Precio.query.get(precio_id)
    form = PrecioForm(obj=precio)
    if form.validate_on_submit():
        form.populate_obj(precio)
        precio.variedad_idvariedad = form.variedad.data
        precio.Mercado_idMercado = form.mercado.data.idMercado
        db.session.commit()
        flash("Success")
        return redirect(url_for("precios"))
    return render_template("precios/registro.html", form=form)


@app.route('/climas/', methods=['GET', 'POST'])
def climas():
    data = Clima.query.order_by(desc(Clima.fecha)).limit(100)
    climas = []
    for item in data:
        ciudad = Ciudad.query.get(item.ciudad_idciudad)
        splts = str(item.fecha).split()
        i = {
            'Fecha' : fecha_parser(splts[0]),
            'Hora' : splts[1],
            'Ciudad': ciudad.nombre,
            'Id' : item.idclima,
            'Temp_max' : item.temperatura_maxima,
            'Temp_min' : item.temperatura_minima,
            'Descripcion' : item.descripcion,
            'Humedad' : item.humedad,
            'Lluvia' : item.lluvia,
            'Icono' : item.imagen,
        }
        climas.append(i)
    return render_template("climas/climas.html", climas = climas)

@app.route('/climas/delete/<int:clima_id>', methods=['GET', 'POST'])
@login_required
def delete_clima(clima_id):

    clima = Clima.query.get(clima_id)
    db.session.delete(clima)
    db.session.commit()

    return redirect(url_for("climas"))

@app.route('/manager/', methods=['GET', 'POST'])
@login_required
def managers():
    data = Manager.query.all()
    managers = []
    for item in data:
        i = {
            'Id' : item.idManager,
            'Nombre' : item.nombre,
            'Apellido' : item.apellido,
            'Email' : item.email,
            'Rol' : item.role,
        }
        managers.append(i)
    return render_template("manager/managers.html", managers = managers)

@app.route('/productos/', methods=['GET'])
def productos():
    data = Producto.query.all()
    productos = []
    for item in data:
        variedades = []
        data_variedades = Variedad.query.filter_by(Producto_idProducto=item.idProducto)
        for item_v in data_variedades:


            i_v = {
                'Id' : item_v.idvariedad,
                'Nombre' : item_v.nombre,
                'Caracteristicas' : item_v.caracteristicas,
            }
            variedades.append(i_v)

        i = {
            'Id' : item.idProducto,
            'Nombre' : item.nombre,
            'Informacion' : item.informacion,
            'Imagen': item.imagen,
            "Variedades": variedades,
        }
        productos.append(i)
    return render_template("productos/productos.html", productos = productos)

@app.route('/productos/<int:producto_id>', methods=['GET'])
def producto(producto_id):
    data = Variedad.query.filter_by(Producto_idProducto=producto_id)
    producto = Producto.query.get(producto_id)
    productos = []
    for item in data:


        i = {
            'Id' : item.idvariedad,
            'Nombre' : item.nombre,
            'Caracteristicas' : item.caracteristicas,
            'Imagen': item.Producto_idProducto,
        }
        productos.append(i)
    return render_template("productos/productos.html", productos = productos)

@app.route('/productos/registro', methods=['GET', 'POST'])
def registro_producto():
    form = VariedadForm()
    if form.validate_on_submit():

        variedad = Variedad(
            nombre = form.nombre.data,
            caracteristicas = form.caracteristicas.data,
            Producto_idProducto = form.producto.data.idProducto,
        )
        db.session.add(variedad)
        db.session.commit()
        flash("Success")
        return redirect(url_for("productos"))
    return render_template("productos/registro.html", form=form)

@app.route('/noticias/', methods=['GET', 'POST'])
def noticias():
    data = Noticia.query.all()
    noticias = []
    for item in data:
        fecha = fecha_parser(item.fecha)

        i = {
            'Id' : item.idNoticia,
            'Titulo' : item.titulo,
            'Cuerpo' : item.cuerpo,
            'Fecha' : fecha,
            'Fuente' : item.fuente,
            'Imagen' : item.imagen,
        }
        noticias.append(i)
    return render_template("noticias/noticias.html", noticias = noticias)


@app.route('/noticias/registro', methods=['GET', 'POST'])
@login_required
def registro_noticia():
    form = NoticiaForm()
    if form.validate_on_submit():

        noticia = Noticia(
            titulo = form.titulo.data,
            cuerpo = form.cuerpo.data,
            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            fuente = form.fuente.data,
            imagen = form.imagen.data,
        )
        db.session.add(noticia)
        db.session.commit()
        flash("Success")
        return redirect(url_for("productos"))
    return render_template("noticias/registro.html", form=form)

@app.route('/manager/profile', methods=['GET', 'POST'])
@login_required
def profile():

    return render_template("manager/profile.html")

@app.route('/manager/register', methods=['GET', 'POST'])
@login_required
def registro_form():
    form = RegisterForm()
    if form.validate_on_submit():
        manager = Manager(
            nombre = form.nombre.data,
            apellido = form.apellido.data,
            email = form.email.data,
            password = form.password.data,
        )
        db.session.add(manager)
        db.session.commit()
        flash("Success")
        return redirect(url_for("managers"))

    return render_template("manager/registro.html", form=form)

# Logeo de admin y encuestadores


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        manager = Manager.query.filter_by(email=form.email.data).first()
        if manager is not None and bcrypt.check_password_hash(
            manager.password, form.password.data
        ):
            login_user(manager)
            flash('Ya estas logeado.')
            return redirect(url_for('homepage'))

    return render_template('manager/login.html', form=form)

@app.route('/logout')   # pragma: no cover
@login_required   # pragma: no cover
def logout():
    logout_user()
    flash('You were logged out.')
    return redirect(url_for('homepage'))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
