from project import app, db
from .model import Departamento, Provincia, Ciudad, Manager, Mercado, bcrypt
from flask import  render_template, flash, request, url_for, redirect

import requests
import simplejson
import json

@app.route("/lat_lon/<int:ciudad_id>")
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
