from Util.manejo_db import DatabaseManager
import hashlib
import secrets


class credentialsUser:
    def __init__(self):
        pass    

     
    def genCredentials(self, nombre, apellido, correo, contraseña):
        try:
            nombre = nombre
            apellido = apellido
            correo = correo
           
            salt = secrets.token_hex(16)

            salted_passwd = contraseña + salt
            hashed_passwd =  hashlib.sha256(salted_passwd.encode()).hexdigest()
            contraseña = hashed_passwd
            print("Credenciales para el usuario: ")
            print(f"Nombre: {nombre}")
            print(f"Apellido: {apellido}")
            print(f"Correo: {correo}")
            print(f"contraseña: {contraseña}")
            print(f"Salt: {salt}")
           
            if (DatabaseManager.insertUserOnDB(nombre, apellido, correo, contraseña, salt)):
                print('Usuario agregado')
                return True


            return False

        except Exception as e:
           print(f"Error al registrar usuario: {e}")
        return False           
    
    def validateLogin(self, passwd, hash_contraseña,  salt):
        hash_input = hashlib.sha256((passwd + salt).encode()).hexdigest()
        return hash_input == hash_contraseña
        
