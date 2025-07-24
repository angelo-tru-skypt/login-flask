from flask import Flask, request, redirect, render_template, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from db import connection

class UserManager:
    def __init__(self, db_connection):
        self.connection = db_connection

    def create_user(self, username, email, password):
        hashed_password = generate_password_hash(password)
        cursor = self.connection.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        self.connection.commit()

    def get_user_by_email(self, email):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        return cursor.fetchone()

    def get_all_users(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, username, email, password FROM users")
        return cursor.fetchall()

    def delete_user(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        self.connection.commit()

    def update_user(self, user_id, username, email):
        cursor = self.connection.cursor()
        cursor.execute(
            "UPDATE users SET username = %s, email = %s WHERE id = %s",
            (username, email, user_id)
        )
        self.connection.commit()

    def get_user_by_id(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT id, username, email FROM users WHERE id = %s", (user_id,))
        return cursor.fetchone()

user_manager = UserManager(connection)
from flask import Flask, request, redirect, render_template, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from db import connection

app = Flask(__name__)
app.secret_key = "mi_clave_secreta"

@app.route('/')
def home():
    if 'email' in session:
        return f"Bienvenido {session['email']} <a href='/logout'>Cerrar sesión</a>"
    else:
        return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (user, email, hashed_password))
        connection.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user and check_password_hash(user[3], password):
            session['email'] = user[2]
            return redirect('/admin')
        else:
            return "Credenciales incorrectas"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')

@app.route('/admin')
def admin():
    if 'email' not in session:
        return redirect('/login')
    cursor = connection.cursor()
    cursor.execute("SELECT id, username, email, password FROM users")
    users = cursor.fetchall()
    return render_template('crud.html', users=users)

@app.route('/admin/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'email' not in session:
        return redirect('/login')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    connection.commit()
    return redirect('/admin')

@app.route('/admin/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if 'email' not in session:
        return redirect('/login')

    cursor = connection.cursor()

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        cursor.execute("UPDATE users SET username = %s, email = %s WHERE id = %s", (username, email, user_id))
        connection.commit()
        return redirect('/admin')
    
    cursor.execute("SELECT id, username, email FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    if not user:
        return "Usuario no encontrado"

    return f"""
        <h2>Editar Usuario</h2>
        <form method="post">
            <label>Username:</label>
            <input type="text" name="username" value="{user[1]}" required><br>
            <label>Email:</label>
            <input type="email" name="email" value="{user[2]}" required><br>
            <button type="submit">Guardar</button>
        </form>
        <a href="/admin">Volver</a>
    """

@app.route('/admin/add', methods=['POST'])
def add_user():
    if 'email' not in session:
        return redirect('/login')

    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    hashed_password = generate_password_hash(password)

    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, hashed_password))
    connection.commit()

    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=3000)
