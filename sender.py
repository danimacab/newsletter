import os
import csv
import smtplib
import argparse

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
from dotenv import load_dotenv



def send_email(sender_email, sender_password, receiver_emails, subject, html_content, images):
    # Configurar los parámetros del correo electrónico
    msg = MIMEMultipart('related')
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_emails)
    msg['Subject'] = subject

    # Crear la parte del mensaje HTML
    msg_alternative = MIMEMultipart('alternative')
    msg.attach(msg_alternative)
    
    # Adjuntar el contenido HTML al correo electrónico
    part = MIMEText(html_content, 'html')
    msg_alternative.attach(part)

    # Adjuntar las imágenes al correo electrónico
    '''for cid, image_path in images.items():
        with open(image_path, 'rb') as img:
            mime_image = MIMEImage(img.read())
            mime_image.add_header('Content-ID', f'<{cid}>')
            msg.attach(mime_image)'''

    # Conectar al servidor SMTP y enviar el correo electrónico
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Ejemplo con Gmail, ajusta según tu proveedor
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_emails, msg.as_string())
        print('Correo electrónico enviado correctamente a la siguiente lista de destinatarixs:')
        print(receiver_emails)
    except Exception as e:
        print(f'Error al enviar el correo electrónico: {e}')
    finally:
        server.quit()

def obtenerDestinatarios(csv_file):
    destinatarios = []
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            destinatarios.append(row['email'])
    return destinatarios

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enviar un correo electrónico.')
    parser.add_argument('credencial', help='Ruta al archivo de credenciales .env')
    parser.add_argument('destinatarios', help='Ruta al archivo CSV con los destinatarios')
    parser.add_argument('contenido', help='Ruta al archivo HTML con el contenido')
    parser.add_argument('asunto', help='Asunto del correo')
    
    args = parser.parse_args()
    # Cargar las variables de entorno desde el archivo .env especificado
    load_dotenv(args.credencial)

    email_user = os.getenv('EMAIL_USER')
    email_pass = os.getenv('EMAIL_PASS')


    # Configurar los parámetros del correo electrónico

    sender_email = email_user
    sender_password = email_pass
    #receiver_emails = ["marti.pernigotti@gmail.com","lucianaruizdiaz97@gmail.com","danielamacab@gmail.com","a_s_alberti@hotmail.com","adnebreda@hotmail.com","lucreciasilva@hotmail.com.ar","dellorobohe@gmail.com","lorenaaicardo1@gmail.com","gloriaprim9@gmail.com","lmennag@gmail.com","jurudiz@gmail.com"]
    receiver_emails = obtenerDestinatarios(args.destinatarios)
    subject = args.asunto

    # Leer el contenido del archivo HTML
    with open(args.contenido, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Diccionario de imágenes con su Content-ID y la ruta correspondiente
    images = {
        'logo-comision': 'mail-plantilla/images/logo-comision.jpg',
        'logo-fakko': 'mail-plantilla/images/logo-fakko.png',
        'ig-icon': 'mail-plantilla/images/ig-icon.png',
        'fb-icon': 'mail-plantilla/images/fb-icon.png'
    }

    # Llamar a la función para enviar el correo electrónico
    send_email(sender_email, sender_password, receiver_emails, subject, html_content, images)

