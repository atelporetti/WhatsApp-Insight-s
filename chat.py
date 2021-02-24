import os, re
import pandas as pd
import matplotlib.pyplot as plt

class Chat():

    def __init__(self, ubicacion):
        self.__ubicacion = ubicacion
        self.__palabras = 0
        self.__mjs_multimedia = 0
        self.__participantes = []
        self.__emojis = 0
        self.__DataFrame = pd.DataFrame(columns=['datetime', 'sender', 'message'])
    
    def get_ubicacion(self):
        return self.__ubicacion
    
    def set_ubicacion(self, ubicacion):
        self.__ubicacion = ubicacion   

    def get_palabras(self):
        return self.__palabras
    
    def set_palabras(self, palabras):
        self.__palabras = palabras   

    def get_multimedia(self):
        return self.__mjs_multimedia
    
    def set_multimedia(self, multimedia):
        self.__mjs_multimedia = multimedia   

    def get_participantes(self):
        return self.__participantes
    
    def set_participantes(self, participantes):
        self.__participantes = participantes   

    def get_emojis(self):
        return self.__emojis
    
    def set_emojis(self, emojis):
        self.__emojis = emojis
        
    def get_DataFrame(self):
        return self.__DataFrame
    
    def set_DataFrame(self, DataFrame):
        self.__DataFrame = DataFrame  

    def __reemplazar_caracteres_no_deseados(self, linea):
        return linea.strip().replace(u"\u202a", "").replace(u"\u200e", "").replace(u"\u202c", "").replace(u"\xa0", " ")

    def __es_comienzo_linea(self, linea):
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
    
    def __es_continuacion_mensaje(self, linea):
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

    def __es_msj_multimedia(linea):
        # Se filtran los siguientes eventos
        # Usuario que se une al grupo
        # Usuario que abandona el grupo
        # Añadir un miembro del grupo
        # Eliminación de un miembro del grupo
        # Cambio de código de seguridad
        # Cambio de número de teléfono
        tipos = ['‎imagen omitida',
                'audio omitido',
                'video omitido',
                'Tarjeta de contacto omitida',
                '<Multimedia omitido>',
                re.findall('(:\s.+bicación:)', linea), # Para ubicaciones omitidas
                re.findall('(:\s)(.*\.\w{3,4}\s)', linea)] # Para archivos omitidos
        if linea in tipos:
            return True
        return

    def lee_chat(self):
        lineas = []
        try:
            with open(self.get_ubicacion(), encoding="utf8") as archivo:
                for linea in archivo:
                    linea = self.__reemplazar_caracteres_no_deseados(linea)
                    resultado = self.__es_comienzo_linea(linea)
                    if resultado:
                        for columna in resultado:
                            linea = [columna[1], columna[18], columna[21]]
                            lineas.append(linea)
                    else:
                        # Agrega la continuacion del mensaje a la linea anterior
                        if len(lineas) > 0 and self.__es_continuacion_mensaje(linea):
                            lineas[-1][2] += (' ' + linea)
            
            self.__guarda_DataFrame(lineas)
        except IOError as e:
            print(
                f"Archivo {self.get_ubicacion()} no encontrado. Please recheck your file location")

    def __guarda_DataFrame(self, datos):
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DatetimeIndex.html
        self.set_DataFrame(pd.DataFrame(datos, columns=['datetime', 'sender', 'message']))
        self.get_DataFrame()['datetime'] = pd.to_datetime(self.get_DataFrame()['datetime'])
        self.get_DataFrame()['date'] = self.get_DataFrame()['datetime'].dt.date
        self.get_DataFrame()['time'] = self.get_DataFrame()['datetime'].dt.time

        """ print('---------------')
        print(self.get_DataFrame().dtypes) """
        print(self.get_DataFrame().head(5))
        print(self.get_DataFrame().tail(5))

    def muestra_datos(self):
        # Create new fields to use in heatmap
        self.get_DataFrame()['dia_semana'] = self.get_DataFrame()['datetime'].dt.dayofweek + 1
        self.get_DataFrame()['hora'] = self.get_DataFrame()['datetime'].dt.hour

        # Create new Dataframe containing self.get_DataFrame() counts
        heatmap_data = self.get_DataFrame().groupby(['dia_semana', 'hora']).size()
        heatmap_data = heatmap_data.unstack()

        # Create heatmap
        plt.pcolor(heatmap_data, cmap='Blues')
        plt.xlabel("Hour of Day")
        plt.ylabel("Day of Week")
        plt.colorbar()
        plt.show()

direccion = os.path.join('Assets', 'chat_1linea.txt')
chat = Chat(direccion)
chat.lee_chat()
#chat.guarda_DataFrame()
chat.muestra_datos()
