import os
import pandas as pd
import numpy as np
from Util.auxiliar_functions import *
from flask import Flask, request, jsonify, session, render_template, url_for
from flask_cors import CORS
from io import BytesIO
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

# ruta que crea una pre-visualizacion, carga y vinculacion del archivo cargado
@app.route('/app/recive_data/<user_id>', methods=['POST'])
def recive_data(user_id):
    # CREAR LOGICA DE MANEJO DE ASISTENCIA
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            curso_id = request.form.get('cursoId')
            file = request.files['file']
        
            # Asegurarse de que ambos datos están presentes
            if not curso_id or not file:
                return jsonify({"success": False, "message": "Falta el archivo o el cursoId"}), 400

            # Procesar el archivo y el curso_id según sea necesario
            # Aquí puedes añadir tu lógica para manejar el archivo y el curso_id
            print("Curso ID: ", curso_id)
            print("Archivo recibido: ", file.filename)
            print("User ID: ", user_id)


            if 'file' not in request.files:
                return jsonify({"error": "no se ha proporcionado ningún archivo"}), 400
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "no se ha seleccionado ningún archivo"}), 400
            
            try: 
                if file:
                    DatabaseManager_instance = DatabaseManager()
                    # mostrar info 
                    print(f"archivo -> {file.filename}")
                    print(f"user_id -> {user_id}")
                    print(f"curso_id -> {curso_id}")

                    # guardamos el df en temp
                    if not os.path.exists('temp'):
                        os.makedirs('temp')
                    ruta_archivo = os.path.join('temp', file.filename)
                    file.save(ruta_archivo)

                    print("ruta_archivo: ", ruta_archivo)
                    # Leer el archivo directamente en un DataFrame
                    data = pd.read_excel(ruta_archivo)
                    
                    
                    # Convertir el DataFrame a HTML
                    html_data = data.to_html(classes='table table-bordered table-striped')
                    # Guardar el DataFrame en base de datos
                    # si ya existe un dataframe asociado concatenar el nuevo df 
                    # con el existente para crear un nuevo df concatenarlos mediante la primera columna
                    # actualizar la base de datos subiendo el nuevo archivo concatenado

                    existing_data = DatabaseManager_instance.get_existing_file(curso_id)
                    
                    if existing_data is not None:
                        print(" ############### Existe un archivo existente ############### ")
                        print(existing_data)
                    
                    # Mostrar archivo a cargar
                    print(" ############### Archivo a cargar ############### ")
                    print(data)

                    
                    ## AQUI ANTES DE SUBIR EL ARCHIVO DEBEMOS REALIZAR LA ACTUALIZACION DE ASISTENCIA ##
                    # obtener la lista de asistentes
                    lista_asistentes = DatabaseManager_instance.obtenerLista_asistentes(curso_id)
                    if lista_asistentes is not None:
                        print("Se ha encontrado una lista de asistentes asociada al curso")
                        tuplas = lista_asistentes[0]
                        campos = lista_asistentes[1]

                        print(f"tuplas reconocidas -> {tuplas}")
                        print(f"campos reconocidos -> {campos}")

                        indice_nombre = campos.index('nombre')
                        indice_asistenteID = campos.index('asistenteid')

                        # extraemos y normalizamos los campos
                        asistente_data = [
                            (tupla[indice_asistenteID], ' '.join(tupla[indice_nombre].split()).title())
                            for tupla in tuplas
                        ]

                        df_asistentes = pd.DataFrame(asistente_data, columns=['AsistenteID', 'Nombre'])

                        # asistance_df = data
                        data['NOMBRE Y APELLIDOS'] = data['NOMBRE Y APELLIDOS'].str.strip().replace(" ", " ")
                        asistance_df_NamesCol = data['NOMBRE Y APELLIDOS'].apply(lambda x: ' '.join(x.split()).title())

                        asistance_df_names_list = asistance_df_NamesCol.tolist()

                        list_asist_presentes = []

                        # Comparar nombres y añadir el ID a la lista de presentes si el nombre coincide
                        
                        for asistente_id, nombre in zip(df_asistentes['AsistenteID'], df_asistentes['Nombre']):
                            if nombre in asistance_df_names_list:
                                print(f"Se encontro un asistente en el archivo de asistencia subido: {nombre} - {asistente_id}")
                                list_asist_presentes.append(asistente_id)
                            else:
                                print(f"El asistente {nombre} no se encuentra en el archivo de asistencia subido")

                        # actualizamos la base de datos
                        try:
                            asistance_flag = DatabaseManager_instance.update_asistencia(curso_id, list_asist_presentes)

                            if asistance_flag:
                                print("Se ha actualizado la base de datos con la lista de asistentes")
                            else:
                                print("No se ha podido actualizar la base de datos con la lista de asistentes")
                        except Exception as e:
                            print(f"Ocurrior un error al ejecutar el método de actualización de asistencia: {e}")
                            return jsonify({"error": "ocurrio un error al ejecutar el método de actualización de asistencia"}), 400
                    ####################################################################################
                    if existing_data is not None:
                        data.columns = existing_data.columns
                        # concatenamos
                        merged_data = pd.concat([existing_data, data]).drop_duplicates(subset=['NOMBRE Y APELLIDOS'])
                    else:
                        merged_data = data

                    
                    print(" ############### Archivo concatenado ############### ")
                    print(merged_data)

                    bytes_io = BytesIO()
                    merged_data.to_excel(bytes_io, index=False)
                    file_data = bytes_io.getvalue()

                    # actualizar o insertar en la base de datos
                    if existing_data is not None:
                        DatabaseManager_instance.update_file(curso_id, file_data)
                    else:
                        DatabaseManager_instance.insert_file(user_id ,curso_id, file_data)
                    
                    os.remove(ruta_archivo)
                    return jsonify({"success": "archivo guardado", "data": html_data}), 200
            except Exception as e:
                print("Error al previsualizar archivo: ", e)
                return jsonify({"error": "ocurrio un error al previsualizar el archivo"}), 400

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "ocurrió un error al procesar el archivo"}), 400

@app.route('/app/register_courses/<user_id>', methods=['POST'])
def register_courses(user_id):
    if request.method == 'POST':
        data = request.get_json()

        DatabaseManager_instance = DatabaseManager()

        # OBTENER DATOS PARA EL REGISTRO DEL CURSO
        nombre_curso        = data.get('nombre')
        fecha_inicio        = data.get('fechaInicio')
        fecha_termino       = data.get('fechaTermino')
        mes_curso           = data.get('mes_curso')
        escuela             = data.get('escuela')
        actividad_servicio  = data.get('actividad_servicio')
        institucion         = data.get('institucion')
        totalClases         = data.get('totalClases')       
        user_id             = data.get('user_id')  # ESTO ES PARA VINCULAR AL COLABORADOR DE MUNICIPALIDAD CON EL CURSO QUE REGISTRÓ.

        # OBTENER DATOS DE ASISTENTES
        asistentes = data.get('asistentes', [])

        # COMPROBAR DATOS DE CURSOS
        if not nombre_curso or not fecha_inicio or not fecha_termino or not escuela or not actividad_servicio or not institucion or not mes_curso or not totalClases:
            return jsonify({"error": "faltan datos del curso"}), 400
        if not user_id:
            return jsonify({"error": "faltan datos del colaborador"}), 400

        # COMPROBAR DATOS DE ASISTENTES
        if len(asistentes) == 0:
            print("No hay asistentes, lista vacia \n lista -> {} \n".format(asistentes))
            return jsonify({"error": "No se ingresaron asistentes"}), 400
        
        # MOSTREMOS LOS DATOS
        datos_curso = {
            'nombre':               nombre_curso,
            'fechaInicio':          fecha_inicio,
            'fechaTermino':         fecha_termino,
            'mes_curso':            mes_curso,
            'escuela':              escuela,
            'actividad_servicio':   actividad_servicio,
            'institucion':          institucion,
            'totalClases':          totalClases
        }

        print("Los datos del curso son: \n {} \n".format(datos_curso))
        print("Los datos de los asistentes son: \n {} \n".format(asistentes))
        
        # INSERTAR DATOS EN BD
        try:
            curso_id = DatabaseManager_instance.insertCourseOnDB(nombre_curso, fecha_inicio, fecha_termino, mes_curso, escuela, actividad_servicio, institucion, user_id, totalClases)
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

#### RUTA DE MOTOR ANALITICO ####
@app.route('/app/analytical_engine/<user_id>', methods=['GET'])
def analytical_engine(user_id):
    if request.method == 'GET':
        cursoID = request.args.get('cursoID')  # Obtener el cursoID de los parámetros de la solicitud
        DatabaseManager_instance = DatabaseManager()  # Instancia de DatabaseManager
        
        # transformar el CURSO ID A INT
        cursoID = int(cursoID)
        # 1.- Recibimos tanto el User_ID como el Curso_ID.
        if cursoID and user_id:
            print(f"Data recibida para motor de analitca \nUID de usuario -> {user_id} \nUID del curso -> {cursoID}\n Tipo de datos del UID Curso: {type(cursoID)} ")
            
            # 2.- Comprobamos con el User_ID que exista un curso registrado que coincida con el Curso_ID.
            cursoSolicitado = DatabaseManager_instance.obtenerCursoBy_userID_CursoID(user_id, cursoID)

            if cursoSolicitado:
                print(f"Curso solicitado encontrado: {cursoSolicitado}")
                print(f"Respuesta de curso solicitado typedata: {type(cursoSolicitado)}")

                # comprobamos si existe un archivo asociado al curso
                existing_file = DatabaseManager_instance.get_existing_file(cursoID)

                if existing_file is not None:
                    print(f"Archivo de asistencia encontrado \n{existing_file}")
                else:
                    print("No se encontro archivo asociado al curso")
                    return jsonify({"error":"No existe un archivo de asistencia asociado al curso"})

                # obtener lista de asistentes
                lista_asistentes, column_names = DatabaseManager_instance.obtenerLista_asistentes(cursoID)
    
                print(f"""
                    Se ha encontrado la siguiente lista de asistentes para el curso: {cursoSolicitado[1]}\n
                    lista de asistentes: {lista_asistentes}
                """)
                print(f"ripo de datos lista asistentes.\n {type(lista_asistentes)}")

                # Crear un DataFrame con los datos de asistencia
                df_asistencia = pd.DataFrame(lista_asistentes, columns=column_names)
                
                # Verificar si la columna 'asistencia' existe en el DataFrame
                if 'asistencia' not in df_asistencia.columns:
                    df_asistencia['asistencia'] = np.nan  # Inicializar la columna 'asistencia' con NaN si no existe
                
                # Agregar la columna 'asistencia' con los datos de asistencia
                df_asistencia['asistencia'] = df_asistencia['asistencia'].apply(lambda x: 'Presente' if pd.notna(x) and isinstance(x, (int, float)) else np.nan)
                
                print(f"DataFrame de asistencia:\n{df_asistencia}")

                return jsonify({'success': 'Ok'})
            else:
                print("No se encontro el curso solicitado asociado al usuario")
                return jsonify({"error":"No se encontro el curso solicitado o no se encontro en la base de datos"}), 404

        else:
            print("Faltan Datos")
            return jsonify({'error': 'Faltan datos, id curso = {} \n User id = {}'.format(cursoID, user_id)}), 400

    else:
        return jsonify({'error': 'Método inválido'}), 500


# ESTA RUTA TE ENVIA LA LISTA DE ASISTENTES DE UN CURSO
# PARAMETROS NECESARIOS: CURSO_ID
# SE DEBE PASAR POR URL
@app.route('/app/get_list_asistances/<curso_id>', methods=['GET'])
def get_list_asistances(curso_id):
    if request.method == 'GET':
        DatabaseManager_instance = DatabaseManager()
        if curso_id:
            asistentes = DatabaseManager_instance.obtenerLista_asistentes(curso_id)

            if asistentes is not None or len(asistentes) > 0:
                return jsonify(asistentes), 200
            else:
                return jsonify({'error': 'No se encontraron asistentes para el curso'}), 404
    else:   
        print('Invalid Method')
        return jsonify({'error':'Invalid Method'}), 400



@app.route('/app/add_certification/<curso_id>/<asistente_id>', methods=['POST'])
def add_certification(curso_id, asistente_id):
    # RUTA DE SUBIR CERTIFICADO DE CURSO
    if request.method == 'POST':
        certificado = request.files['file']

        if not curso_id or not certificado or not asistente_id:
            return jsonify({'error': 'faltan datos'}), 400
        
        if 'file' not in request.files:
            return jsonify({'error': 'no se ha proporcionado ningun archivo'}), 400
        
        if certificado.filename == '':
            return jsonify({'error': 'No se ha seleccionado ningun archivo'}), 400

        # Guardamos el certificado en una ruta temporal 
        if not os.path.exists('certificados_temp'):
            os.makedirs('certificados_temp')
        ruta_certificado = os.path.join('certificados_temp', certificado.filename)
        certificado.save(ruta_certificado)

        try:
            # Leer el archivo y obtener el tipo
            file_data = read_file(ruta_certificado)
            file_type = get_file_type(ruta_certificado)

            # Instancia de DatabaseManager
            DatabaseManager_instance = DatabaseManager()

            # Insertar el archivo en la base de datos
            success = DatabaseManager_instance.subir_certificado(curso_id, file_data, asistente_id, file_type)
            if not success:
                return jsonify({'error': 'Error al insertar la certificación en la base de datos'}), 500

        except Exception as e:
            print(f'Error al subir certificado de curso\n Error -> {e}')
            return jsonify({'error': 'Internal Server Error'}), 500
        finally:
            # Eliminar el archivo temporal
            os.remove(ruta_certificado)
        
        print(f"Datos recibidos:\n Curso UID: {curso_id}\n Asistente UID: {asistente_id}\n Certificado: {certificado.filename}")
        return jsonify({'success': 'Se han recibido los datos correctamente'}), 200

    else:
        print("Invalid Method")
        return jsonify({'error': 'Invalid Method'}), 405


if __name__ == '__main__':
    app.run(debug=True)