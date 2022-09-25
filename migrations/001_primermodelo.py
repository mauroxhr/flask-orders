"""Peewee migrations -- 001_primermodelo.py.

Some examples (model - class or model name)::

    > Model = migrator.orm['model_name']            # Return model in current state by name

    > migrator.sql(sql)                             # Run custom SQL
    > migrator.python(func, *args, **kwargs)        # Run python code
    > migrator.create_model(Model)                  # Create a model (could be used as decorator)
    > migrator.remove_model(model, cascade=True)    # Remove a model
    > migrator.add_fields(model, **fields)          # Add fields to a model
    > migrator.change_fields(model, **fields)       # Change fields
    > migrator.remove_fields(model, *field_names, cascade=True)
    > migrator.rename_field(model, old_field_name, new_field_name)
    > migrator.rename_table(model, new_table_name)
    > migrator.add_index(model, *col_names, unique=False)
    > migrator.drop_index(model, *col_names)
    > migrator.add_not_null(model, *field_names)
    > migrator.drop_not_null(model, *field_names)
    > migrator.add_default(model, field_name, default)

"""

import datetime as dt
import peewee as pw
from peewee_migrate import Migrator
from decimal import ROUND_HALF_EVEN

try:
    import playhouse.postgres_ext as pw_pext
except ImportError:
    pass

SQL = pw.SQL


def migrate(migrator: Migrator, database, fake=False, **kwargs):
    """Write your migrations here."""

    @migrator.create_model
    class Usuario(pw.Model):
        id = pw.UUIDField(primary_key=True)
        identificacion = pw.CharField(max_length=20)
        nombre = pw.CharField(max_length=255)
        direccion = pw.CharField(max_length=255)
        telefono = pw.IntegerField()

        class Meta:
            table_name = "usuario"

    @migrator.create_model
    class Producto(pw.Model):
        id = pw.AutoField()
        codigo = pw.CharField(max_length=8)
        nombre = pw.CharField(max_length=20)
        precio = pw.IntegerField()

        class Meta:
            table_name = "producto"

    @migrator.create_model
    class Pedido(pw.Model):
        orden_id = pw.UUIDField(primary_key=True)
        nombre = pw.CharField(max_length=20)
        precio = pw.IntegerField()
        cliente = pw.ForeignKeyField(backref='usuario_pedido', column_name='cliente_id', field='id', model=migrator.orm['usuario'])
        producto = pw.ForeignKeyField(backref='producto_pedido', column_name='producto_id', field='id', model=migrator.orm['producto'])
        cantidad = pw.IntegerField()

        class Meta:
            table_name = "pedido"



def rollback(migrator: Migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    migrator.remove_model('pedido')

    migrator.remove_model('producto')

    migrator.remove_model('usuario')
