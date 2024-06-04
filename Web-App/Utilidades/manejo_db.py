import json
import psycopg2  # type: ignore


class db_manage:
    def __init__(self):
        pass

    @staticmethod
    def connect():

        try:
            with open('Backend/Informacion/db_config.json', 'r') as f:
                credenciales = json.load(f)

            database = credenciales.get('database')
            user = credenciales.get('user')
            host = credenciales.get('host')
            password = credenciales.get('password')
            port = credenciales.get('port')

            conn = psycopg2.connect(
                    user=user,
                    password=password,
                    host=host,
                    database=database,
                    port=port,
                    )

            if conn:
                print(f"Conexion exitosa a la base de datos")
                return conn
                
        except psycopg2.Error as e:
            print(f"Error al conectar a la base de datos: {e}")


    @staticmethod
    def insertUserOnDB(nombre, apellido, correo, hash_clave, salt):
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

        except (Exception, psycopg2.DatabaseError) as error:
            print(f"Error: {error}")
            return False

    @staticmethod
    def validate(correo, contraseña):
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
    
    @staticmethod
    def get_user_id(correo):
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
