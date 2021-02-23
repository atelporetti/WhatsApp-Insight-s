import os
import re
import pandas as pd


direccion = os.path.join('Assets', '_chat.txt')

def reemplazar_caracteres_no_deseados(linea):
    return linea.strip().replace(u"\u202a", "").replace(u"\u200e", "").replace(u"\u202c", "").replace(u"\xa0", " ")

def es_comienzo_linea(linea):
        #El formato siempre es: <datetime><separator><contact/phone number>
        # (?P<datetime>(\[?)(((\d{1,2})(/|-)(\d{1,2})(/|-)(\d{2,4}))(,?\s)((\d{1,2})(:|\.)(\d{2})(\.|:)?(\d{2})?(\s?[apAP]\.?[mM]\.?)?))(\]?\s-?\s?))(?P<sender>(.*?))(:+\s?)(?P<message>(.+))
        patron = r"""
            (\[?)#Cero o Un corchete '['
            (?P<datetime>#Agrupo caracteres con el nombre 'datetime'
            (((\d{1,2})#1 a 2 digitos de dia
            (/|-)#'/' o '-' separador de dia 
            (\d{1,2})#1 a 2 digitos de mes
            (/|-)#'/' o '-' separador de mes
            (\d{2,4}))#2 a 4 digitos de año
            (,?\s)#Cero o Una coma ',' y un espacio en blanco
            ((\d{1,2})#Exactamente 1 a 2 digitos de hora
            (:|\.)#Separadores de Dos puntos ':' o punto '.'
            (\d{2})#2 digitos exactos para minutos
            (\.|:)?#Cero o Un punto '.' o dos puntos ':'
            (\d{2})?#Cero o Exactamente 2 digitos para segundos
            (\s?[apAP]\.?[mM]\.?)?)))#Cero o un caracter de ('espacio', 'A' or 'P', and 'M') para formato de AM/PM
            (\]?\s-?\s?)#Cero o Un corchete ']', Cero o Un (espacio y '-'), cero o Un espacio en blanco
            (?P<sender>#Agrupo caracteres con el nombre 'sender'
            (.*?))#Cero o mas caracteres (excepto \n) en forma lazy
            (:+\s?)#Uno o mas caracteres de dos puntos ':', cero o Un espacio en blacno
            (?P<message>#Agrupo caracteres con el nombre 'message'
            (.+))#Uno o mas caracteres (excepto \n) de mensajes
        """
        match = re.findall(re.compile(patron, re.VERBOSE), linea)
        if match:
            return match
        return

def lee_chat(dir):
    lineas = []
    try:
        with open(dir, encoding="utf8") as archivo:
            for linea in archivo:
                linea = reemplazar_caracteres_no_deseados(linea)
                resultado = es_comienzo_linea(linea)
                if resultado:
                    for columna in resultado:
                        linea = [columna[1], columna[18], columna[21]]
                        lineas.append(linea)
                #else:
                    #pass
                    #resultado = linea.strip()
                    # for columna in resultado:
                    # print(resultado)
                # print(lineas[0])
        return lineas
    except IOError as e:
        print(f"Archivo {direccion} no encontrado. Please recheck your file location")

# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.html
df = pd.DataFrame(lee_chat(direccion), columns=['datetime', 'sender', 'message'])
df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = df['datetime'].dt.date
df['time'] = df['datetime'].dt.time

print('---------------')
print(df.dtypes)
print('---------------')
print(df['datetime'])
print('---------------')
print(df['date'])
print('---------------')
print(df['time'])
print('---------------')
print(df['sender'])
print('---------------')
print(df['message'])
print('---------------')
print(df.head())
