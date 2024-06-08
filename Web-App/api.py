import os
import pandas as pd
from flask import Flask, request, jsonify, session, render_template
from flask_cors import CORS

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'supersecretkey'  # Necesario para usar sesiones
CORS(app)

# Lista para almacenar los cursos registrados
cursos_registrados = []

# Diccionario para almacenar los DataFrames asociados a los cursos
dataframes_cursos = {}

# Ruta del archivo CSV donde se guardarán las vinculaciones
CSV_FILE_PATH = 'vinculaciones.csv'

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
                # Leer el archivo directamente en un DataFrame
                data = pd.read_excel(file)
                # Convertir el DataFrame a HTML
                html_data = data.to_html(classes='table table-bordered table-striped')
                # Guardar el DataFrame en una variable de sesión o en memoria
                session['uploaded_data'] = data.to_dict()
                return jsonify({"success": "archivo guardado", "data": html_data}), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "ocurrió un error al procesar el archivo"}), 400

@app.route('/app/register_courses', methods=['POST'])
def register_courses():
    if request.method == 'POST':
        data = request.get_json()
        # obtenemos los datos ingresados del curso
        nombre_curso = data['nombre']
        año_curso = data['año']  # Asegúrate de usar 'año' en lugar de 'anio'
        fecha_inicio_curso = data['fechaInicio']
        fecha_termino_curso = data['fechaTermino']
        # Crear el curso_id combinando el nombre del curso y un sufijo _id
        curso_id = f"{nombre_curso.replace(' ', '_')}_id"
        # Agregar el curso a la lista de cursos registrados
        curso = {
            "id": curso_id,
            "nombre": nombre_curso,
            "año": año_curso,
            "fechaInicio": fecha_inicio_curso,
            "fechaTermino": fecha_termino_curso
        }
        cursos_registrados.append(curso)
        print("############ DATA RECIBIDA ############")
        print(f"Nombre del curso: {nombre_curso}")
        print(f"Año: {año_curso}")
        print(f"Fecha de inicio: {fecha_inicio_curso}")
        print(f"Fecha de termino: {fecha_termino_curso}")
        print("############ FIN DATA RECIBIDA ############")
        return jsonify({"success": "curso recibido"}), 200

@app.route('/app/get_courses', methods=['GET'])
def get_courses():
    return jsonify(cursos_registrados), 200

@app.route('/app/vincular_archivo_curso', methods=['POST'])
def vincular_archivo_curso():
    if request.method == 'POST':
        data = request.get_json()
        curso_id = data.get('cursoId')
        if not curso_id:
            return jsonify({"success": False, "error": "cursoId no proporcionado"}), 400
        try:
            # Obtener el DataFrame de la variable de sesión o memoria
            if 'uploaded_data' not in session:
                return jsonify({"success": False, "error": "No hay datos cargados"}), 400
            df = pd.DataFrame(session['uploaded_data'])
            # Asociar el DataFrame con el curso
            dataframes_cursos[curso_id] = df
            html_data = df.to_html(classes='table table-bordered table-striped')
            # Guardar la vinculación en un archivo CSV
            df['curso_id'] = curso_id
            df['nombre_curso'] = next((curso['nombre'] for curso in cursos_registrados if curso['id'] == curso_id), 'Desconocido')
            if os.path.exists(CSV_FILE_PATH):
                df.to_csv(CSV_FILE_PATH, mode='a', header=False, index=False)
            else:
                df.to_csv(CSV_FILE_PATH, mode='w', header=True, index=False)
            # Agregar print para ver la vinculación en la terminal
            print(f"Curso ID: {curso_id} vinculado con el siguiente DataFrame:")
            print(df)
            return jsonify({"success": True, "data": html_data}), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"success": False, "error": "ocurrió un error al vincular el archivo"}), 400

if __name__ == '__main__':
    app.run(debug=True)