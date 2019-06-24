from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import numpy as np

filtro = []

def azureml_main(dataframe1 = None, dataframe2 = None):
    # filtro = ['Falta de stock','Falta de orden y limpieza en tienda','Insatisfacción con los precios']
    filtro = data["Nivel 3"].unique()
    filtro_dic = {}
    for indice, label in enumerate(filtro):
        filtro_dic[label] = indice
        # {'Falta de stock':1, 'Falta de orden y limpieza en tienda':2, 'Insatisfacción con los precios':3}

    diccionario_vocales_sin_acentos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}
    data_filtrada = dataframe1[dataframe1["Nivel 3"].isin(filtro)]
    dimensiones = dataframe2
    dimensiones = dimensiones[dimensiones["clases"].isin(filtro)]
    print(dimensiones)
    lista_dimensiones = []
    lista_dimensiones.append("Idy")
    for label in dimensiones['texto'].values:
        for key in diccionario_vocales_sin_acentos:
            label = label.replace(key, diccionario_vocales_sin_acentos[key])
        label = label.lower()
        lista_dimensiones.append(label)
    vector = pd.DataFrame(data=None, index=None, columns=lista_dimensiones)
    arreglo2D = []
    target = []
    for index, comentario_cuota in enumerate(data_filtrada["Razón LTR"]):
        cadena = comentario_cuota
        for key in diccionario_vocales_sin_acentos:
            cadena = cadena.replace(key, diccionario_vocales_sin_acentos[key])
        comentario = cadena.lower()
        row = {}
        for label in lista_dimensiones:
            row[label] = 0
        # row["Idy"] = data_filtrada.iloc[index]["Idy"]
        for clave in row.keys():
            if clave in comentario:
                row[clave] += 1
        # row["Clase"] = filtro_dic[data_filtrada.iloc[index]["Nivel 3"]]
        target.append(filtro_dic[data_filtrada.iloc[index]["Nivel 3"]])
        lista = []
        for clave in row.keys():
            lista.append(row[clave])
        arreglo2D.append(lista)
    return arreglo2D,target


if __name__ == "__main__":
    data = pd.read_csv("Detractores todo los archivos.txt", sep='\t', header=0)
    dimensiones = pd.read_csv("lista de dimensiones.txt", sep='\t')
    # print(data["Nivel 3"].unique())
    vector,target = azureml_main(data, dimensiones)
    train_vector  = vector[:-500]
    train_target = target[:-500]
    vetor_pred = vector[-10:]
    # print(target[-10:])
    clf = MultinomialNB().fit(train_vector, train_target)
    predicted = clf.predict(vetor_pred)
    for indx, texto in enumerate(data["Razón LTR"].values[-10:]):
        print(predicted[indx])
        print(texto, "\n","CLASIFICACION: {}".format(filtro[predicted[indx]]))
    # print(predicted)
    # print(np.mean(predicted == target[-10:]))
    # print(target)
