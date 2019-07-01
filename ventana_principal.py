import pandas as pd
import urllib.request
import json
import os
import ssl
import threading
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,
                             QAction, QFileDialog, QApplication)

import sys

lista_clasificaciones = []
cantidad_hilos = 0
MAX_CANTIDAD_HILOS = 2
porcenta_procesado = 0
cantidad_total_a_procesar = 0

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def clasificar_websv(texto, index):
    global cantidad_hilos, lista_clasificaciones, porcenta_procesado, cantidad_total_a_procesar
    while cantidad_hilos > MAX_CANTIDAD_HILOS:
        time.sleep(5)
    cantidad_hilos += 1
    print("index: {} texto: {}:".format(index,texto))


    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

    data = {
        "Inputs": {
              "input1":
              [
                  {
                          'Idy': "2",
                          'Fecha de Respuesta': "30/05/2018",
                          'Nombre Tienda': "Florida 1 (Florida N°343)",
                          'Nota de Recomendación': "1",
                          'Razón LTR': texto,
                          'Nivel 1': "Productos",
                          'Nivel 2': "Disponibilidad",
                          'Nivel 3': "Falta de stock",
                          'archivo': "detractores resto para compesandar",
                  },
              ],
        },
        "GlobalParameters":  {
        }
    }

    body = str.encode(json.dumps(data))

    url = 'http://40.117.32.126:80/api/v1/service/amlstudio-e1d56d8b31db4afd989268/score?api-version=2.0&format=swagger'
    api_key = 'mjhJU3p986WwGZYEdct6B4w6VXqQj8cv' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()
        # print(result)
        lista_clasificaciones[index] = result
        cantidad_hilos -= 1
        return result
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))

def hola():
    print("Hola")
    fname = QFileDialog.getOpenFileName(None, 'Open file', '/home')

app = QtWidgets.QApplication([])

win = uic.loadUi("ventana_principal.ui")
win.show()
win.boton_cargar_archivo.clicked.connect(hola)
# print(win.boton_cargar_archivo)
sys.exit(app.exec())
# archivo_para_catalogar = pd.read_csv("Detractores filtrado 3 clases.txt.tsv", sep='\t', header=0)
# lista_clasificaciones = [""]*len(archivo_para_catalogar["Razón LTR"].values)
# cantidad_total_a_procesar = len(lista_clasificaciones)

# for value in archivo_para_catalogar["Razón LTR"].values:
#     lista_clasificaciones.append("")
#
# for index, queja in enumerate(archivo_para_catalogar["Razón LTR"].values):
#     x = threading.Thread(target=clasificar_websv, args=(queja, index,))
#     # clasificar_websv(queja, index)
#     # print(index)
#     x.start()
# # print(archivo_para_catalogar["Razón LTR"].values)
# while cantidad_hilos>1:
#     time.sleep(5)
# print(lista_clasificaciones)


# text = "Quise comprar un celular, me dijeron que del color que buscaba no había. Pedí información sobre cuál color quedaba y elegí otro, porque neceistaba comprarlo en el momento. Hice toda la gestión, incluyendo el seguro, pero cuando fuí a retirar me dejaron esperando un rato y luego vinieron a decirme que no había más que el equipo que estaba en exhibición. No entiendo cómo venden algo que luego no tienen stock.Perdí más de 45 minutos, para irme con las manos vacías."
# opinion = clasificar_websv(text)
# print(len(archivo_para_catalogar))