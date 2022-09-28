from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import logout_user, login_required
from models import Producto, Pedido


user = Blueprint("user_bp", __name__)

@user.route("/")
@login_required
def index():
    return render_template('dashboard/index.html')

@user.route("/profile")
@login_required
def profile():
    return render_template('dashboard/profile.html')

@user.route("/crearproducto", methods=["GET", "POST"])
@login_required
def crearProducto():
    if request.method == "GET":
     return render_template('dashboard/crearProducto.html')

    if request.method == "POST":
        nombre = request.form.get('nombre')
        codigo = request.form.get('codigo')
        precio = request.form.get('precio')

        if nombre and codigo and precio:
            try:
                precio = int(precio)
                if Producto.select().where(Producto.codigo == codigo):
                    return "Ya existe el producto"
                nuevoProducto = Producto.create(nombre=nombre, codigo=codigo, precio=precio)
                nuevoProducto.save()
            except Exception as e:
                return f"No se pudo crear el producto {e}"
    return render_template('dashboard/crearProducto.html')


@user.route("/verproducto")
@login_required
def verProducto():
    listadoProductos = Producto.select().dicts()
    return render_template('dashboard/verProducto.html', productos=listadoProductos)

@user.route("/crearpedido")
@login_required
def crearPedido():
    listadoProductos = Producto.select().dicts()
    return render_template('dashboard/crearPedido.html', productos=listadoProductos)


@user.route("/verpedidos")
@login_required
def verPedido():
    listadoPedidos = Pedido.select()
    return render_template('dashboard/verPedido.html', pedidos=listadoPedidos)

@user.route("/faq")
@login_required
def faq():
    return render_template('dashboard/faq.html')

@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_bp.index'))
