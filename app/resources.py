from flask_restful import Resource, Api
from app import mysql, api, conn

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
api.add_resource(GetDepartamentos, '/getDepartamentos', methods=['GET',])
api.add_resource(GetProvincias, '/getProvincias/<int:dep_id>', methods=['GET',])
