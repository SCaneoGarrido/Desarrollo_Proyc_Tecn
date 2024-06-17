import secrets
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv #type: ignore


class autenticacion:
    def __init__(self) -> None:
        pass
  
    def generar_token():
        try:
            token2fa = secrets.token_bytes(16)
            if token2fa:
                print("Token generado")
                print(token2fa)
                return token2fa.hex()  # Convertir bytes a representación hexadecimal
            else:
                return None
        except Exception as e:
            print(f"Error al generar token de autenticacion: ", e)


    def enviar_token(token, destinatario):
        load_dotenv()
        remitente = os.getenv('CORREO_EMISOR')
        destinatario = destinatario
        asunto = 'test token para municipalidad'

        msg = MIMEMultipart()
        msg['Subject'] = asunto
        msg['From'] = remitente
        msg['To'] = destinatario

        # Leer el contenido HTML del archivo email.html
        with open('Backend/Public/email.html', 'r') as archivo:
            html = archivo.read()

        # Reemplazar el marcador de posición {{TOKEN}} con el token generado
        html_con_token = html.replace('{{TOKEN}}', token)

        # Adjuntar el contenido HTML al mensaje
        msg.attach(MIMEText(html_con_token, 'html'))

        # Iniciar conexión con el servidor SMTP de Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, os.getenv('PASS'))

        # Enviar correo electrónico
        server.sendmail(remitente, destinatario, msg.as_string())
        server.quit()


    def validarToken():
        pass

 
