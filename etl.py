import os
import re
import pandas as pd

patron = '(?P<datetime>\d+/\d+/\d+ \d{2}:\d{2}) - (?P<sender>(.*?)): (?P<message>((.+\s+)?))'
direccion = os.path.join('Assets', 'chat.txt')

lineas = []
with open(direccion, encoding="utf8") as archivo:
    for linea in archivo:
        resultado = re.findall(patron, linea)
        for columna in resultado:
            linea = [columna[0], columna[1], columna[3]]
            lineas.append(linea)

df = pd.DataFrame(lineas, columns=['datetime', 'sender', 'message'])
df['date'] = pd.to_datetime(df['datetime'])
df = df.drop(columns=['datetime'])
df['hour'] = df['date'].dt.hour
df['minute'] = df['date'].dt.minute
print('---------------')
print(df.dtypes)
print('---------------')
print(df['date'])
