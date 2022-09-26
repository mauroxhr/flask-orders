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


@user.route("/test")
@login_required
def test():
    return render_template('dashboard/base.html')

@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_bp.index'))
