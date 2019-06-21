import pandas as pd

#Poca cantidad de cuotas1
#Falta amabilidad y actitud de servicio del colaborador
#Fila extensa para acceder al probador


# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# imports up here can be used to
import pandas as pd



def azureml_main(dataframe1 = None, dataframe2 = None):
    filtro = ['Falta de stock','Falta de orden y limpieza en tienda','Insatisfacción con los precios']
    diccionario_vocales_sin_acentos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}
    data_filtrada = dataframe1[dataframe1["Nivel 3"].isin(filtro)]
    dimensiones = dataframe2
    dimensiones = dimensiones[dimensiones["clases"].isin(filtro)]
    lista_dimensiones = []
    lista_dimensiones.append("Idy")
    for label in dimensiones['texto'].values:
        for key in diccionario_vocales_sin_acentos:
            label = label.replace(key, diccionario_vocales_sin_acentos[key])
        label = label.lower()
        lista_dimensiones.append(label)
    vector = pd.DataFrame(data=None, index=None, columns=lista_dimensiones)
    for index, comentario_cuota in enumerate(data_filtrada["Razón LTR"]):
        cadena = comentario_cuota
        for key in diccionario_vocales_sin_acentos:
            cadena = cadena.replace(key, diccionario_vocales_sin_acentos[key])
        comentario = cadena.lower()
        row = {}
        for label in lista_dimensiones:
            row[label] = 0
        row["Idy"] = data_filtrada.iloc[index]["Idy"]
        for clave in row.keys():
            if clave in comentario:
                row[clave] += 1
        vector = vector.append(row, ignore_index=True)
    vector_join = vector.merge(data_filtrada, on=["Idy"], how='inner')
    print(lista_dimensiones)
    #return vector_join, dataframe2,
    return vector_join


if __name__ == "__main__":
    filtro = ['Falta de stock','Falta de orden y limpieza en tienda','Insatisfacción con los precios']
    data = pd.read_csv("Detractores todo los archivos.txt", sep='\t', header=0)
    data_filtrada = data[data["Nivel 3"].isin(filtro)]
    # data_filtrada = data
    dimensiones = pd.read_csv("lista de dimensiones.txt", sep='\t')
    dimensiones = dimensiones[dimensiones["clases"].isin(filtro)]
    print(dimensiones.values)
    #
    # lista = []
    # for valor in dimensiones["texto"]:
    #     if valor in lista:
    #         print("duplicado {}".format(valor))
    #     else:
    #         lista.append(valor)


    #
    # vect, dimen = azureml_main(data_filtrada, dimensiones)
    # print(dimensiones.values)