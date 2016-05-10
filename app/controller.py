from flask import render_template, url_for, redirect
from flask_restful import Resource, Api, reqparse
from app import app, mysql, api, db
from .model import Departamento, Provincia

@app.route('/')
@app.route('/home')
def homepage():
    return render_template("main.html")

@app.route('/dep')
def departament():
    try:
#        conn = mysql.connect()
#        cursor = conn.cursor()
#        cursor.execute('''SELECT * from departamento;''')
#        data = cursor.fetchall()
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
    except Exception as e:
        return render_template("main.html", error = e)


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

class GetDepartamentos(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''SELECT * from departamento;''')
            data = cursor.fetchall()
            regions_list = []
            for item in data:
                i = {
                    'Id':item[0],
                    'Departamento':item[1],
                    'Superficie':item[3]
                }
                regions_list.append(i)

            return {'StatusCode':'200','regions':regions_list}
        except Exception as e:
            return {'error': str(e)}

api.add_resource(GetDepartamentos, '/getDepartamentos')
