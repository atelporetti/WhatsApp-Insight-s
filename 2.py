import re
linea_u = 'ldfsadfskhladfkjldfs'
linea_a = '7/11/20 10:14 - AP: <Multimedia omitido>'
ubicacion = re.findall(':\s+(\wbicación)\s?:', linea_u)
archivo = re.findall(':\s.*\.\w{3,4}\s.*(documento omitido|archivo adjunto)', linea_a)

print(ubicacion)
print(type(ubicacion))
print(archivo)
print(type(archivo))