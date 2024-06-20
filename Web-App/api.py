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
            if cursos:
                return jsonify({"cursos": cursos}), 200
            else:
                return jsonify({"error": "no hay cursos registrados"}), 400
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "ocurrió un error al obtener los cursos"}), 400

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

        DatabaseManager_instance = DatabaseManager()

        # OBTENER DATOS PARA EL REGISTRO DEL CURSO
        nombre_curso = data.get('nombre')
        fecha_inicio = data.get('fechaInicio')
        fecha_termino = data.get('fechaTermino')
        mes_curso = data.get('mes_curso')
        escuela = data.get('escuela')
        actividad_servicio = data.get('actividad_servicio')
        institucion = data.get('institucion')
        user_id = data.get('user_id')  # ESTO ES PARA VINCULAR AL COLABORADOR DE MUNICIPALIDAD CON EL CURSO QUE REGISTRÓ.

        # OBTENER DATOS DE ASISTENTES
        asistentes = data.get('asistentes', [])

        # COMPROBAR DATOS DE CURSOS
        if not nombre_curso or not fecha_inicio or not fecha_termino or not escuela or not actividad_servicio or not institucion or not mes_curso:
            return jsonify({"error": "faltan datos del curso"}), 400
        if not user_id:
            return jsonify({"error": "faltan datos del colaborador"}), 400

        # COMPROBAR DATOS DE ASISTENTES
        if len(asistentes) == 0:
            print("No hay asistentes, lista vacia \n lista -> {} \n".format(asistentes))
            return jsonify({"error": "No se ingresaron asistentes"}), 400
        
        # MOSTREMOS LOS DATOS
        datos_curso = {
            'nombre': nombre_curso,
            'fechaInicio': fecha_inicio,
            'fechaTermino': fecha_termino,
            'mes_curso': mes_curso,
            'escuela': escuela,
            'actividad_servicio': actividad_servicio,
            'institucion': institucion,
        }

        print("Los datos del curso son: \n {} \n".format(datos_curso))
        print("Los datos de los asistentes son: \n {} \n".format(asistentes))
        
        # INSERTAR DATOS EN BD
        try:
            curso_id = DatabaseManager_instance.insertCourseOnDB(nombre_curso, fecha_inicio, fecha_termino, mes_curso, escuela, actividad_servicio, institucion, user_id,)
            if curso_id:
                if len(asistentes) > 0:
                    for asistente in asistentes:
                        asistente['curso_id'] = curso_id  # aquí agrego una nueva clave 'curso_id' al diccionario 'asistente'
                    if DatabaseManager_instance.CargarAsistentes_cursos(asistentes):
                        return jsonify({"message":"Curso y asistentes registrados"}), 200
                    else:
                        return jsonify({"message":"Ocurrio un error al registrar asistentes"}), 400
                else:
                    return jsonify({"message":"Curso cargado correctamente pero no se proporcionaron asistentes"}), 200
            else:
                return jsonify({"message":"Ocurrio un error al registrar el curso"}), 400
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": str(e)}), 500  # Devuelve el error como respuesta HTTP 500
    else:
        return jsonify({"error": "Invalid Method"}), 400
        
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


@app.route('/app/get_info_User/<user_id>', methods=['GET'])
def getInfo_muniColab(user_id):
    if request.method == 'GET':
        try:
            DatabaseManager_instance = DatabaseManager()
            if user_id:
                info = DatabaseManager_instance.getMuni_colabInfo(user_id)
                if info:
                    return jsonify({"info": info}), 200
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "ocurrio un error al obtener la información del usuario"}), 400


if __name__ == '__main__':
    app.run(debug=True)
