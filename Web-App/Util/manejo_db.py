import os
from datetime import datetime
import psycopg2
import math
import pandas as pd
from dotenv import load_dotenv
from io import BytesIO

class DatabaseManager:
    def __init__(self):
        load_dotenv()
        self.database = os.environ.get('DATABASE')
        self.user = os.environ.get('USER_BD') # CAMBIEN ESTA LINEA EN SUS .ENV
        self.password = os.environ.get('PASSWORD')
        self.host = os.environ.get('HOST')
        self.port = os.environ.get('PORT')

    def connect(self):
        try:
            conn = psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return conn
        except Exception as e:
            print(f"Error: {e}")
            return None

    def insertUserOnDB(self, nombre, apellido, correo, hash_clave, salt):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            data = (correo, nombre, apellido, hash_clave, salt)
            cursor.execute("""
                INSERT INTO muni_colab (correo, nombre, apellido, hash, salt)
                VALUES (%s, %s, %s, %s, %s)
            """, data)
            conn.commit()
            return True
        except psycopg2.Error as error:
            print(f"Error: {error}")
            return False
        finally:
            cursor.close()
            conn.close()

    def get_user_id(self, correo):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM muni_colab WHERE correo = %s", (correo,))
            user_id = cursor.fetchone()
            cursor.close()
            if user_id:
                return user_id[0]  # devolver solo el id
            else:
                print("Error al obtener id del usuario...")
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None

    def getRegistered_courses(self, user_id):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Cursos WHERE colab_id = %s", (user_id,))
            cursos = cursor.fetchall()
            cursor.close()
            if cursos:
                return cursos
            else:
                return []
        except Exception as e:
            print(f"Error: {e}")
            return []

    def validate(self, correo, contraseña):
        from Util.manage_credential import CredentialsManager
        credentialsManager_instance = CredentialsManager()
        conn = self.connect()

        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM muni_colab WHERE correo = %s", (correo,))
                    user = cursor.fetchone()
                    if user:
                        print("Usuario encontrado")
                        hash_ = user[4]
                        salt_ = user[5]
                        if credentialsManager_instance.validateLogin(contraseña, hash_, salt_):
                            return True
                        else:
                            return False
                    else:
                        print(f"Usuario no encontrado,\n data -> {user}")
                        return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    def validar_edad(self,edad):
        if isinstance(edad, (int, float)):
            if math.isnan(edad):
                return None  # Convertir NaN a None
            else:
                return int(edad)  # Convertir a entero si es posible
        else:
            return None  # Manejar otros tipos de datos

    def CargarAsistentes_cursos(self, asistentes):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            
            for asistente in asistentes:
                edad = self.validar_edad(asistente['EDAD'])
                dv = asistente['DV'] if asistente['DV'] and len(str(asistente['DV'])) == 1 else None

                data = (
                    asistente['RUT'],
                    dv,
                    asistente['NOMBRE Y APELLIDOS'],
                    asistente['TELEFONO'],
                    asistente['CORREO'],
                    asistente['GENERO'],
                    edad,
                    asistente['NACION.'],
                    asistente['COMUNA'],
                    asistente['BARRIO'],
                    asistente['curso_id'],  # Asegúrate de tener este campo en la tupla data
                )
                
                print(f"Data a insertar: {data}")

                cursor.execute("""
                    INSERT INTO asistentes (rut, digito_v, nombre, telefono, correo, genero, edad, nacionalidad, comuna, barrio, cursoid)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, data)
            
            conn.commit()
            return True
        except psycopg2.Error as error:
            print(f"Error error raro en CargarAsistentes_cursos -> {error}")
            return False
        finally:
            cursor.close()
            conn.close()

    def insertCourseOnDB(self, nombre_curso,  fecha_inicio, fecha_fin, mes_curso, escuela, actividad_servicio, institucion, colab_id, total_clases):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            data = (nombre_curso, fecha_inicio, fecha_fin, colab_id, escuela, actividad_servicio, institucion, mes_curso, total_clases)
            cursor.execute("""
                INSERT INTO cursos (nombre_curso, fecha_inicio, fecha_fin, colab_id, escuela, actividad_servicio, institucion, mes, total_clases)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING CursoID
            """, data)
            curso_id = cursor.fetchone()[0] 
            conn.commit()

            return curso_id
        except psycopg2.Error as error:
            print(f"Error raro en insertCourseOnDB -> {error}")
            return None
        finally:
            cursor.close()
            conn.close()

    def getMuni_colabInfo(self, user_id):
        try:
            conn = self.connect()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT correo, nombre, apellido FROM muni_colab WHERE id = %s", (user_id,))
                    info = cursor.fetchone()

                    if info:
                        print(f"Informacion del usuario encontrada -> \n {info}")
                        return info
                    else:
                        print(f"Usuario no encontrado,\n data -> {info}")
                        return None
        except Exception as e:
            print(f"Ocurrio un error al obtener la informacion del usuario de la base de datos \n Error -> {e}")

        finally:
            cursor.close()
            conn.close()


    #### FUNCIONES RELACIONADAS A LA INSERCION DEL ARCHIVO DE ASISTENCIAS #### 

    # ESTA FUNCION DEVUELVE EL ARCHIVO CARGADO EN LA BASE DE DATOS
    def get_existing_file(self, curso_id):
        try:
            conn = self.connect()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT archivoasistencia FROM asistencia WHERE cursoid = %s", (curso_id,))
                    result = cursor.fetchone()

                    if result:
                        file_data = result[0]
                        # Si el archivo está guardado como bytes en la base de datos
                        # Puedes cargarlo utilizando BytesIO para leerlo con pandas
                        df = pd.read_excel(BytesIO(file_data))
                        return df  # Retornamos el DataFrame cargado desde el archivo
                    else:
                        print(f"No se han encontrado resultados para curso_id {curso_id}")
                        return None
        except Exception as e:
            print(f"Error raro en get_existing_file -> {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    # ESTA FUNCION ACTUALIZA EL ARCHIVO CARGADO EN LA BASE DE DATOS

    def update_file(self, curso_id, file_data):
        try:
            conn = self.connect()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        UPDATE asistencia 
                        SET archivoasistencia = %s, fecha_subida = %s
                        WHERE cursoid = %s
                    """, (file_data, datetime.now(), curso_id))
                    conn.commit()
        except Exception as e:
            print(f"Error raro en update_file -> {e}")
        finally:
            cursor.close()
            conn.close()


    # ESTA FUNCION INSERTA EL ARCHIVO CARGADO EN LA BASE DE DATOS
    def insert_file(self, user_id, cursoid, file_data):
        try:
            conn = self.connect()
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("INSERT INTO asistencia (cursoid, archivoasistencia, colab_id, fecha_subida) VALUES (%s, %s, %s, %s)", (cursoid, file_data, user_id, datetime.now()))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error raro en insert_file -> {e}")
        
        finally:
            cursor.close()
            conn.close()
    
    ################ FIN FUNCIONES PARA CARGAR ARCHIVOS ##################

    def obtenerLista_asistentes(self, cursoid):
        try:
            conn = self.connect()
            if conn is None:
                return [], []  # Devuelve listas vacías en caso de error
            
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM asistentes WHERE cursoid = %s", (cursoid,))
                    lista_asistentes = cursor.fetchall()

                    column_names = [description[0] for description in cursor.description]
                    return lista_asistentes if lista_asistentes else [], column_names

        except Exception as e:
            print(f"Error en 'obtenerLista_asistentes - DatabaseManager' \nError -> {e}")
            return None  # Devuelve listas vacías en caso de excepción
        finally:
            if conn:
                conn.close()

    def obtenerCursoBy_userID_CursoID(self, user_id, cursoid):
        try:
            conn = self.connect()

            if conn is None:
                return None
            
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM cursos WHERE cursoid=%s AND colab_id=%s", (cursoid, user_id))
                    curso = cursor.fetchone()

                    if curso:
                        return curso
                    else:
                        return None
        except Exception as e:
            print(f"Error en 'obtenerCursoBy_userID_CursoID()\n Error: {e}")

        finally:
            cursor.close()
            conn.close()
    
    
    def update_asistencia(self, cursoid, lista_id):
        try:
            conn = self.connect()
            with conn:
                with conn.cursor() as cursor:
                    # Obtener el total de clases para el curso
                    cursor.execute(
                        """
                        SELECT total_clases FROM cursos
                        WHERE cursoid = %s
                        """,
                        (cursoid,)
                    )
                    total_clases = cursor.fetchone()
                    
                    if not total_clases:
                        print(f"No se encontró el curso con id: {cursoid}")
                        return False

                    total_clases = total_clases[0]
                    
                    for id in lista_id:
                        print(f"Procesando id -> {id} de la lista de id presentes\n")
                        # Consulta de prueba para verificar coincidencia
                        cursor.execute(
                            """
                            SELECT * FROM asistentes
                            WHERE cursoid = %s AND asistenteid = %s
                            """,
                            (cursoid, id)
                        )
                        resultado = cursor.fetchone()
                        if resultado:
                            print(f"Se encontró coincidencia: {resultado}")
                            # Ejecutar la actualización
                            cursor.execute(
                                """
                                UPDATE asistentes
                                SET clases_asistidas = COALESCE(clases_asistidas, 0) + 1
                                WHERE cursoid = %s AND asistenteid = %s
                                RETURNING clases_asistidas
                                """,
                                (cursoid, id)
                            )
                            asistencia_actualizada = cursor.fetchone()[0]
                            # Calcular el promedio de asistencia sin redondear y convertirlo a porcentaje
                            promedio_asistencia = (asistencia_actualizada / total_clases) * 100
                            print(f"El promedio de asistencia es: {promedio_asistencia}%")
                            cursor.execute(
                                """
                                UPDATE asistentes
                                SET asistencia_promedio = %s
                                WHERE cursoid = %s AND asistenteid = %s
                                """,
                                (promedio_asistencia, cursoid, id)
                            )
                            print(f"Filas actualizadas: {cursor.rowcount}")
                        else:
                            print(f"No se encontró coincidencia para id: {id}")
                return True
        except Exception as e:
            print(f"Error en 'update_asistencia()'\n Error: {e}")
            return False
        finally:
            if conn:
                conn.close()    

    def subir_certificado(self, cursoid, certificado_file, asistente_id, file_type):
        try:
            conn = self.connect()
            if conn is None:
                print(f"Error al realizar conexion con la base de datos")
                return False
            
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO certificados (cursoid, asistenteid, archivocertificado, file_type)
                        VALUES (%s, %s, %s, %s)
                        """, (cursoid, asistente_id, certificado_file, file_type)
                    )
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Error en 'subir_certificado()'\n Error: {e}")
            return None
        
        finally:
            cursor.close()
            conn.close()