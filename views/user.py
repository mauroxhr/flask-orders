from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import logout_user, login_required
from models import Producto


user = Blueprint("user_bp", __name__)

@user.route("/")
@login_required
def index():
    return render_template('dashboard/index.html')

@user.route("/profile")
@login_required
def profile():
    return render_template('dashboard/profile.html')

@user.route("/crearproducto")
@login_required
def crearProducto():
    return render_template('dashboard/crearProducto.html')


@user.route("/verproducto")
@login_required
def verProducto():
    listadoProductos = Producto.select().dicts()
    return render_template('dashboard/verProducto.html', productos=listadoProductos)

@user.route("/crearpedido")
@login_required
def crearPedido():
    return render_template('dashboard/crearPedido.html')


@user.route("/verpedido")
@login_required
def verPedido():
    return render_template('dashboard/crearProducto.html')

@user.route("/faq")
@login_required
def faq():
    return render_template('dashboard/faq.html')

@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_bp.index'))
