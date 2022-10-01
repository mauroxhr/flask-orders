from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user, logout_user, login_required
from models import Producto, Pedido, Usuario
import uuid


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
                    flash("Ya existe el producto", "alert-danger bg-danger")
                    return render_template('dashboard/crearProducto.html')
                nuevoProducto = Producto.create(nombre=nombre, codigo=codigo, precio=precio)
                nuevoProducto.save()
                flash("Producto creado exitosamente", "alert-success bg-success")
            except Exception as e:
                flash("Ya existe el producto", "alert-danger bg-danger")
        else:
            flash("Rellena todos los campos", "alert-danger bg-danger")

    return render_template('dashboard/crearProducto.html')


@user.route("/verproducto")
@login_required
def verProducto():
    listadoProductos = Producto.select().dicts()
    if current_user.rol == "ADMINISTRADOR":
        form = request.args
        if form:
            if "borrarproducto" in form:
                producto = Producto.get(Producto.id == form["borrarproducto"])
                producto.delete_instance()
                pedido = Pedido.delete().where(Pedido.producto_id == form["borrarproducto"])
                pedido.execute()
    return render_template('dashboard/verProducto.html', productos=listadoProductos)

@user.route("/crearpedido", methods=["GET", "POST"])
@login_required
def crearPedido():
    listadoProductos = Producto.select().dicts()
    if request.method == "GET":
        form = request.args
        if form:
            cliente = form["cliente"]
            producto = form["producto"]
            cantidad = form["cantidad"]
            if cliente and producto != "Elegir producto" and cantidad:
                try:
                    cliente = uuid.UUID(cliente)
                    query = Pedido.select().where(Pedido.cliente_id == cliente)
                    # Si existe el producto, aumentar la cantidad o restar la cantidad y es diferente del cliente id
                    idProducto = ""
                    idCliente = ""
                    idOrden = ""
                    for i in query:
                        if i.producto.id == int(producto):
                            idOrden = i.id
                            idCliente = i.cliente_id
                            idProducto = i.producto_id

                    if idCliente == cliente and idProducto == int(producto):
                            # cantidadMinima = [0].cantidad
                            queryQuantity = Pedido.select().where(Pedido.id == idOrden)
                            productoCantidad = queryQuantity[0].cantidad
                            cantidadMinima = productoCantidad + int(cantidad)
                            if cantidadMinima > 0:
                                pedidoUpdate = Pedido.update(cantidad=cantidadMinima).where(Pedido.id == idOrden)
                                pedidoUpdate.execute()
                                flash("Pedido actualizado exitosamente.", "alert-success bg-success")
                                flash(f"Cantidad anterior: {productoCantidad}, ahora la nueva cantidad es {cantidadMinima} ", "alert-success bg-success")
                                return redirect(request.path,code=302)
                    else:
                        nuevoPedido = Pedido.create(cliente_id=cliente, producto_id=producto, cantidad=cantidad)
                        nuevoPedido.save()
                        flash("Pedido creado exitosamente", "alert-success bg-success")
                        return redirect(request.path,code=302)
                except Exception as e:
                    flash("No se pudo crear el pedido", "alert-danger bg-danger")
                    return render_template('dashboard/crearPedido.html', productos=listadoProductos)
            else:
                flash("Rellena todos los campos", "alert-danger bg-danger")
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
    flash("Has cerrado sesión exitosamente", "alert-success bg-success")
    return redirect(url_for('home_bp.index'))



admin = Blueprint("admin_bp", __name__)


@admin.route("/verusuarios")
@login_required
def verUsuarios():
    if current_user.rol == "ADMINISTRADOR": # to do a decorator
        listadoUsuarios = Usuario.select().dicts()
        try:
            form = request.args
            if form:
                if "usuario" in form:
                    usuario = Usuario.get(Usuario.id == form["usuario"])
                    usuario.delete_instance()
                if "quitaradmin" in form:
                    usuario = Usuario.update(rol="USUARIO").where(Usuario.id == form["quitaradmin"])
                    usuario.execute()
                if "haceradmin" in form:
                    usuario = Usuario.update(rol="ADMINISTRADOR").where(Usuario.id == form["haceradmin"])
                    usuario.execute()
        except Exception as e:
            raise e
        return render_template('dashboard/admin/verUsuarios.html', usuarios=listadoUsuarios)
    else:
        return render_template('dashboard/index.html')
