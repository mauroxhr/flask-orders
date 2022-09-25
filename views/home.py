from flask import Blueprint, render_template, request
from models import Producto


home = Blueprint("home_bp", __name__)

@home.route("/")
def index():
    return render_template('pages/index.html')

@home.route("/about")
def about():
    return "<h1>About</h1>"

@home.route("/login")
def login():
    return render_template('pages/login.html')

@home.route("/register")
def register():
    return render_template('pages/register.html')

@home.route("/contact")
def contact():
    return "<h1>Contact </h1>"

@home.route("/products/", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        listadoProductos = Producto.select().dicts()
        return render_template('crearProducto.html', listadoProductos=listadoProductos)
    elif request.method == "POST":
        codigo = request.form.get("codigo")
        nombre = request.form.get("nombre")
        precio = request.form.get("precio")

        if codigo and nombre and precio:
            if Producto.select().where(Producto.codigo == codigo):
                return 'Ya existe'
            else:
                Producto.create(codigo=codigo, nombre=nombre, precio=precio)
        return f'producto creado exitosamente {codigo} {nombre} {precio}'



@home.route("/products/<id>", methods=["GET", "POST"])
def products_get(id: int):
    listadoProductos = Producto.select().where(Producto.id == id)
    return render_template('base.html', listadoProductos=listadoProductos)

@home.route("/products/update", methods=["GET", "POST"])
def update():
    listadoProductos = Producto.select().dicts()
    return render_template('base.html', listadoProductos=listadoProductos)
