from flask import Flask
from routes import principal
from routes.login import login
from routes.register import register
from routes.logout import logout
from models.db import db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Amancebo0818@localhost:3306/login'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

app.register_blueprint(principal)
app.register_blueprint(login)
app.register_blueprint(register)
app.register_blueprint(logout)
app.secret_key= "mi_clave_secreta"

if __name__ == '__main__':
    app.run(debug=True)
