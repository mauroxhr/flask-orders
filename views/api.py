from flask import Blueprint, redirect, render_template, request, url_for, jsonify
from models import Producto


api = Blueprint("api_bp", __name__)

@api.route("/products/", methods=["GET", "POST"])
@api.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "GET":
        listadoProductos = Producto.select().dicts()
        listado = []
        for x in listadoProductos:
            listado.append(x)
        return jsonify(listado)

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



@api.route("/products/<id>", methods=["GET", "POST"])
def products_get(id: int):
    producto = Producto.get(Producto.id == id)
    # return f'PRODUCTO: {producto.codigo} {producto.nombre} {producto.precio}'
    return jsonify(producto.id, producto.nombre, producto.codigo, producto.precio)
