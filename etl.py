import os
import re
import pandas as pd


direccion = os.path.join('Assets', '_chat.txt')
patron_1 = '(?P<datetime>\d+/\d+/\d+ \d{2}:\d{2}) - (?P<sender>(.*?)): (?P<message>((.+\s+)?))'
patron_2 = '(?P<datetime>\[\d+\/\d+\/\d+ \d{2}:\d{2}:\d{2}\]) (?P<sender>(.*?)): (?P<message>((.+\s+)?))'

def comprueba_patron(cadena):
    if re.match(patron_1, cadena):
        return patron_1
    elif re.match(patron_2, cadena):
        return patron_2,

def empieza_con_fecha(cadena):
    resultado = re.match(comprueba_patron(cadena), cadena)
    if resultado:
        return True
    return False

lineas = []
with open(direccion, encoding="utf8") as archivo:
    for linea in archivo:
        #linea = linea.strip()
        if empieza_con_fecha(linea):
            resultado = re.findall(comprueba_patron(linea), linea[:-1])
            for columna in resultado:
                linea = [columna[0], columna[1], columna[3]]
                lineas.append(linea)
        else:
            resultado = linea.strip()
            #for columna in resultado:
            print(resultado)
            #print(lineas[0])



# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.html
df = pd.DataFrame(lineas, columns=['datetime', 'sender', 'message'])
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