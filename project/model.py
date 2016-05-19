from project import db, bcrypt

class Manager(db.Model):
    __tablename__ = "manager"

    idManager = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    apellido = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

    def __init__(self, nombre, apellido, email, password):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.role = "encuestador"

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.idManager)

    def __repr__(self):
        return  (self.nombre)

class Producto(db.Model):
    __tablename__ = "producto"

    idProducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    informacion = db.Column(db.String, nullable=False)
    foto = db.Column(db.String, nullable=False)

    def __repr__(self):
        return  (self.nombre)

class Mercado(db.Model):
    __tablename__ = "mercado"

    idMercado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    capacidad = db.Column(db.String, nullable=False)
    ciudad_idciudad = db.Column(db.Integer, db.ForeignKey('ciudad.idCiudad'))

    def __repr__(self):
        return  (self.nombre)

class Variedad(db.Model):
    __tablename__ = "variedad"

    idVariedad = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    caracteristicas = db.Column(db.String, nullable=False)
    Producto_idProducto = db.Column(db.Integer, db.ForeignKey('producto.idProducto'))

    def __repr__(self):
        return  (self.nombre)

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
