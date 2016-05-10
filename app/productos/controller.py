from flask import Blueprint, render_template

productos = Blueprint('productos', __name__,
                        template_folder='templates')

@productos.route('/<producto>/historia')
def historia(producto):
    return render_template("historia.html" , producto = producto)

@productos.route('/<producto>/historia')
def vnutricional(producto):
    return render_template("historia.html" , producto = producto)

@productos.route('/<producto>/historia')
def precio(producto):
    return render_template("historia.html" , producto = producto)

@productos.route('/<producto>/historia')
def cosecha(producto):
    return render_template("historia.html" , producto = producto)
