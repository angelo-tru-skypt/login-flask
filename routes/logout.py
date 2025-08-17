from flask import Blueprint, session, redirect

logout = Blueprint('logout', __name__)
@logout.route("/logout")
def cerrar_sesion():
    session.pop("email", None)
    return redirect("/login")

