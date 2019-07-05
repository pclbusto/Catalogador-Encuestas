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
import json

lista_clasificaciones = []
cantidad_hilos = 0
MAX_CANTIDAD_HILOS = 1
cantidad_procesados = 0
cantidad_total_a_procesar = 0
procesando = True
archivo_para_catalogar = None

def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context

def clasificar_websv(lista_texto):
    global cantidad_hilos, lista_clasificaciones, cantidad_procesados, cantidad_total_a_procesar
    while cantidad_hilos > MAX_CANTIDAD_HILOS:
        time.sleep(5)
    cantidad_hilos += 1
    # print("index: {} texto: {}:".format(lista_texto))
    cantidad_procesados += 1

    allowSelfSignedHttps(True) # this line is needed if you use self-signed certificate in your scoring service.

    data = {
        "Inputs": {
              "input1":
              [
                  # {
                  #         'Idy': "2",
                  #         'Fecha de Respuesta': "30/05/2018",
                  #         'Nombre Tienda': "Florida 1 (Florida N°343)",
                  #         'Nota de Recomendación': "1",
                  #         'Razón LTR': "falta stock",
                  #         'Nivel 1': "Productos",
                  #         'Nivel 2': "Disponibilidad",
                  #         'Nivel 3': "Falta de stock",
                  #         'archivo': "detractores resto para compesandar",
                  # },
                  # {
                  #     'Idy': "2",
                  #     'Fecha de Respuesta': "30/05/2018",
                  #     'Nombre Tienda': "Florida 1 (Florida N°343)",
                  #     'Nota de Recomendación': "1",
                  #     'Razón LTR': "todo estaba desordenado",
                  #     'Nivel 1': "Productos",
                  #     'Nivel 2': "Disponibilidad",
                  #     'Nivel 3': "Falta de stock",
                  #     'archivo': "detractores resto para compesandar",
                  # }
              ],
        },
        "GlobalParameters":  {
        }
    }
    # print("lista:{}".format(len(lista_texto)))
    for index, texto in enumerate(lista_texto):
        data["Inputs"]["input1"].append({
                          'Idy': "{}".format(index),
                          'Fecha de Respuesta': "",
                          'Nombre Tienda': "",
                          'Nota de Recomendación': "0",
                          'Razón LTR': texto,
                          'Nivel 1': "",
                          'Nivel 2': "",
                          'Nivel 3': "",
                          'archivo': "",
                  })
    print(data)
    body = str.encode(json.dumps(data))
    #
    url = 'http://40.117.32.126:80/api/v1/service/amlstudio-e1d56d8b31db4afd989268/score?api-version=2.0&format=swagger'
    api_key = 'mjhJU3p986WwGZYEdct6B4w6VXqQj8cv' # Replace this with the API key for the web service
    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read()

        print(result.decode('unicode_escape'))
        son = json.loads(result.decode('unicode_escape'))
        print(len(son["Results"]["output1"]))
        print(len(lista_clasificaciones))

        for index, resultados in enumerate(son["Results"]["output1"]):
            lista_clasificaciones[index]=resultados["items"]["output1Item"]["Scored Labels"]

    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))
        lista_clasificaciones[index] = "No se pudo clasificar"
    # except:
    #     lista_clasificaciones[index] = "No se pudo clasificar"
    # win.progressBar.setValue(100*(cantidad_procesados/cantidad_total_a_procesar))
    win.progressBar.setValue(100)

    global archivo_para_catalogar
    archivo_para_catalogar["Nivel 3"] = lista_clasificaciones
    archivo_para_catalogar.to_csv(sep='\t',
                                  path_or_buf="C:\\Users\\pedro\\PycharmProjects\\Clasificador encuentas Gui\\salida.tsv",
                                  encoding='utf-8')
    print("Archivo Guardado")
def boton_cargar_archivo_click():
    global cantidad_total_a_procesar, lista_clasificaciones, archivo_para_catalogar, win
    fname = QFileDialog.getOpenFileName(None, 'Open file', 'C:\\Users\\pedro\\PycharmProjects\\Clasificador encuentas Gui')
    # fname ='C:\\Users\\pedro\\PycharmProjects\\Clasificador encuentas Gui\\Detractores filtrado 3 clases.txt.tsv'
    print(fname[0])
    # print(fname)
    # archivo_para_catalogar = pd.read_csv(fname, sep='\t', header=0)
    archivo_para_catalogar = pd.read_csv(fname[0], sep='\t', header=0)
    win.label.setText(fname[0])
    # win.label.setText(fname)
    lista_clasificaciones = [""]*len(archivo_para_catalogar["Razón LTR"].values)
    cantidad_total_a_procesar = len(lista_clasificaciones)

def guardar_archivo():
    global  archivo_para_catalogar
    while cantidad_procesados<cantidad_total_a_procesar:
        time.sleep(5)
    archivo_para_catalogar["Nivel 3"]=lista_clasificaciones
    archivo_para_catalogar.to_csv(sep='\t',path_or_buf="C:\\Users\\pedro\\PycharmProjects\\Clasificador encuentas Gui\\salida.tsv",encoding = 'utf-8')
    print("Archivo Guardado")

def proceso_clasificacion():
    global lista_clasificaciones, archivo_para_catalogar
    # for index, queja in enumerate(archivo_para_catalogar["Razón LTR"].values):
    threading.Thread(target=clasificar_websv, args=(archivo_para_catalogar["Razón LTR"].values,)).start()
    threading.Thread(target=guardar_archivo).start()

#
# def download():
#     global win
#     completed = 0
#     while completed < 100:
#         completed += 0.0001
#         win.progressBar.setValue(completed)

app = QtWidgets.QApplication([])

win = uic.loadUi("ventana_principal.ui")
win.show()
win.boton_cargar_archivo.clicked.connect(boton_cargar_archivo_click)
win.boton_clasificar.clicked.connect(proceso_clasificacion)
# boton_cargar_archivo_click()
# proceso_clasificacion()
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