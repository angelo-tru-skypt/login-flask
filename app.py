from flask import Flask, redirect, request, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import connection

app = Flask(__name__)
app.secret_key = "mi_clave_secreta"

@app.route("/")
def index():
    if "email" in session:
        return f'Bienvenido {session["email"]} a mi pagina en flask <a href="/logout">Cerrar sesión</a>'
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        hash_password = generate_password_hash(password)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users(username, email, password) VALUES(%s, %s, %s)", (username, email, hash_password))
        connection.commit()
        return redirect("/login")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user[3], password):
            session['email'] = email
            return redirect("/")
        return render_template("login.html", error="Credenciales incorrectos")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)

