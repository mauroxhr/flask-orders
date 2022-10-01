from datetime import timedelta
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_user, current_user
from models import Usuario
from bcrypt import gensalt
from bcrypt import hashpw as encriptar_password
from bcrypt import checkpw as confirmar_password


home = Blueprint("home_bp", __name__)

@home.route("/")
def index():
    return render_template('pages/index.html')

@home.route("/terms-condition")
def terms_and_condition():
    return "<h1>Términos y condiciones</h1><p>Los datos registrados no serán compartidos con terceros</p>"

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
            except Exception as e:
                flash("No se pudo iniciar sesión", "alert-danger bg-danger")
                return render_template('pages/login.html')
            pass_actual = usuario.contraseña
            hacen_match = confirmar_password(password.encode("utf-8"), pass_actual.encode("utf-8"))

            if hacen_match:
                if remember == "on":
                    delta = timedelta(7, 3600)
                    login_user(usuario, remember=True, duration=delta)
                else:
                    login_user(usuario, remember=False, duration=False)

                flash("Has iniciado sesión correctamente", "alert-success bg-success")
                return redirect(url_for('user_bp.index'))

        flash("No se pudo iniciar sesión", "alert-danger bg-danger")
        return render_template('pages/login.html')


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
                    if Usuario.select().where(Usuario.identificacion == identificacion and Usuario.correo == correo):
                        flash("El usuario ya existe", "alert-danger bg-danger")
                        return render_template('pages/register.html')

                    nuevoUsuario = Usuario.create(nombre=name, correo=correo, identificacion=identificacion[:10], contraseña=cifrar_password)
                    login_user(nuevoUsuario)
                    flash("Cuenta creada exitosamente", "alert-success bg-success")
                    return redirect(url_for('user_bp.index'))
                except Exception as e:
                    flash("No se pudo crear el usuario", "alert-danger bg-danger")
                    return render_template('pages/register.html')
            else:
                flash("No se pudo crear el usuario", "alert-danger bg-danger")
                return render_template('pages/register.html')
