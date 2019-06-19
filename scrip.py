import pandas as pd

#Poca cantidad de cuotas1
#Falta amabilidad y actitud de servicio del colaborador
#Fila extensa para acceder al probador


# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# imports up here can be used to
import pandas as pd



def azureml_main(dataframe1 = None, dataframe2 = None):
    diccionario_vocales_sin_acentos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u"}
    data_filtrada = dataframe1
    lista_dimensiones = []
    lista_dimensiones.append("Idy")
    for label in dataframe2['texto'].values:
        # for key in diccionario_vocales_sin_acentos:
        #     label = label.replace(key, diccionario_vocales_sin_acentos[key])
        label = label.lower()
        lista_dimensiones.append(label)

    vector = pd.DataFrame(data=None, index=None, columns=lista_dimensiones)
    for index, comentario_cuota in enumerate(data_filtrada["Razón LTR"]):
        # cadena = comentario_cuota
        # for key in diccionario_vocales_sin_acentos:
        #     cadena = cadena.replace(key, diccionario_vocales_sin_acentos[key])
        comentario = comentario_cuota.lower()
        row = {}
        for label in lista_dimensiones:
            row[label] = 0
        row["Idy"] = data_filtrada.iloc[index]["Idy"]
        for clave in row.keys():
            if clave in comentario:
                row[clave] += 1
        vector = vector.append(row, ignore_index=True)
        # print(row)
    vector_join = vector.merge(data_filtrada, on=["Idy"], how='inner')
    return vector_join, dataframe2,


if __name__ == "__main__":
    data = pd.read_csv("Detractores todo los archivos.txt", sep='\t', header=0)
    # data_filtrada = data[data["Nivel 3"].isin(['Fila extensa para acceder al probador','Falta amabilidad y actitud de servicio del colaborador','Fila extensa para acceder al probador'])]
    data_filtrada = data
    dimensiones = pd.read_csv("lista de dimensiones.txt", sep='\t')
    vect, dimen = azureml_main(data_filtrada, dimensiones)
    # print(vect.values)