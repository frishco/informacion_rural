from app import app, mysql, api, db

class Departamento(db.Model):

    __tablename__ = "departamento"

    idDepartamento = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    ubicacion = db.Column(db.String, nullable=False)
    superficie = db.Column(db.String, nullable=False)

    def __init__(self, nombre, ubicacion, superficie):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.superficie = superficie

    def __repr__(self):
        return '<Departamento %r>' % (self.nombre)

class Provincia(db.Model):
    __tablename__ = "provincia"

    idProvincia = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    Departamento_idDepartamento = db.Column(db.Integer, db.ForeignKey('departamento.idDepartamento'))

    def __init__(self, nombre, ubicacion, superficie):
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.superficie = superficie

    def __repr__(self):
        return '<Departamento %r>' % (self.nombre)
