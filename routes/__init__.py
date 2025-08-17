from flask import Blueprint, session, redirect
principal = Blueprint('routes', __name__)

@principal.route("/")
def home():
    if "email" in session:
        return f"Bienvenido {session['email']} <a href='/logout'>Cerrar sesión</a>"
    else:
        return redirect("/login")
