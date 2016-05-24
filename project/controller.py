from flask import Blueprint, render_template, flash, request, url_for, redirect
from project import app, db
from flask.ext.login import login_user, login_required, logout_user, current_user
from flask.ext.user import roles_required
from .model import Departamento, Provincia, Ciudad, Manager, Mercado, Clima,  bcrypt
from .resources import GetDepartamentos, GetProvincias
from .form import MercadoForm, CiudadForm, RegisterForm, LoginForm, ClimaForm
from sqlalchemy import desc


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

    return render_template("departament.html", regions = regions)

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
    return render_template("provincias.html", regions = regions, departamento = departamento)

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
    return render_template("ciudades.html", regions = regions, provincia = provincia)

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
        print(item)
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

@app.route('/climas/', methods=['GET', 'POST'])
def climas():
    data = Clima.query.order_by(desc(Clima.fecha)).limit(100)
    climas = []
    for item in data:
        ciudad = Ciudad.query.get(item.ciudad_idciudad)
        splts = str(item.fecha).split()
        i = {
            'Fecha' : splts[0],
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

@app.route('/productos/', methods=['GET', 'POST'])
def mercados():
    data = Mercado.query.all()
    mercados = []
    for item in data:
        i = {
            'Id' : item.idProducto,
            'Nombre' : item.nombre,
            'informacion' : item.informacion,
            'foto': ciudad.foto,
        }
        print(item)
        mercados.append(i)
    return render_template("mercados/mercados.html", mercados = mercados)


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
