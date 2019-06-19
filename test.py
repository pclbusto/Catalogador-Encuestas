lista_acentos = ["á","é","í","ó","ú"]
diccionario_vocales_sin_acentos={"á":"a","é":"e","í":"i","ó":"o","ú":"u"}

def sacar_acentos(cadena):
    for key in diccionario_vocales_sin_acentos:
        cadena =cadena.replace(key, diccionario_vocales_sin_acentos[key])
    return cadena


cadena = "esta1"
cadena_unicod = "ESTA"

print(cadena.lower()==cadena_unicod.lower())
# print(cadena_unicod)