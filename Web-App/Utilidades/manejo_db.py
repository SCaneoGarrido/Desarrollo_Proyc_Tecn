import json
import os
import mysql.connector
from dotenv import load_dotenv


class db_manage:
    def __init__(self):
        load_dotenv()
        self.database = os.environ.get('DATABASE')
        self.user = os.environ.get('USER')
        self.password = os.environ.get('PASSWORD')
        self.host = os.environ.get('HOST')
        self.port = os.environ.get('PORT')
        pass


    def connect(self):
        try:
            conn = mysql.connector.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            
            )
            if conn:
                return conn
        except Exception as e:
            print(f"Error: {e}") 
    
    def insertUserOnDB(self ,nombre, apellido, correo, hash_clave, salt):
        try:
            conn = db_manage.connect()
            cursor = conn.cursor()
            data = (nombre, apellido, correo, hash_clave, salt)
            cursor.execute("""
                INSERT INTO usuarios (Nombre, Apellido, Correo, hash_clave, salt)
                VALUES(%s, %s, %s, %s, %s)""", data)


            conn.commit()
            cursor.close()
            conn.close()
            return True

        except mysql.connector.Error as error:
            print(f"Error: {error}")
            return False

    
    def validate(self ,correo, contraseña):
        #importacion tardia para romper dependencia circular
        from Utilidades.manage_credential import credentialsUser
        try:
            conn = db_manage.connect()
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
            conn = db_manage.connect()
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
