import os
import pandas as pd
from flask import Flask, request, jsonify, session, render_template, url_for
from flask_cors import CORS
from io import BytesIO
from Util.manejo_db import DatabaseManager
from Util.manage_credential import CredentialsManager
import numpy as np

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
                    #lista_asistentes = DatabaseManager_instance.obtenerLista_asistentes(curso_id)
                    #if lista_asistentes is not None:
                    #    print(f"Lista de asistentes del curso solicitado")
                    #    tuplas = lista_asistentes[0]
                    #    campos = lista_asistentes[1]
                    #    indice_nombre = campos.index('nombre')
                    #    nombres = [tupla[indice_nombre].strip().replace("  ", " ") for tupla in tuplas]  # Limpia espacios adicionales
                    #    
                    

                                        
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
##################################################################################################################################
#                                     !!!!!!!!! REVISAR ESTA RUTA !!!!!!!!!!!!!!!!!                                              #   
# LA RUTA A REVISAR ES: @app.route('/app/test/<curso_id>', methods=['GET'])                                                      #   
# LAS PRUEBAS SE REALIZAN UTILIZANDO POSTMAN                                                                                     #   
# PARA LA PETICION USA: http://127.0.0.1:5000/app/test/8                                                                         #   
# EN LA PARTE DE BODY, SELECCIONAS:                                                                                              #       
# - form-data                                                                                                                    #       
# - CAMPO 'Key' pones file                                                                                                       #       
# - CAMPO 'Value' cargas el archivo de asistencia de 'Asistencia Alfabetizacion Digital.xlsx' (esta en la carpeta test)          #
# SE USA EL METODO DE update_asistencia DE LA INSTANCIA DatabaseManager                                                          #
# EL METODO RECIBE LA LISTA DE ASISTENTES PRESENTES (list_asist_presentes) y el cursoid                                          #   
# ======================================================================================================================= #      #
#                  !!!!!!!! LO QUE SE DEBE REVISAR ES LO SIGUIENTE !!!!!!!!!!!!!!                                                #   
#  LA COLUMNA ASISTENCIA DE LA TABLA asistentes NO SE ACTUALIZA                                                                  #                                                   
#  EL POSIBLE PROBLEMA ES POR LA NORMALIZACION DE LOS CAMPOS                                                                     #
#  ====================================================================================================================== #      #   
#                                                                                                                                #           
#                                          SUERTE MANIN :D                                                                       #       
#                      deje una captura de pantalla de como deberia verse el postman                                             #      
##################################################################################################################################
@app.route('/app/test/<curso_id>', methods=['GET'])
def test(curso_id):
    if request.method == 'GET':
        try:
            file = request.files['file']
            print(f"Nombre del archivo enviado -> {file.filename}")
            print(f'curso id solicitado, {curso_id}')
            DatabaseManager_instance = DatabaseManager()
            lista_asistentes = DatabaseManager_instance.obtenerLista_asistentes(curso_id)

            if lista_asistentes is not None:
                print(f"Hay una lista de asistentes al curso solicitado\n")
                tuplas = lista_asistentes[0]
                campos = lista_asistentes[1]

                indice_nombre = campos.index('nombre')
                nombres = [tupla[indice_nombre].strip().replace("  ", " ") for tupla in tuplas]  # Limpia espacios adicionales

                if not os.path.exists('temp'):
                    os.makedirs('temp')
                ruta_archivo = os.path.join('temp', file.filename)
                file.save(ruta_archivo)
                
                asistance_df = pd.read_excel(ruta_archivo)  # Este es el Excel de asistencia

                asistance_df_NamesCol = asistance_df['NOMBRE Y APELLIDOS'].str.strip().replace("  ", " ")  # Limpia espacios adicionales

                print(f"Tipo de dato de 'nombres' -> {type(nombres)}\n Tipo de dato de 'asistance_df_NamesCol' -> {type(asistance_df_NamesCol)}\n\n")

                print(f"CONTENIDO DE 'nombres' -> {nombres}\n")
                print(f"CONTENIDO DE 'asistance_df_NamesCol' :\n {asistance_df_NamesCol}\n")

                # Convertir la columna del DataFrame a una lista
                asistance_df_names_list = asistance_df_NamesCol.tolist()

                # CREAR UNA LISTA DONDE SE ALMACENARAN LOS ASISTENTES QUE SI FUERON ENCONTRADOS
                list_asist_presentes = []

                asistance_df_names_list = [nombre.strip().title() for nombre in asistance_df_names_list]


                # REALIZAR COMPROBACION DE LA LISTA DE ASISTENTES CON EL DATAFRAME
                for nombre in nombres:
                    if nombre in asistance_df_names_list:
                        print(f"Se encontró un asistente en el archivo de asistencia subido: {nombre}")
                        list_asist_presentes.append(nombre)
                    else:
                        print(f"No se encontró el nombre - {nombre}")

                # ACTUALIZAMOS LA ASISTENCIA
                try:
                    asistance_flag = DatabaseManager_instance.update_asistencia(curso_id, list_asist_presentes)

                    if asistance_flag:
                        print('Asistencia actualizada correctamente')
                    else:
                        print('algo salio mal al actualizar la asistencia')
                except Exception as e:
                    print(f'Ocurrio un error al ejecutar el metodo de actualizacion de asistencia')

                
                return jsonify({'message': list_asist_presentes}), 200
            else:
                print(f"Hubo un error al obtener la lista de Asistenes del curso solicitado")
                return jsonify({'error': 'el curso solicitado no posee una lista de asistentes'}), 404
        except Exception as e:
            print(f"Error en testeo: -> {e}")
            return jsonify({'error': 'Error en la ejecucion del test'}), 404

    else:
        print('Metodo no valido')
        return jsonify({'error': 'Bad Request'}), 500



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
        user_id             = data.get('user_id')  # ESTO ES PARA VINCULAR AL COLABORADOR DE MUNICIPALIDAD CON EL CURSO QUE REGISTRÓ.

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
            'nombre':               nombre_curso,
            'fechaInicio':          fecha_inicio,
            'fechaTermino':         fecha_termino,
            'mes_curso':            mes_curso,
            'escuela':              escuela,
            'actividad_servicio':   actividad_servicio,
            'institucion':          institucion,
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

if __name__ == '__main__':
    app.run(debug=True)