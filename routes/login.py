from flask import Blueprint, request, render_template, redirect, session
from werkzeug.security import check_password_hash
from models.db import db
from models.user import Users

login = Blueprint('login', __name__)

@login.route("/login", methods=["GET", "POST"])
def inicio():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = Users.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['email'] = user.email
            return redirect("/")
        else:
            return "Usuario o contraseña incorrectos"

    return render_template("login.html")
