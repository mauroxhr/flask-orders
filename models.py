from collections import defaultdict
from peewee import *
from playhouse.postgres_ext import ArrayField
from playhouse.flask_utils import FlaskDB
from uuid  import uuid4
from datetime import datetime

db = FlaskDB()

class Usuario(db.Model):
    id = UUIDField(primary_key=True, default=uuid4)
    identificacion = CharField(max_length=20)
    nombre = CharField()
    direccion = CharField()
    telefono = IntegerField()

class Producto(db.Model):
    codigo = CharField(max_length=8)
    nombre = CharField(max_length=20)
    precio = IntegerField()

class Pedido(db.Model):
    orden_id = UUIDField(primary_key=True, default=uuid4)
    cliente = ForeignKeyField(Usuario, backref="usuario_pedido")
    producto = ForeignKeyField(Producto, backref="producto_pedido")
    cantidad = IntegerField()
    # productos = ArrayField(TextField)
