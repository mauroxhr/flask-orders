from datetime import timedelta
from flask import Blueprint, redirect, render_template, request, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import Producto, Usuario
from bcrypt import gensalt
from bcrypt import hashpw as encriptar_password
from bcrypt import checkpw as confirmar_password


home = Blueprint("home_bp", __name__)

@home.route("/")
def index():
    return render_template('pages/index.html')

@home.route("/about")
def about():
    return "<h1>About</h1>"

@home.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if current_user.is_active:
            return redirect(url_for(('user_bp.index')))
        else:
            return render_template('pages/login.html')

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')

        if username and password:
            try:
                usuario = Usuario.get(correo=username)
                print(usuario)
            except Exception as e:
                return f"Error, no se pudo obtener el usuario {e}"
            pass_actual = usuario.contraseña
            hacen_match = confirmar_password(password.encode("utf-8"), pass_actual.encode("utf-8"))

            if hacen_match:
                if remember == "on":
                    delta = timedelta(7, 3600)
                    login_user(usuario, remember=True, duration=delta)
                else:
                    login_user(usuario, remember=False, duration=False)

                return redirect(url_for('user_bp.index'))

        return "Error, datos incompletos"


@home.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        if current_user.is_active:
            return redirect(url_for(('user_bp.index')))
        else:
            return render_template('pages/register.html')

    if request.method == "POST":
        if 'btnRegister' in request.form:
            name = request.form.get('name')
            correo = request.form.get('email')
            identificacion = request.form.get('identificacion')
            contraseña = request.form.get('password')

            if name and correo and identificacion and contraseña:
                cifrar_password = encriptar_password(contraseña.encode("utf-8"), gensalt())

                try:
                    if Usuario.select().where(Usuario.identificacion == identificacion):
                        return "El usuario ya existe"
                    nuevoUsuario = Usuario.create(nombre=name, correo=correo, identificacion=identificacion[:10], contraseña=cifrar_password)
                    login_user(nuevoUsuario)
                    return redirect(url_for('user_bp.index'))
                except Exception as e:
                    return f"No se puede crear el usuario {e}"
            else:
                return f"Información incompleta"

            # return f"{correo} {name} {identificacion}"


@home.route("/contact")
def contact():
    return "<h1>Contact </h1>"

