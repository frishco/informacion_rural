from flask import render_template, url_for, redirect
from app import app, mysql, db, conn
from .model import Departamento, Provincia
from .resources import GetDepartamentos, GetProvincias

@app.route('/')
@app.route('/home')
def homepage():
    return render_template("main.html")

@app.route('/dep')
def departament():

    cursor = conn.cursor()
    cursor.callproc('ir_obtenerDepart')
    data = cursor.fetchall()
#        data = Departamento.query.all()
    regions = []
    for item in data:
        i = {
            'Id' : item[0], #item.idDepartamento,
            'Departamento' : item[1], #item.nombre,
            'Descripcion' : item[2], #item.ubicacion,
            'Superficie' : item[3] #item.superficie

        }
        regions.append(i)

    return render_template("departament.html", regions = regions)

@app.route('/prov/<int:dep_id>')
def provincias(dep_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('ir_obtenerProvincias',(dep_id,))
    data = cursor.fetchall()
    regions = []
    f = 1
    for item in data:
        i = {
            #'Id' : item.idDepartamento,
            'Id' : item[0],
            'Numero' : f,
            'Nombre' : item[1],

        }
        regions.append(i)
        f = f + 1
    return render_template("provincias.html", regions = regions)

@app.route('/prov2')
def provincias2():

    data = Provincia.query.filter_by(Departamento_idDepartamento=2)
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
    return render_template("provincias.html", regions = regions)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
