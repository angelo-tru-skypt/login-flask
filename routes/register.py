from flask import Blueprint, session, redirect, request, render_template
from werkzeug.security import generate_password_hash
from models.db import db
from models.user import Users

register = Blueprint('register', __name__)

@register.route("/register", methods=["GET", "POST"])
def registrar():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hash_password = generate_password_hash(password)
        user = Users(username=username, email=email, password=hash_password)
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")
