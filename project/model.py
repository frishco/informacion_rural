from project import db

class Departamento(db.Model):

    __tablename__ = "departamento"

    idDepartamento = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    ubicacion = db.Column(db.String, nullable=False)
    superficie = db.Column(db.String, nullable=False)
    pronvincias = db.relationship('Provincia', backref='departamento', lazy='dynamic')

    def __init__(self, nombre, ubicacion, superficie):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.superficie = superficie

    def __repr__(self):
        return  (self.nombre)

class Provincia(db.Model):
    __tablename__ = "provincia"

    idProvincia = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    Departamento_idDepartamento = db.Column(db.Integer, db.ForeignKey('departamento.idDepartamento'))

    def __repr__(self):
        return (self.nombre)

class Ciudad(db.Model):
    __tablename__ = "ciudad"

    idCiudad = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    latitud = db.Column(db.String, nullable=False)
    longitud = db.Column(db.String, nullable=False)
    Provincia_idProvincia = db.Column(db.Integer, db.ForeignKey('provincia.idProvincia'))

    def __init__(self, nombre, latitud, longitud, Provincia_idProvincia):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.Provincia_idProvincia = Provincia_idProvincia

    def __repr__(self):
        return '<Distrito %r>' % (self.nombre)
