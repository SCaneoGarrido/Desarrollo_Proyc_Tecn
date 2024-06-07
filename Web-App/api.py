import os
import pandas as pd
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
@app.route('/app/recive_data', methods=['POST'])
def recive_data():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                return jsonify({"error": "no se ha proporcionado ningún archivo"}), 400
            file = request.files['file']

            if file.filename == '':
                return jsonify({"error": "no se ha seleccionado ningún archivo"}), 400

            if file:
                file_path = os.path.join('temp', file.filename)
                file.save(file_path)

                # Procesar el archivo y convertirlo a HTML
                data = pd.read_excel(file_path)
                html_data = data.to_html()

                return jsonify({"success": "archivo guardado", "data": html_data}), 200

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "ocurrió un error al procesar el archivo"}), 400


@app.route('/app/register_courses', methods=['POST'])
def register_courses():
    if request.method == 'POST':
        data = request.get_json()

        # obtenemos los datos ingresados del curso
        nombre_curso        = data['nombre']
        año_curso           = data['año']  # Asegúrate de usar 'año' en lugar de 'anio'
        fecha_inicio_curso  = data['fechaInicio']
        fecha_termino_curso = data['fechaTermino']

        print("############ DATA RECIBIDA ############")
        print(f"Nombre del curso: {nombre_curso}")
        print(f"Año: {año_curso}")
        print(f"Fecha de inicio: {fecha_inicio_curso}")
        print(f"Fecha de termino: {fecha_termino_curso}")
        print("############ FIN DATA RECIBIDA ############")

        return jsonify({"success":"curso recibido"}), 200
        
if __name__ == '__main__':
    os.makedirs('temp', exist_ok=True)
    app.run(debug=True)
