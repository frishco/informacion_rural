from project import app, db
from .model import Departamento, Provincia, Ciudad, Clima
from flask import  render_template, flash, request, url_for, redirect
from flask.ext.login import login_required

import requests
import simplejson
import json

@app.route("/lat_lon/<int:ciudad_id>")
@login_required
def update_latlog(ciudad_id):
    ciudad = Ciudad.query.get(ciudad_id)
    ciudad_u = ciudad.nombre.replace (" ", "+")
    provincia = Provincia.query.get(ciudad.Provincia_idProvincia)
    provincia_u = provincia.nombre.replace (" ", "+")
    departamento = Departamento.query.get(provincia.Departamento_idDepartamento)
    departamento_u = departamento.nombre.replace (" ", "+")
    uri = "https://maps.googleapis.com/maps/api/geocode/json?address=" + ciudad_u + ",+" + provincia_u + ",+" + departamento_u+ ",+PE&key=AIzaSyAxpda7Dxacj_rUHrLHyaxasBUlyAGqHU4"

    try:
        uResponse = requests.get(uri)
    except requests.ConnectionError:
       return "Connection Error"
    Jresponse = uResponse.text
    data = json.loads(Jresponse)
    if data['status'] == 'OK':

        ciudad.latitud = data['results'][0]['geometry']['location']['lat']
        ciudad.longitud = data['results'][0]['geometry']['location']['lng']
        db.session.commit()
        flash("Success")

        return redirect(url_for("ciudades", prov_id = provincia.idProvincia))

    return Jresponse

@app.route("/lat_lon_prov/<int:prov_id>")
@login_required
def update_latlog_prov(prov_id):
    ciudades = Ciudad.query.filter_by(Provincia_idProvincia=prov_id)

    flag = True

    provincia = Provincia.query.get(prov_id)
    print(prov_id)
    provincia_u = provincia.nombre.replace (" ", "+")
    departamento = Departamento.query.get(provincia.Departamento_idDepartamento)
    departamento_u = departamento.nombre.replace (" ", "+")

    for item in ciudades:

        ciudad_u = item.nombre.replace (" ", "+")

        uri = "https://maps.googleapis.com/maps/api/geocode/json?address=" + ciudad_u + ",+" + provincia_u + ",+" + departamento_u+ ",+PE&key=AIzaSyAxpda7Dxacj_rUHrLHyaxasBUlyAGqHU4"

        try:
            uResponse = requests.get(uri)
        except requests.ConnectionError:
            pass
            flag = False
        Jresponse = uResponse.text
        data = json.loads(Jresponse)
        if data['status'] == 'OK':

            item.latitud = data['results'][0]['geometry']['location']['lat']
            item.longitud = data['results'][0]['geometry']['location']['lng']

            flash("Success")
        else:
            flag = False
    db.session.commit()
    print (flag)
    return redirect(url_for("ciudades", prov_id = prov_id))

@app.route("/clima/<int:ciudad_id>")
@login_required
def update_clima(ciudad_id):

    ciudad = Ciudad.query.get(ciudad_id)
    lat = ciudad.latitud
    lgn = ciudad.longitud

    if lat is not None and lgn is not None:

        uri = "http://api.openweathermap.org/data/2.5/forecast?lat=" + lat + "&lon=" + lgn + "&cnt=6&lang=es&units=metric&appid=0b8b9f1a08624187cb3b64dcf4079946"

        try:
            uResponse = requests.get(uri)
        except requests.ConnectionError:
           return "Connection Error"
        Jresponse = uResponse.text
        data = json.loads(Jresponse)
        climas = []

        if data['cod'] == "200":
            climas = data['list']
            for item in climas:
                if not Clima.query.filter_by(fecha=item['dt_txt']).filter_by(ciudad_idciudad=ciudad_id).first():
                    if not item['rain'] :
                        rain = "0"
                    else:
                        rain = item['rain']["3h"]
                    print item['rain']
                    clima = Clima(
                        temperatura_maxima = item['main']['temp_max'],
                        temperatura_minima = item['main']['temp_min'],
                        fecha = item['dt_txt'],
                        descripcion = item['weather'][0]['description'],
                        lluvia = rain,
                        humedad = item['main']['humidity'],
                        imagen = item['weather'][0]['icon'],
                        ciudad_idciudad = ciudad_id,
                    )
                    db.session.add(clima)



            db.session.commit()
            flash("Success")

            return redirect(url_for("ciudades", prov_id = ciudad.Provincia_idProvincia))

        return Jresponse
    else:
        return "debe tener latitud y longitud"


@app.route("/clima_prov/<int:prov_id>")
@login_required
def update_clima_prov(prov_id):
    ciudades = Ciudad.query.filter_by(Provincia_idProvincia=prov_id)

    flag = True

    provincia = Provincia.query.get(prov_id)
    print(prov_id)
    provincia_u = provincia.nombre.replace (" ", "+")
    departamento = Departamento.query.get(provincia.Departamento_idDepartamento)
    departamento_u = departamento.nombre.replace (" ", "+")

    for ciudad in ciudades:

        lat = ciudad.latitud
        lgn = ciudad.longitud

        if lat is not None and lgn is not None:

            uri = "http://api.openweathermap.org/data/2.5/forecast?lat=" + lat + "&lon=" + lgn + "&cnt=6&lang=es&units=metric&appid=0b8b9f1a08624187cb3b64dcf4079946"


            try:
                uResponse = requests.get(uri)
            except requests.ConnectionError:
                pass
                flag = False

            Jresponse = uResponse.text
            data = json.loads(Jresponse)
            if data['cod'] == '200':

                climas = data['list']
                for item in climas:
                    if not Clima.query.filter_by(fecha=item['dt_txt']).filter_by(ciudad_idciudad=ciudad.idCiudad).first():
                        if not 'rain' in item:
                            print ('wiji')
                            rain = "0"
                        else:
                            if not item['rain'] :
                                rain = "0"
                            else:
                                rain = item['rain']["3h"]

                        clima = Clima(
                            temperatura_maxima = item['main']['temp_max'],
                            temperatura_minima = item['main']['temp_min'],
                            fecha = item['dt_txt'],
                            descripcion = item['weather'][0]['description'],
                            lluvia = rain,
                            humedad = item['main']['humidity'],
                            imagen = item['weather'][0]['icon'],
                            ciudad_idciudad = ciudad.idCiudad,
                        )
                        db.session.add(clima)
                flash("Success")
            else:
                flag = False



    db.session.commit()
    print (flag)
    return redirect(url_for("ciudades", prov_id = prov_id))
