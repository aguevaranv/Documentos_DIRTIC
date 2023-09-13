from smtplib import SMTP

# Establecemos conexion con el servidor smtp de gmail
mailServer = SMTP('10.128.39.214',25)
mailServer.ehlo()
mailServer.starttls()
mailServer.ehlo()
mailServer.login("aguevarac@armada.mil.ec","Guevara.2023")

print (mailServer.ehlo())

