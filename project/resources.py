from flask_restful import Resource, Api
from project import mysql, api, conn
from .model import Departamento, Provincia, Ciudad, Producto, Variedad, Clima, Noticia
from sqlalchemy import desc
from .parser import fecha_parser
from datetime import datetime, timedelta

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

class GetClimaCiudadActual(Resource):
    def get(self, ciudad_id):
        try:
            info = []
            data = Clima.query.filter_by(ciudad_idciudad=ciudad_id).order_by(desc(Clima.fecha)).limit(20)
            temp = []
            humedad = []
            climas = []
            icono = []
            descripcion = []
            dia = (datetime.now()).strftime("%Y-%m-%d")


            for item in data:

                splts = str(item.fecha).split()
                if(splts[0] == dia):
                    humedad.append(int(item.humedad))
                    temp.append(float(item.temperatura_maxima))
                    temp.append(float(item.temperatura_minima))
                    icono.append(item.imagen)
                    descripcion.append(item.descripcion)
                    i = {
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

            clima = {
                'fecha': dia,
                'climas' : climas,
                'temp_max': max(temp),
                'temp_min': min(temp),
                'humedad': str(max(humedad)) + "-" + str(min(humedad)),
                'icono': max(set(icono), key=icono.count),
                'descripcion': max(set(descripcion), key=descripcion.count),
            }
            info.append(clima)
            return {'StatusCode':'200','data':info}
        except Exception as e:
            return {'error': str(e)}

class GetClimaCiudadSemana(Resource):
    def get(self, ciudad_id):
        try:
            data = Clima.query.filter_by(ciudad_idciudad=ciudad_id).order_by(desc(Clima.fecha))
            info = []
            for n in range(0,3):
                temp = []
                humedad = []
                climas = []
                icono = []
                descripcion = []
                dia = (datetime.now() - timedelta(n)).strftime("%Y-%m-%d")


                for item in data:


                    splts = str(item.fecha).split()
                    if(splts[0] == dia):
                        humedad.append(int(item.humedad))
                        temp.append(float(item.temperatura_maxima))
                        temp.append(float(item.temperatura_minima))
                        icono.append(item.imagen)
                        descripcion.append(item.descripcion)
                        i = {
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

                clima = {
                    'fecha': dia,
                    'climas' : climas,
                    'temp_max': max(temp),
                    'temp_min': min(temp),
                    'humedad': str(max(humedad)) + "-" + str(min(humedad)),
                    'icono': max(set(icono), key=icono.count),
                    'descripcion': max(set(descripcion), key=descripcion.count),
                }
                info.append(clima)

            return {'StatusCode':'200','data':info}
        except Exception as e:
            return {'error': str(e)}

class GetCiudad(Resource):
    def get(self, ciudad_id):
        try:
            ciudad = Ciudad.query.get(ciudad_id)
            provincia = Provincia.query.get(ciudad.Provincia_idProvincia)
            departamento = Departamento.query.get(provincia.Departamento_idDepartamento)

            i = {
                'Id' : ciudad.idCiudad,
                'Nombre' : ciudad.nombre,
                'Latitud' : ciudad.latitud,
                'Longitud' : ciudad.longitud,
                'Provincia' : provincia.nombre,
                'Departamento' : departamento.nombre
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

class GetNoticias(Resource):
    def get(self):
        try:
            data = Noticia.query.order_by(desc(Noticia.fecha)).limit(10)
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

            return {'StatusCode':'200','noticias':noticias}
        except Exception as e:
            return {'error': str(e)}
GetClimaCiudadSemana
api.add_resource(GetDepartamentos, '/getDepartamentos', methods=['GET',])
api.add_resource(GetProductos, '/getProductos', methods=['GET',])
api.add_resource(GetNoticias, '/getNoticias', methods=['GET',])
api.add_resource(GetProvincias, '/getProvincias/<int:dep_id>', methods=['GET',])
api.add_resource(GetCiudades, '/getCiudades/<int:prov_id>', methods=['GET',])
api.add_resource(GetCiudad, '/getCiudad/<int:ciudad_id>', methods=['GET',])
api.add_resource(GetClimaCiudad, '/getClima/<int:ciudad_id>', methods=['GET',])
api.add_resource(GetClimaCiudadActual, '/getClimaActual/<int:ciudad_id>', methods=['GET',])
api.add_resource(GetClimaCiudadSemana, '/getClimaSemana/<int:ciudad_id>', methods=['GET',])
api.add_resource(GetVariedades, '/getVariedades/<int:producto_id>', methods=['GET',])
