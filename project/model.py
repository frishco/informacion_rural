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

    def is_admin(self):

        if(self.role is not "encuestador"):
            return True
        else:
            return False


    def __repr__(self):
        return  (self.nombre)

class Producto(db.Model):
    __tablename__ = "producto"

    idProducto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    informacion = db.Column(db.String, nullable=False)
    imagen = db.Column(db.String, nullable=False)

    def __repr__(self):
        return  (self.nombre)

class Precio(db.Model):
    __tablename__ = "precio"

    idPrecio =  db.Column(db.Integer, primary_key=True)
    precio_promedio = db.Column(db.String, nullable=False)
    precio_max = db.Column(db.String, nullable=False)
    precio_min = db.Column(db.String, nullable=False)
    fecha = db.Column(db.String, nullable=False)
    Mercado_idMercado = db.Column(db.Integer, db.ForeignKey('mercado.idMercado'))
    variedad_idvariedad = db.Column(db.Integer, db.ForeignKey('variedad.idvariedad'))

    def __init__(self, precio_promedio, precio_max, precio_min, fecha, Mercado_idMercado, variedad_idvariedad):
        self.precio_promedio = precio_promedio
        self.precio_max = precio_max
        self.precio_min = precio_min
        self.fecha = fecha
        self.Mercado_idMercado = Mercado_idMercado
        self.variedad_idvariedad = variedad_idvariedad

    def __repr__(self):
        return  (self.fecha)


class Mercado(db.Model):
    __tablename__ = "mercado"

    idMercado = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    capacidad = db.Column(db.String, nullable=False)
    ciudad_idciudad = db.Column(db.Integer, db.ForeignKey('ciudad.idCiudad'))

    def __init__(self, nombre, capacidad, ciudad_idciudad):
        self.nombre = nombre
        self.capacidad = capacidad
        self.ciudad_idciudad = ciudad_idciudad

    def __repr__(self):
        return  (self.nombre)

class Noticia(db.Model):
    __tablename__ = "noticia"

    idNoticia = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String, nullable=False)
    cuerpo = db.Column(db.String, nullable=False)
    fecha = db.Column(db.String, nullable=False)
    fuente = db.Column(db.String, nullable=False)
    imagen = db.Column(db.String, nullable=False)

    def __init__(self, titulo, cuerpo, fecha, fuente, imagen):
        self.titulo = titulo
        self.cuerpo = cuerpo
        self.fecha = fecha
        self.fuente = fuente
        self.imagen = imagen

    def __repr__(self):
        return  (self.titulo)


class Variedad(db.Model):
    __tablename__ = "variedad"

    idvariedad = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    caracteristicas = db.Column(db.String, nullable=False)
    Producto_idProducto = db.Column(db.Integer, db.ForeignKey('producto.idProducto'))

    def __init__(self, nombre, caracteristicas, Producto_idProducto):
        self.nombre = nombre
        self.caracteristicas = caracteristicas
        self.Producto_idProducto = Producto_idProducto

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
    ciudades = db.relationship('Ciudad', backref='provincia', lazy='dynamic')

    def __repr__(self):
        return (self.nombre)

class Ciudad(db.Model):
    __tablename__ = "ciudad"

    idCiudad = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String, nullable=False)
    latitud = db.Column(db.String, nullable=False)
    longitud = db.Column(db.String, nullable=False)
    Provincia_idProvincia = db.Column(db.Integer, db.ForeignKey('provincia.idProvincia'))
    mercados = db.relationship('Mercado', backref='ciudad', lazy='dynamic')

    def __init__(self, nombre, latitud, longitud, Provincia_idProvincia):
        self.nombre = nombre
        self.latitud = latitud
        self.longitud = longitud
        self.Provincia_idProvincia = Provincia_idProvincia

    def __repr__(self):
        return '<Distrito %r>' % (self.nombre)

class Clima(db.Model):
    __tablename__ = "clima"

    idclima = db.Column(db.Integer, primary_key=True)
    temperatura_maxima = db.Column(db.String, nullable=False)
    temperatura_minima = db.Column(db.String, nullable=False)
    fecha = db.Column(db.String, nullable=False)
    descripcion = db.Column(db.String, nullable=False)
    lluvia = db.Column(db.String, nullable=False)
    humedad = db.Column(db.String, nullable=False)
    imagen = db.Column(db.String, nullable=False)
    ciudad_idciudad = db.Column(db.Integer, db.ForeignKey('ciudad.idCiudad'))


    def __init__(self, temperatura_maxima, temperatura_minima, fecha, descripcion, lluvia, humedad, imagen, ciudad_idciudad):
        self.temperatura_maxima = temperatura_maxima
        self.temperatura_minima = temperatura_minima
        self.fecha = fecha
        self.descripcion = descripcion
        self.lluvia = lluvia
        self.humedad = humedad
        self.imagen = imagen
        self.ciudad_idciudad = ciudad_idciudad

    def __repr__(self):
        return '<Distrito %r>' % (self.nombre)
