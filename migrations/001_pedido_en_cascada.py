"""Peewee migrations -- 001_pedido_en_cascada.py.

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
        identificacion = pw.CharField(max_length=20, unique=True)
        nombre = pw.CharField(max_length=255)
        correo = pw.CharField(max_length=255, unique=True)
        contraseña = pw.CharField(max_length=255)
        direccion = pw.CharField(max_length=255, null=True)
        telefono = pw.IntegerField(null=True)
        rol = pw.CharField(constraints=[SQL("DEFAULT 'USUARIO'")], default='USUARIO', max_length=255)

        class Meta:
            table_name = "usuario"

    @migrator.create_model
    class Limitaciones(pw.Model):
        id = pw.AutoField()
        usuario = pw.ForeignKeyField(backref='usuario_limitaciones', column_name='usuario_id', field='id', model=migrator.orm['usuario'])
        productos = pw.IntegerField()
        pedidos = pw.IntegerField()

        class Meta:
            table_name = "limitaciones"

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
        id = pw.IntegerField(primary_key=True)
        orden_id = pw.UUIDField()
        cliente = pw.ForeignKeyField(backref='usuario_pedido', column_name='cliente_id', field='id', model=migrator.orm['usuario'])
        producto = pw.ForeignKeyField(backref='producto_pedido', column_name='producto_id', field='id', model=migrator.orm['producto'], on_delete='cascade')
        cantidad = pw.IntegerField()

        class Meta:
            table_name = "pedido"



def rollback(migrator: Migrator, database, fake=False, **kwargs):
    """Write your rollback migrations here."""

    migrator.remove_model('pedido')

    migrator.remove_model('producto')

    migrator.remove_model('limitaciones')

    migrator.remove_model('usuario')
