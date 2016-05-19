from flask import Blueprint, render_template, flash, request, url_for, redirect
from project import app, mysql, db, conn
from .model import Departamento, Provincia, Ciudad
from .resources import GetDepartamentos, GetProvincias
from .form import MercadoForm, CiudadForm

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
    #conn = mysql.connect()
    #cursor = conn.cursor()
    #cursor.callproc('ir_obtenerProvincias',(dep_id,))
    #data = cursor.fetchall()
    departamento = Departamento.query.filter(Departamento.idDepartamento==dep_id).first()
    #print(departamento.nombre)
    data = Provincia.query.filter_by(Departamento_idDepartamento=dep_id)
    regions = []
    f = 1
    for item in data:
        i = {
            #'Id' : item.idDepartamento,
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
            #'Id' : item.idDepartamento,
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
    form = CiudadForm(obj=ciudad)
    form.Provincia_idProvincia.query = Provincia.query.filter(Provincia.idProvincia==ciudad.Provincia_idProvincia)

    if form.validate_on_submit():
        form.populate_obj(ciudad)
        ciudad.Provincia_idProvincia = form.Provincia_idProvincia.data.idProvincia
        db.session.commit()
        flash("Success")
        return redirect(url_for("departament"))

    return render_template("regions/registro.html", action="Edit", form=form)




@app.route('/mercados/registro', methods=['GET', 'POST'])
def registro_mercado():
    form = MercadoForm()
    if form.validate_on_submit():
        flash("Success")
        return redirect(url_for("homepage"))

    return render_template("mercados/registro.html", form=form)

"""@app.route('/mercados/registro', methods=['GET', 'POST'])
def provincia_form():
    form = ProvinciaForm()
    if form.validate_on_submit():
        flash("Success")
        return redirect(url_for("homepage"))

    return render_template("mercados/registro.html", form=form)"""

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
