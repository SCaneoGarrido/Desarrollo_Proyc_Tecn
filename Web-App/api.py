from flask import Flask, request, jsonify, send_file, session, redirect, url_for, render_template # type: ignore
from flask_cors import CORS # type: ignore
from datetime import datetime, timedelta
from Utilidades.manage_credential import credentialsUser
from Utilidades.manejo_db import db_manage
from Utilidades.autenticacion import autenticacion

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# =========== INICIO RENDERIZADOR ====================== #
@app.route('/')
def render_login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')
# =========== TERMINO DE RENDERIZADOR ====================== #
app.route('/datos', methods=['GET'])
def get_response():
    pass


if __name__ == '__main__':
    app.run(debug=True)
