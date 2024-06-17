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
            
    
    def insertUserOnDB(self ,nombre, apellido, correo, hash_clave, salt):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            data = (nombre, apellido, correo, hash_clave, salt)
            cursor.execute("""
                INSERT INTO empleados (nombre, apellido, mail, hash_contraseña, salt)
                VALUES(%s, %s, %s, %s, %s)""", data)
            conn.commit()
            return True

        except psycopg2.Error as error:
            print(f"Error: {error}")
            return False

        finally:
            cursor.close()
            conn.close()
    
    def get_user_id(self ,correo):
        try:
            conn = self.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT id_empleado FROM empleados WHERE mail = %s", (correo, ))
            user_id = cursor.fetchone()
            cursor.close()

            if user_id:
                return user_id
            else:
                print("Error al obtener id del usuario...")
                return None
        except Exception as e:
            print(f"Error: {e}")


    def insertCourseOnDB(self ,nombre_curso, course_year, start_date, finish_date):
        pass
        # GENERAR LOGICA DE INSERTAR CURSOS

    
    def UploadFileToBD(self):
        pass
        # GENERAR LOGICA DE INSERTAR ARCHIVOS DE CURSOS

    
    def validate(self, correo, contraseña):
        from Util.manage_credential import CredentialsManager
        credentialsManager_instance = CredentialsManager()
        conn = self.connect()

        if conn is None:
            return None
        
        try:
            with conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM empleados WHERE mail = %s", (correo, ))
                    user = cursor.fetchone()
                    if user:
                        hash_contraseña =user[4]
                        salt = user[5]

                        if credentialsManager_instance.validateLogin(contraseña, hash_contraseña, salt):
                            print("Credenciales Correctas, permitiendo acceso...")
                            cursor.close()
                            return True
                        else:
                            print("Credenciales incorrectas...")
                            return False
                    else:
                        print("Usuario no encontrado...")
                        return None
        except Exception as e:
            print(f"Error: {e}")
        

# TESTEO DE CONEXION A BASE DE DATOS

