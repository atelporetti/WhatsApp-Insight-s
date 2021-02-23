import os
import re
import pandas as pd


direccion = os.path.join('Assets', 'chat.txt')

def es_comienzo_linea(linea):
        #El formato siempre es: <datetime><separator><contact/phone number>
        # (?P<datetime>(\[?)(((\d{1,2})(/|-)(\d{1,2})(/|-)(\d{2,4}))(,?\s)((\d{1,2})(:|\.)(\d{2})(\.|:)?(\d{2})?(\s?[apAP]\.?[mM]\.?)?))(\]?\s-?\s?))(?P<sender>(.*?))(:+\s?)(?P<message>(.+))
        patron = r"""
            (?P<datetime>#Agrupo caracteres con el nombre 'datetime'
            (\[?)       #Cero o Un corchete '['
            (((\d{1,2}) #1 a 2 digitos de dia
            (/|-)       #'/' o '-' separador de dia 
            (\d{1,2})   #1 a 2 digitos de mes
            (/|-)       #'/' o '-' separador de mes
            (\d{2,4}))  #2 a 4 digitos de año
            (,?\s)      #Cero o Una coma ',' y un espacio en blanco
            ((\d{1,2})  #Exactamente 1 a 2 digitos de hora
            (:|\.)      #Separadores de Dos puntos ':' o punto '.'
            (\d{2})     #2 digitos exactos para minutos
            (\.|:)?     #Cero o Un punto '.' o dos puntos ':'
            (\d{2})?    #Cero o Exactamente 2 digitos para segundos
            (\s?[apAP]\.?[mM]\.?)?))  #Cero o un caracter de ('espacio', 'A' or 'P', and 'M') para formato de AM/PM
            (\]?\s-?\s?))#Cero o Un corchete ']', Cero o Un (espacio y '-'), cero o Un espacio en blanco
            (?P<sender> #Agrupo caracteres con el nombre 'sender'
            (.*?))      #Cero o mas caracteres (excepto \n) en forma lazy
            (:+\s?)      #Uno o mas caracteres de dos puntos ':', cero o Un espacio en blacno
            (?P<message>#Agrupo caracteres con el nombre 'message'
            (.+))       #Uno o mas caracteres (excepto \n) de mensajes
        """
        match = re.match(re.compile(patron, re.VERBOSE), linea)
        if match:
            return match
        return None



""" def comprueba_patron(cadena):
    if re.match(patron_1, cadena):
        return patron_1
    elif re.match(patron_2, cadena):
        return patron_2,
    else:
        return patron_vacio


def empieza_con_fecha(cadena):
    if re.match(patron_1, cadena):
        return re.match(patron_1, cadena)
    elif re.match(patron_2, cadena):
        return re.match(patron_2, cadena)
    else:
        return re.match(patron_vacio, cadena) """


def lee_chat(dir):
    lineas = []
    try:
        with open(dir, encoding="utf8") as archivo:
            for linea in archivo:
                #linea.replace('[', '').replace(']', '')
                resultado = es_comienzo_linea(linea)
                for columna in resultado:
                    linea = [columna[0].strip('[').strip(']'), columna[1], columna[3]]
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
