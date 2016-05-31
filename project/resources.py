from flask_restful import Resource, Api
from project import mysql, api, conn
from .model import Departamento, Provincia, Ciudad, Producto, Variedad, Clima
from sqlalchemy import desc

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

class GetClimaCiudad(Resource):
    def get(self, ciudad_id):
        try:
            data = Clima.query.filter_by(ciudad_idciudad=ciudad_id).order_by(desc(Clima.fecha)).limit(8)
            climas = []
            f = 1
            for item in data:
                splts = str(item.fecha).split()
                i = {
                    'Fecha' : splts[0],
                    'Hora' : splts[1],
                    'Id' : item.idclima,
                    'Temp_max' : item.temperatura_maxima,
                    'Temp_min' : item.temperatura_minima,
                    'Descripcion' : item.descripcion,
                    'Humedad' : item.humedad,
                    'Lluvia' : item.lluvia,
                    'Icono' : item.imagen,
                }
                climas.append(i)

            return {'StatusCode':'200','climas':climas}
        except Exception as e:
            return {'error': str(e)}

class GetCiudad(Resource):
    def get(self, ciudad_id):
        try:
            ciudad = Ciudad.query.get(ciudad_id)
            i = {
                'Id' : ciudad.idCiudad,
                'Nombre' : ciudad.nombre,
                'Latitud' : ciudad.latitud,
                'Longitud' : ciudad.longitud
            }

            return {'StatusCode':'200','ciudad':i}
        except Exception as e:
            return {'error': str(e)}

class GetProductos(Resource):
    def get(self):
        try:
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

            return {'StatusCode':'200','productos':productos}
        except Exception as e:
            return {'error': str(e)}


class GetVariedades(Resource):
    def get(self, producto_id):
        try:
            data = Variedad.query.filter_by(Producto_idProducto=producto_id)
            variedades = []
            for item in data:
                i = {
                    'Id' : item.idvariedad,
                    'Nombre' : item.nombre,
                    'Caracteristicas' : item.caracteristicas,
                }
                variedades.append(i)

            return {'StatusCode':'200','variedades':variedades}
        except Exception as e:
            return {'error': str(e)}

api.add_resource(GetDepartamentos, '/getDepartamentos', methods=['GET',])
api.add_resource(GetProductos, '/getProductos', methods=['GET',])
api.add_resource(GetProvincias, '/getProvincias/<int:dep_id>', methods=['GET',])
api.add_resource(GetCiudades, '/getCiudades/<int:prov_id>', methods=['GET',])
api.add_resource(GetCiudad, '/getCiudad/<int:ciudad_id>', methods=['GET',])
api.add_resource(GetClimaCiudad, '/getClima/<int:ciudad_id>', methods=['GET',])
api.add_resource(GetVariedades, '/getVariedades/<int:producto_id>', methods=['GET',])
