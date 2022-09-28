from collections import defaultdict
from peewee import *
from playhouse.postgres_ext import ArrayField
from playhouse.flask_utils import FlaskDB
from uuid  import uuid4
from datetime import datetime
from flask_login import UserMixin
from enum import auto
from strenum import StrEnum

db = FlaskDB()

class Usuario(db.Model, UserMixin):
    class ROLES(StrEnum):
        ADMINISTRADOR = auto()
        USUARIO = auto()

    id = UUIDField(primary_key=True, default=uuid4)
    identificacion = CharField(max_length=20, unique=True)
    nombre = CharField()
    correo = CharField(unique=True)
    contraseña = CharField()
    direccion = CharField(null=True)
    telefono = IntegerField(null=True)
    rol = CharField(
        default=ROLES.USUARIO.value,
        choices=[(r.name, r.value) for r in ROLES]
    )

class Producto(db.Model):
    codigo = CharField(max_length=8)
    nombre = CharField(max_length=20)
    precio = IntegerField()

class Pedido(db.Model):
    id = IntegerField(primary_key=True)
    orden_id = UUIDField(default=uuid4)
    cliente = ForeignKeyField(Usuario, backref="usuario_pedido")
    producto = ForeignKeyField(Producto, backref="producto_pedido", on_delete='cascade')
    cantidad = IntegerField()
    # productos = ArrayField(TextField)

class Limitaciones(db.Model):
    usuario = ForeignKeyField(Usuario, backref="usuario_limitaciones")
    productos = IntegerField()
    pedidos = IntegerField()
