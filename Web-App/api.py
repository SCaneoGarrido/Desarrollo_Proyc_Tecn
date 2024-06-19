import os
import pandas as pd
from flask import Flask, request, jsonify, session, render_template, url_for
from flask_cors import CORS
from Util.manejo_db import DatabaseManager
from Util.manage_credential import CredentialsManager

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

@app.route('/app/get_courses/<user_id>', methods=['GET'])
def get_courses(user_id):
    try:
        if user_id:
            DatabaseManager_instance = DatabaseManager()

            cursos = DatabaseManager_instance.getRegistered_courses(user_id)
            if len(cursos) > 0:
                return jsonify({"cursos": cursos}), 200
            else:
                return jsonify({"error": "no hay cursos registrados"}), 400

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "ocurrio un error al obtener los cursos"}), 400

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

@app.route('/app/register_courses/<user_id>', methods=['POST'])
def register_courses(user_id):
    if request.method == 'POST':
        data = request.get_json()
        # obtenemos los datos ingresados del curso
        nombre_curso = data['nombre']
        año_curso = data['año']
        fecha_incio_curso = data['fechaInicio']
        fecha_termino_curso = data['fechaTermino']
        asistentes = data.get('asistentes', [])


        print("DATA DE ENTRADA. \n", nombre_curso, "\n", año_curso, "\n", fecha_incio_curso, "\n", fecha_termino_curso, "\n", asistentes)
        

        response = {
            "message": "Curso creado exitosamente",
            "data": {
                "nombre_curso": nombre_curso,
                "año_curso": año_curso,
                "fecha_inicio_curso": fecha_incio_curso,
                "fecha_termino_curso": fecha_termino_curso,
                "user_id": user_id,
                "asistentes": asistentes
            }
        }
     
        print(f"Data de ingreso a registro -> {response}")

    
    
        # IMPLEMENTAR LOGICA DE CARGA DE CURSO + RELACION DE COLABORADOR QUE CARGO EL CURSO
        ######
        if not nombre_curso or not año_curso or not fecha_incio_curso or not fecha_termino_curso:
            print("No se proporcionaron los datos requeridos")
            return jsonify({'error': 'No se proporcionaron los datos requeridos'}), 400
        else:
            # aqui implementa logica si es que los datos de los cursos llegaron correctamente
            pass
        # IMPLEMENTAR LOGICA DE CARGA DE ASISTENTES A TABLA "ASISTENTES" + RELACION ASISTENTE -> CURSO
        if len(asistentes) == 0:
            print(f"Asistentes vacio -> {asistentes}")
            return jsonify({'error': 'No se proporcionaron asistentes'}), 400
        else:
            # aqui implementa logica si es que los datos de los asistentes llegaron correctamente
            pass
        #####
        

        
    else:
        return jsonify({'error':'Invalid Method'}), 405
        
@app.route('/app/vincular_archivo_curso/<user_id>', methods=['POST'])
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
            html_data = df.to_html(classes='table table-bordered table-striped') # no se debe perder
            # Guardar la vinculación en un archivo CSV
            df['curso_id'] = curso_id
            df['nombre_curso'] = next((curso['nombre'] for curso in cursos_registrados if curso['id'] == curso_id), 'Desconocido')
            if os.path.exists(CSV_FILE_PATH):
                # Agregar una línea de separación antes de concatenar los nuevos datos
                with open(CSV_FILE_PATH, 'a') as f:
                    f.write('\n' + '-'*50 + '\n')
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

# RUTA PARA MANEJAR EL LOGIN
@app.route('/app/login', methods=['POST'])
def handle_login():
    DatabaseManager_instance = DatabaseManager() # Instancia de clase para uso de metodo de validacion de credenciales.
    if request.method == 'POST':
        try:
            data = request.get_json()

            if not data: 
                print("No se proporcionaron datos")
                return jsonify({"error": "No se proporcionaron datos"}), 400
            
            correo = data.get('correo')
            contraseña = data.get('contrasena')

            if not correo or not contraseña:
                print("No se proporcionaron correo o contraseña")
                print()
                return jsonify({"error": "No se proporcionaron correo o contraseña"}), 400
            
            print("Data de entrada: ", correo, " - ", contraseña)
            user = DatabaseManager_instance.validate(correo, contraseña)
            if user:
                user_id = DatabaseManager_instance.get_user_id(correo)
                if user_id:
                    return jsonify({'url':url_for('home'), "user_id": user_id}), 200

        except ValueError as ve:
            print(f"Error: {ve}")
            return jsonify({"error": "ocurrio un error al iniciar sesion"}), 400
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "ocurrio un error al iniciar sesion"}), 400
    
# RUTA PARA CREAR CREDENCIALES (AUXILIAR -> ELIMINAR LUEGO DEL PROYECTO)
@app.route('/app/create_user', methods=['POST'])
def create_user():
    CredentialsManager_instance = CredentialsManager()
    if request.method == 'POST':
        try:
            data = request.get_json()

            if not data:
                print(f"No se proporcionardon datos: {data}")
                return jsonify({"error": "No se proporcionaron datos"}), 400
            
            nombre = data.get('nombre')
            apellido = data.get('apellido')
            correo = data.get('correo')
            contraseña = data.get('contraseña')

            if not nombre or not apellido or not correo or not contraseña:
                print("Datos necesarios para el registro no proporcionados")
                return jsonify({"error": "Datos necesarios para el registro no proporcionados"}), 400
            
            if CredentialsManager_instance.genCredentials(nombre, apellido, correo, contraseña):
                return jsonify({'message': 'Credenciales generadas correctamente'}), 200
            else:
                return jsonify({'message': 'Error al generar credenciales'}), 400
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "ocurrio un error al crear usuario"}), 400
    else:
        return jsonify({'error':'Invalid Method'}), 400

if __name__ == '__main__':
    app.run(debug=True)