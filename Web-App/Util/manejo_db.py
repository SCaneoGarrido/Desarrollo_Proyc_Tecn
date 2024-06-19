import os
import psycopg2
from dotenv import load_dotenv


class DatabaseManager:
    def __init__(self):
        load_dotenv()
        self.database = os.environ.get('DATABASE')
        self.user = os.environ.get('USER')
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

            if conn is not None:
                return conn
            else:
                print("Error al crear la conexion a la base de datos...")
                return None
        except Exception as e:
            print(f"Error: {e}") 
            
    # INGRESAR UN USUAURIO EN LA BASE DE DATOS (TEMPORAL ELIMINAR LUEGO DE DESARROLLO)
    def insertUserOnDB(self ,nombre, apellido, correo, hash_clave, salt):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            data = (correo, nombre, apellido, hash_clave, salt)
            cursor.execute("""
                INSERT INTO muni_colab (correo, nombre, apellido, hash, salt)
                VALUES(%s, %s, %s, %s, %s)""", data)
            conn.commit()
            return True

        except psycopg2.Error as error:
            print(f"Error: {error}")
            return False

        finally:
            cursor.close()
            conn.close()
    
    # OBTENER EL ID DEL USUARIO
    def get_user_id(self ,correo):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM muni_colab WHERE correo = %s", (correo, ))
            user_id = cursor.fetchone()
            cursor.close()

            if user_id:
                return user_id
            else:
                print("Error al obtener id del usuario...")
                return None
        except Exception as e:
            print(f"Error: {e}")



    # OBTENER LOS CURSOS REGISTRADOS
    def getRegistered_courses(self, user_id):
        pass
        
    # VALIDAR CREDENCIALES
    def validate(self, correo, contraseña):
        from Util.manage_credential import CredentialsManager
        credentialsManager_instance = CredentialsManager()
        conn = self.connect()

        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM muni_colab WHERE correo = %s", (correo, ))
                    user = cursor.fetchone()

                    if user:
                        print("Usuario encontrado")
                        hash_  = user[4]
                        salt_ = user[5]

                        if credentialsManager_instance.validateLogin(contraseña, hash_, salt_):
                            cursor.close()
                            return True
                        else:
                            return False

                    else:
                        print(f"Usuario no encontrado,\n data -> {user}")
                        return None

        except Exception as e:
            print(f"Error: {e}")

    
    # FUNCION PARA CARGAR LOS ASISTENTES EN LA TABLA asistentes
    def CargarAsistentes_cursos(self, array):
        try:
            conn = self.connect()
            cursor = conn.cursor()

            for asistente in array:
                data = (asistente['nombre'], asistente['edad'], asistente['apellido'], asistente['direccion'], asistente['estadoCivil'], asistente['genero'], asistente['rut'])
                cursor.execute("""
                    INSERT INTO asistentes (nombre, edad, apellido, direccion, estadoCivil, genero, rut)
                    VALUES(%s, %s, %s, %s, %s, %s, %s)""", data)

            conn.commit()
            return True
    
        except psycopg2.Error as error:
            print(f"Error: {error}")
            return False

        finally:
            cursor.close()
            conn.close()


        

    # FUNCION PARA INSERTAR UN CURSO EN LA TABLA cursos
    def insertCourseOnDB(self,nombre_curso, fecha_inicio, fecha_fin , colab_id):    
        try:
            conn = self.connect()
            cursor = conn.cursor()
            data = (nombre_curso, fecha_inicio, fecha_fin, colab_id)
            cursor.execute(""" INSERT INTO cursos (nombre_curso, fecha_inicio, fecha_fin, colab_id)
            VALUES(%s, %s, %s, %s)""", data)
            conn.commit()
            return True
        except psycopg2.Error as error:
            print(f"Error: {error}")
            return False
        finally:
            cursor.close()
            conn.close()


