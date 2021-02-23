import os, re
direccion = os.path.join('Assets', 'chat.txt')

def es_comienzo_linea(linea):
        #El formato siempre es: <datetime><separator><contact/phone number>
        #(?P<datetime>(\[?)(((\d{1,2})(/|-)(\d{1,2})(/|-)(\d{2,4}))(,?\s)((\d{1,2})(:|\.)(\d{2})(\.|:)?(\d{2})?(\s?[apAP]\.?[mM]\.?)?))(\]?\s-?\s?))(?P<sender>(.*?))(:+\s?)(?P<message>(.+))
        patron = r"""
            (\[?)#Cero o Un corchete '['
            (?P<datetime>#Agrupo caracteres con el nombre 'datetime'
            (((\d{1,2})#1 a 2 digitos de dia
            (\/|-)#'/' o '-' separador de dia 
            (\d{1,2})#1 a 2 digitos de mes
            (\/|-)#'/' o '-' separador de mes
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
        return None

resultado = es_comienzo_linea('‎[14/6/17 19:30:23] AP : ‎audio omitido')
print(resultado)
resultado_1 = es_comienzo_linea('7/11/20 10:04 - AP: Podrías enviarme el CBU?')
print(resultado_1)
