from flask import Blueprint, json, redirect, render_template, request, url_for, jsonify
from models import Producto, Pedido
import uuid


api = Blueprint("api_bp", __name__)

@api.route("/products/", methods=["GET", "POST"])
@api.route("/products", methods=["GET", "POST"])
def get_all_products():
    if request.method == "GET":
        listado = []
        try:
            listadoProductos = Producto.select().dicts()


            for x in listadoProductos:
                listado.append(x)

            if listado:
                return jsonify(listado)
            else:
                return jsonify({"error": "no hay productos en el sistema"})

        except Exception as e:
            return jsonify({"ha ocurrido un error"})

    elif request.method == "POST":
        data = request.get_json()
        print(data)

        if data["nombre"] and data["codigo"] and data["precio"]:
            if Producto.select().where(Producto.codigo == data["codigo"]):
                return f'Ya existe el producto {data}'
            else:
                Producto.create(codigo=data["codigo"], nombre=data["nombre"], precio=data["precio"])
        else:
            return "No se puede crear el producto"
        return f'producto creado exitosamente {data}'



@api.route("/products/<int:id>", methods=["GET", "POST"])
def get_product(id: int):
    try:
        producto = Producto.get(Producto.id == id)
    except Exception as e:
        return jsonify({"error": "El producto no existe"}), 404
    # return f'PRODUCTO: {producto.codigo} {producto.nombre} {producto.precio}'
    return jsonify(producto.id, producto.nombre, producto.codigo, producto.precio)


@api.route("/orders/", methods=["GET", "POST"])
@api.route("/orders", methods=["GET", "POST"])
def get_all_orders():
    if request.method == "GET":
        listado = []
        try:
            listadoPedidos = Pedido.select().dicts()


            for x in listadoPedidos:
                listado.append(x)

            if listado:
                return jsonify(listado)
            else:
                return jsonify({"error": "no hay pedidos en el sistema"})
        except Exception as e:
            return jsonify({"ha ocurrido un error"})

    elif request.method == "POST":
        data = request.get_json()
        if data["cliente_id"] and data["producto_id"] and data["cantidad"]:
                Pedido.create(cliente_id=data["cliente_id"], producto_id=data["producto_id"], cantidad=data["cantidad"])
        else:
            return "No se puede crear el pedido"
        return f'pedido creado exitosamente {data}'

@api.route("/orders/<id>", methods=["GET", "POST"])
def get_order(id):
    listado = []
    try:
        pedido = Pedido.select().where(Pedido.id == id).dicts()
        for x in pedido:
            listado.append(x)

        if listado:
            return jsonify(listado)
        else:
            return jsonify({"error": "no existe el pedido"}), 404
    except Exception as e:
        return jsonify({"ocurrió un error"})
