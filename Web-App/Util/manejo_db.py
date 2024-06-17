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
            conn = DatabaseManager.connect()
            cursor = conn.cursor()
            data = (nombre, apellido, correo, hash_clave, salt)
            cursor.execute("""
                INSERT INTO usuarios (Nombre, Apellido, Correo, hash_clave, salt)
                VALUES(%s, %s, %s, %s, %s)""", data)


            conn.commit()
            cursor.close()
            conn.close()
            return True

        except psycopg2.Error as error:
            print(f"Error: {error}")
            return False

    
    def validate(self ,correo, contraseña):
        #importacion tardia para romper dependencia circular
        from Util.manage_credential import credentialsUser
        try:
            conn = DatabaseManager.connect()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (correo, ))
            user = cursor.fetchone()
            cursor.close()

            if user:
                hash_contraseña =user[4]
                salt = user[5]

                if credentialsUser.validateLogin(contraseña, hash_contraseña, salt):
                    return True
                else:
                    return False
                
        except Exception as e:
            print(f"Error: {e}")    
    
    
    def get_user_id(self ,correo):
        try:
            conn = DatabaseManager.connect()
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM usuarios WHERE correo = %s", (correo, ))
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

    