import os, re
direccion = os.path.join('Assets', 'chat.txt')

def es_comienzo_linea(linea):
        #El formato siempre es: <datetime><separator><contact/phone number>
        #(?P<datetime>(\[?)(((\d{1,2})(\/|-)(\d{1,2})(\/|-)(\d{2,4}))(,?\s)((\d{1,2})(:|\.)(\d{2})(\.|:)?(\d{2})?(\s?[apAP]\.?[mM]\.?)?))(\]?\s-?\s?))(?P<sender>(.*?))(:+\s?)(?P<message>(.+))
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
resultado_1 = es_comienzo_linea('7/11/20 10:02 - Los mensajes y las llamadas están cifrados de extremo a extremo. Nadie fuera de este chat, ni siquiera WhatsApp, puede leerlos ni escucharlos. Toca para obtener más información.')
print(resultado_1)
resultado_2 = es_comienzo_linea('7/11/20 10:14 - AP: <Multimedia omitido>')
print(resultado_2)

def is_event(body=""):
        """Detect wether the body of chat is event log.
        If the body if an event, it won't be count and the body of the message will not analized
        Event log means note of event.
        Below are known event log patterns in difference language
        - Group created
        - User joining group
        - User left group
        - Adding group member
        - Removing group member
        - Security code changed
        - Phone number changed
        -
        Feel free to add similar pattern for other known pattern or language
        Keyword arguments:
        body -- body of exported chat
        The Rule is:
        Match the known event message
        """
        pattern_event = [
            # Welcoming message
            r"Messages to this group are now secured with end-to-end encryption\.$",  # EN
            # User created group
            r".+\screated this group$",  # EN
            # User left group
            r".+\sleft$",  # EN
            # User join group via inviation link
            r".+\sjoined using this group's invite link$",  # EN
            # Admin adds member
            r".+\sadded\s.+",  # EN
            # Admin removes member
            r".+\sremoved\s.+",  # EN
            # Member's security code changed
            r".+'s security code changed\.$",  # EN
            # Member changes phone number
            r".*changed their phone number to a new number. Tap to message or add the new number\.$"  # EN
        ]

        for p in pattern_event:
            match = re.match(p, body)
            if match:
                return match
        return None
    
resultado = is_event('‎[14/6/17 19:30:23] AP : ‎audio omitido')
print(resultado)
resultado_1 = is_event('7/11/20 10:02 - Los mensajes y las llamadas están cifrados de extremo a extremo. Nadie fuera de este chat, ni siquiera WhatsApp, puede leerlos ni escucharlos. Toca para obtener más información.')
print(resultado_1)
resultado_2 = is_event('7/11/20 10:14 - AP: <Multimedia omitido>')
print(resultado_2)