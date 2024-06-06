from flask import Flask, request, jsonify, send_file, session, redirect, url_for, render_template # type: ignore
from flask_cors import CORS # type: ignore
from datetime import datetime, timedelta
from flask_session import Session # type: ignore
from Utilidades.manage_credential import credentialsUser
from Utilidades.manejo_db import db_manage
from Utilidades.autenticacion import autenticacion

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Renderizador

@app.route('/')
def render_login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST'])
def handle_login():
    if request.method == "POST":
        try:
            data = request.get_json()
            correo = data.get('correo')
            contraseña = data.get('contraseña')

            # obtener el usuario de la base de datos:
            user = db_manage.validate(correo, contraseña)
            if user:
                user_id = db_manage.get_user_id(correo)

                if user_id:
                    session['user_id'] = user_id
                    session['correo'] = correo

                    return jsonify({'user_id': user_id, 'correo': correo, 'redirect_url': url_for('home')})
            return jsonify({'error': 'Invalid credentials'}), 401
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Internal Server Error'}), 500
    return jsonify({'error': 'Bad Request'}), 400

@app.route('/app/registro', methods=['POST'])
def registro():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        nombre = data.get('nombre')
        apellido = data.get('apellido')
        correo = data.get('correo')
        contraseña = data.get('contrasena')
        try:
            token_generado = autenticacion.generar_token()
            time_now = datetime.now()
            tiempo_token_expirado = timedelta(minutes=3)
            tiempo_creacion_token = time_now - tiempo_token_expirado
            
            if autenticacion.enviar_token:
                if tiempo_creacion_token < tiempo_token_expirado:
                    validarToken(token_generado)
                else:
                    print("El tiempo del token ha expirado")
            else:
                print("No se logró enviar el token")
        except Exception as e:
            print(f"Algo salió mal... {e}")
            return jsonify({'message': 'Error interno del servidor.'}), 500

@app.route('/app/validate_token', methods=['POST'])
def validarToken(token_generado, nombre, apellido, correo, contraseña):
    if request.method == 'POST':
        data = request.get_json()
        token_ingreso = data.get('token')

        try:
            if token_ingreso == token_generado:
                if credentialsUser.genCredentials(nombre, apellido, correo, contraseña):
                    print("Usuario validado y agregado")
                return True
            else:
                return False
        except Exception as e:
            print(f"Hubo un error al validar el token de autenticacion: {e}")

if __name__ == '__main__':
    app.run()
