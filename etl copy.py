import datetime
import re
import pandas as pd

patron = '(?P<datetime>\d+/\d+/\d+ \d{2}:\d{2}) - (?P<sender>(.*?)): (?P<message>((.+\s+)?))'
texto = """7/11/20 19:37 - AP: Que linda salis en tu foto de perfil❤️
asdasd
asdasdasdasd
asdasdasdasdasdads
7/11/20 20:26 - VB: Gracias mi amor
7/11/20 20:26 - VB: No pueden los chicos
7/11/20 20:29 - AP: Y tenes ganas de juntarte con alguien mas? Tipo la Juli ponele q la otra semana no se dii
7/11/20 21:11 - VB: Voy a tener q comprar mas
7/11/20 21:11 - AP: X?
7/11/20 21:12 - AP: Estoy yendo
7/11/20 21:13 - VB: Ok
8/11/20 01:27 - VB: <Multimedia omitido>"""
#resultado = re.search(patron, texto)
# print(resultado.group('date'))
# print(resultado.group('time'))
# print(resultado.group('sender'))
# print(resultado.group('message'))
# print(resultado.group())

# displaymatch(resultado)
resultado = re.findall(patron, texto)
# print(resultado)
""" for res in resultado:
    print(res[0])
    print(res[1])
    print(res[2])
    print(res[3])
    print(res[4])
    print(res[5])
    print(res[6]) """

lineas = []
linea = []
for res in resultado:
    linea = [res[0], res[1], res[3]]
    lineas.append(linea)

df = pd.DataFrame(lineas, columns=['datetime', 'sender', 'message'])
df['date'] = pd.to_datetime(df['datetime'])
df = df.drop(columns = ['datetime'])
df['hour'] = df['date'].dt.hour
df['minute'] = df['date'].dt.minute
