
# The script MUST contain a function named azureml_main
# which is the entry point for this module.

# imports up here can be used to
import pandas as pd

# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame1
def azureml_main(data=None, dimensiones=None):
    data_filtrada = data[data["Nivel 3"].isin(
        ['Falta de stock',
            'Poca cantidad de cuotas',
         'Fila extensa para acceder al probador'])]
    lista_dimensiones = []
    lista_dimensiones.append("Idy")
    for label in dimensiones['texto'].values:
        lista_dimensiones.append(label)

    vector = pd.DataFrame(data=None, index=None, columns=lista_dimensiones)

    for index, comentario_cuota in enumerate(data_filtrada["Razón LTR"]):
        # print(comentario_cuota)
        row = {}
        for label in lista_dimensiones:
            row[label] = 0

        row["Idy"] = data_filtrada.iloc[index]["Idy"]
        for clave in row.keys():
            if clave in comentario_cuota:
                row[clave] += 1
        vector = vector.append(row, ignore_index=True)
    vector_join = vector.merge(data_filtrada, on=["Idy"], how='inner')
    return vector_join, dimensiones,

