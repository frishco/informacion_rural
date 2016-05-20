from flask_restful import Resource, Api
from project import mysql, api, conn
from .model import Departamento, Provincia, Ciudad

class GetDepartamentos(Resource):
    def get(self):
        try:
            cursor = conn.cursor()
            cursor.callproc('ir_obtenerDepart')
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

class GetProvincias(Resource):
    def get(self, dep_id):
        try:
            cursor = conn.cursor()
            cursor.callproc('ir_obtenerProvincias',(dep_id,))
            data = cursor.fetchall()
            regions_list = []
            for item in data:
                i = {
                    'Id':item[0],
                    'Nombre':item[1]
                }
                regions_list.append(i)

            return {'StatusCode':'200','regions':regions_list}
        except Exception as e:
            return {'error': str(e)}
class GetCiudades(Resource):
    def get(self, prov_id):
        try:
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

            return {'StatusCode':'200','regions':regions}
        except Exception as e:
            return {'error': str(e)}

api.add_resource(GetDepartamentos, '/getDepartamentos', methods=['GET',])
api.add_resource(GetProvincias, '/getProvincias/<int:dep_id>', methods=['GET',])
api.add_resource(GetCiudades, '/getCiudades/<int:prov_id>', methods=['GET',])
