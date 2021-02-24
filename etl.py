#!/usr/bin/env python
import os
import re
import pandas as pd
import matplotlib.pyplot as plt

direccion = os.path.join('Assets', 'chat.txt')


def reemplazar_caracteres_no_deseados(linea):
    return linea.strip().replace(u"\u202a", "").replace(u"\u200e", "").replace(u"\u202c", "").replace(u"\xa0", " ")


def es_comienzo_linea(linea):
    # El formato siempre es: <datetime><separator><contact/phone number>
    # (?P<datetime>(\[?)(((\d{1,2})(\/|-)(\d{1,2})(\/|-)(\d{2,4}))(,?\s)((\d{1,2})(:|\.)(\d{2})(\.|:)?(\d{2})?(\s?[apAP]\.?[mM]\.?)?))(\]?\s-?\s?))(?P<sender>(.*?))(:+\s?)(?P<message>(.+))
    patron = r"""
            (\[?)           #Cero o Un corchete '['
            (?P<datetime>   #Agrupo caracteres con el nombre 'datetime'
            (((\d{1,2})     #1 a 2 digitos de dia
            (/|-)           #'/' o '-' separador de dia 
            (\d{1,2})       #1 a 2 digitos de mes
            (/|-)           #'/' o '-' separador de mes
            (\d{2,4}))      #2 a 4 digitos de año
            (,?\s)          #Cero o Una coma ',' y un espacio en blanco
            ((\d{1,2})      #Exactamente 1 a 2 digitos de hora
            (:|\.)          #Separadores de Dos puntos ':' o punto '.'
            (\d{2})         #2 digitos exactos para minutos
            (\.|:)?         #Cero o Un punto '.' o dos puntos ':'
            (\d{2})?        #Cero o Exactamente 2 digitos para segundos
            (\s?[apAP]\.?[mM]\.?)?)))#Cero o un caracter de ('espacio', 'A' or 'P', and 'M') para formato de AM/PM
            (\]?\s-?\s?)    #Cero o Un corchete ']', Cero o Un (espacio y '-'), cero o Un espacio en blanco
            (?P<sender>     #Agrupo caracteres con el nombre 'sender'
            (.*?))          #Cero o mas caracteres (excepto \n) en forma lazy
            (:+\s?)         #Uno o mas caracteres de dos puntos ':', cero o Un espacio en blacno
            (?P<message>    #Agrupo caracteres con el nombre 'message'
            (.+))           #Uno o mas caracteres (excepto \n) de mensajes
        """
    match = re.findall(re.compile(patron, re.VERBOSE), linea)
    if match:
        return match
    return

def es_continuacion_mensaje(linea):
    # Si tiene fecha entonces no puede ser la continuacion de un mensaje anterior
    # (\[?)(((\d{1,2})(\/|-)(\d{1,2})(\/|-)(\d{2,4}))(,?\s)((\d{1,2})(:|\.)(\d{2})(\.|:)?(\d{2})?(\s?[apAP]\.?[mM]\.?)?))(\]?)
    patron = r"""
            (\[?)           #Cero o Un corchete '['
            (((\d{1,2})     #1 a 2 digitos de dia
            (/|-)           #'/' o '-' separador de dia 
            (\d{1,2})       #1 a 2 digitos de mes
            (/|-)           #'/' o '-' separador de mes
            (\d{2,4}))      #2 a 4 digitos de año
            (,?\s)          #Cero o Una coma ',' y un espacio en blanco
            ((\d{1,2})      #Exactamente 1 a 2 digitos de hora
            (:|\.)          #Separadores de Dos puntos ':' o punto '.'
            (\d{2})         #2 digitos exactos para minutos
            (\.|:)?         #Cero o Un punto '.' o dos puntos ':'
            (\d{2})?        #Cero o Exactamente 2 digitos para segundos
            (\s?[apAP]\.?[mM]\.?)?))#Cero o un caracter de ('espacio', 'A' or 'P', and 'M') para formato de AM/PM
            (\]?)    #Cero o Un corchete ']'
    """
    match = re.match(re.compile(patron, re.VERBOSE), linea)
    if match:
        return False
    return True

def es_evento():
    # Se filtran los siguientes eventos
    # Usuario que se une al grupo
    # Usuario que abandona el grupo
    # Añadir un miembro del grupo
    # Eliminación de un miembro del grupo
    # Cambio de código de seguridad
    # Cambio de número de teléfono
    pass


def lee_chat(dir):
    lineas = []
    try:
        with open(dir, encoding="utf8") as archivo:
            for linea in archivo:
                linea = reemplazar_caracteres_no_deseados(linea)
                resultado = es_comienzo_linea(linea)
                #if resultado and linea:
                    #print('hola')
                if resultado:
                    for columna in resultado:
                        linea = [columna[1], columna[18], columna[21]]
                        lineas.append(linea)
                else:
                    # Agrega la continuacion del mensaje a la linea anterior
                    if len(lineas) > 0 and es_continuacion_mensaje(linea):
                        lineas[-1][2] += (' ' + linea)
        return lineas
    except IOError as e:
        print(
            f"Archivo {direccion} no encontrado. Please recheck your file location")


# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.html
df = pd.DataFrame(lee_chat(direccion), columns=['datetime', 'sender', 'message'])
df['datetime'] = pd.to_datetime(df['datetime'])
df['date'] = df['datetime'].dt.date
df['time'] = df['datetime'].dt.time

""" print('---------------')
print(df.dtypes) """
print(df.head(5))
print(df.tail(5))

# Create new fields to use in heatmap
df['dia_semana'] = df['datetime'].dt.dayofweek + 1
df['hora'] = df['datetime'].dt.hour

# Create new Dataframe containing df counts
heatmap_data = df.groupby(['dia_semana', 'hora']).size()
heatmap_data = heatmap_data.unstack()

# Create heatmap
plt.pcolor(heatmap_data, cmap='Blues')
plt.xlabel("Hour of Day")
plt.ylabel("Day of Week")
plt.colorbar()
plt.show()