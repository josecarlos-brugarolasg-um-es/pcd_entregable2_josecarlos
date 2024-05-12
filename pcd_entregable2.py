import random
import time
import functools
from math import sqrt
from abc import ABC, abstractmethod
import threading


'''R1: En primer lugar, debe de existir una única instancia del sistema que gestione 
todos los componentes y recursos del entorno IoT.  '''
# Para ello usamos el patrón de creación Singleton
class Sistema:
    _unicaInstancia = None

    def __init__(self):
        self.datos = []  # Almacena los datos de temperatura recibidos
        self.base_de_datos = {}  # Base de datos para almacenar los datos históricos de temperatura
        self.sensor_id = "Sensor_Temperatura"  # Identificador del sensor de temperatura
        self.observadores = []  # Almacena los observadores suscritos al sistema

    @classmethod
    def obtener_instancia(cls):
        '''Devuelve la única instancia del sistema'''
        if not cls._unicaInstancia:
            cls._unicaInstancia = cls()
        return cls._unicaInstancia
    
    def actualizar(self, dato):
        '''Actualiza los datos de temperatura, los almacena en la base de datos
        y notifica a los observadores.'''
        self.datos.append(dato)
        self.almacenar_en_base_de_datos(dato)
        self.notificar_observadores(dato)

    def visualizar_datos(self):
        '''Devuelve los datos de temperatura almacenados'''
        return self.datos

    def almacenar_en_base_de_datos(self, dato):
        '''Almacena el dato de temperatura junto con su timestamp en la base de datos'''
        timestamp = len(self.datos)  
        self.base_de_datos[timestamp] = {self.sensor_id: dato}

    def attach(self, observer):
        '''Suscribe un observador al sistema'''
        self.observadores.append(observer)

    def detach(self, observer):
        '''Desuscribe un observador del sistema'''
        self.observadores.remove(observer)

    def notificar_observadores(self, nueva_temperatura):
        '''Notifica a todos los observadores sobre la nueva temperatura'''
        for observador in self.observadores:
            observador.update(nueva_temperatura)


'''R2. El sistema notifica al sistema con un nuevo valor de temperatura cada 5 
segundos de forma que el sistema pueda recibir actualizaciones de datos en 
tiempo real y procesarlas adecuadamente.  . '''
# Para esto usamos el patrón de comportamiento Observer

class Observer(ABC):
    @abstractmethod
    def update(self, nueva_temperatura):
        '''Actualiza el observador con la nueva temperatura'''
        pass

class Temperatura:
    def __init__(self):
        self.observadores = []  # Almacena los observadores suscritos
        self.base_de_datos = {}  # Base de datos para almacenar los datos históricos de temperatura
        self.sensor_id = "Sensor_Temperatura"  # Identificador del sensor de temperatura

    def attach(self, observer):
        '''Suscribe un observador'''
        self.observadores.append(observer)

    def detach(self, observer):
        '''Desuscribe un observador'''
        self.observadores.remove(observer)

    def notify(self, nueva_temperatura):
        '''Notifica a todos los observadores sobre la nueva temperatura'''
        for observer in self.observadores:
            observer.update(nueva_temperatura)

    def simular_actualizaciones(self):
        '''Simula la recepción de actualizaciones de temperatura cada 5 segundos'''
        while True:
            nueva_temperatura = self.generar_temperatura_aleatoria()
            self.actualizar(nueva_temperatura)
            time.sleep(5)

    def generar_temperatura_aleatoria(self):
        '''Genera una temperatura aleatoria entre 0 y 100 grados Celsius'''
        return random.randint(0, 100)

    def actualizar(self, nueva_temperatura):
        '''Actualiza los datos de temperatura y notifica a los observadores'''
        self.almacenar_en_base_de_datos(nueva_temperatura)
        self.notify(nueva_temperatura)

    def almacenar_en_base_de_datos(self, dato):
        '''Almacena el dato de temperatura junto con su timestamp en la base de datos'''
        timestamp = int(time.time())
        self.base_de_datos[timestamp] = {self.sensor_id: dato}

class SistemaObserver(Observer):
    def update(self, nueva_temperatura):
        '''Actualiza el sistema con la nueva temperatura'''
        sistema = Sistema.obtener_instancia()
        sistema.actualizar(nueva_temperatura)


'''R3: Cada nuevo valor de temperatura recibido debe de implicar la realización de 
una serie de pasos encadenados. Dichos pasos son los siguientes: 
1. Calcular diferentes estadísticos de la temperatura (ej: media, desviación 
típica) durante los últimos 60 segundos.  
2. Luego, comprobar si la temperatura actual del invernadero está por 
encima de un umbral (dicho umbral puede fijarse por el estudiante). 
3. Finalmente, comprobar si durante los últimos 30 segundos la 
temperatura ha aumentado más de 10 grados centígrados.'''

# Para ello usamos el patrón de comportamiento Chain of Responsibility

class Handler:
    def __init__(self, successor=None):
        self.successor = successor

    def handle_request(self, request):
        '''Maneja la solicitud o pasa la solicitud al siguiente en la cadena'''
        pass

class SuperaUmbralHandler(Handler):
    def handle_request(self, request):
        '''Maneja la solicitud de comprobar si la temperatura supera el umbral'''
        if request.step == "SuperaUmbral":
            print("Comprobando si la temperatura supera el umbral...")
            if request.current_temperature > request.threshold:
                print("¡Alerta! La temperatura actual está por encima del umbral.")
        elif self.successor:
            self.successor.handle_request(request)

class AumentoBruscoHandler(Handler):
    def handle_request(self, request):
        '''Maneja la solicitud de comprobar si hay un aumento brusco de temperatura'''
        if request.step == "AumentoBrusco":
            print("Comprobando si hay un aumento brusco de temperatura...")
            if request.last_temperature_diff > request.aumento_brusco_threshold:
                print("Aumento brusco detectado en los últimos 30 segundos.")
        elif self.successor:
            self.successor.handle_request(request)

class Request:
    def __init__(self, step, temperatures=None, sensor_id=None, current_temperature=None, threshold=None, last_temperature_diff=None, aumento_brusco_threshold=None):
        self.step = step
        self.temperatures = temperatures
        self.sensor_id = sensor_id
        self.current_temperature = current_temperature
        self.threshold = threshold
        self.last_temperature_diff = last_temperature_diff
        self.aumento_brusco_threshold = aumento_brusco_threshold




'''R4: Para el primero de los pasos anteriores, se deberán tener diferentes 
estrategias para computar los estadísticos. Así una estrategia podrá centrarse 
calcular la media y desviación típica, otra estrategia podría centrarse en 
computar los cuantiles, y otra estrategia podría centrarse en computar los 
valores máximo y mínimo durante el periodo indicado (60 segundos). '''
# Para ello he usado el patrón de comportamiento Strategy

class Estrategia(ABC):
    def __init__(self, data, sensor_id):
        self.data = data
        self.sensor_id = sensor_id

    @abstractmethod
    def execute(self):
        '''Ejecuta la estrategia para calcular estadísticas de temperatura'''
        pass

class EstrategiaMedia(Estrategia):
    def execute(self):
        '''Calcula y muestra la media de los últimos 60 segundos'''
        last_60_seconds = list(self.data.values())[-12:]
        temperatures = [temp[self.sensor_id] for temp in last_60_seconds]
        mean = sum(temperatures) / len(temperatures)
        print(f"Media de los últimos 60 segundos: {mean}")

class EstrategiaDesviacion(Estrategia):
    def execute(self):
        '''Calcula y muestra la desviación estándar de los últimos 60 segundos'''
        last_60_seconds = list(self.data.values())[-12:]
        temperatures = [temp[self.sensor_id] for temp in last_60_seconds]
        mean = sum(temperatures) / len(temperatures)
        sd = sqrt(sum((x - mean) ** 2 for x in temperatures) / len(temperatures))
        print(f"Desviación estándar: {sd}")

class EstrategiaCuantiles(Estrategia):
    def execute(self):
        '''Calcula y muestra los cuantiles (25%, 50% y 75%) de los últimos 60 segundos'''
        last_60_seconds = list(self.data.values())[-12:]
        temperatures = [temp[self.sensor_id] for temp in last_60_seconds]
        quantiles = list(map(lambda q: round((len(temperatures) - 1) * q), [0.25, 0.5, 0.75]))
        quantiles_values = sorted(temperatures)[quantiles[0]], sorted(temperatures)[quantiles[1]], sorted(temperatures)[quantiles[2]]
        print(f"Cuantiles (25%, 50%, 75%): {quantiles_values}")

class EstrategiaMaxMin(Estrategia):
    def execute(self):
        '''Calcula y muestra el máximo y mínimo de los últimos 60 segundos'''
        last_60_seconds = list(self.data.values())[-12:]
        temperatures = [temp[self.sensor_id] for temp in last_60_seconds]
        max_min = functools.reduce(lambda acc, val: (max(acc[0], val), min(acc[1], val)), temperatures, (float('-inf'), float('inf')))
        print(f"Máximo y mínimo: {max_min}")





if __name__ == "__main__":
    temperatura = Temperatura()  

    sistema_observer = SistemaObserver()
    sistema = Sistema.obtener_instancia()
    sistema.attach(sistema_observer)

    temperatura_thread = threading.Thread(target=temperatura.simular_actualizaciones)
    temperatura_thread.daemon = True
    temperatura_thread.start()

    supera_umbral_handler = SuperaUmbralHandler()
    aumento_brusco_handler = AumentoBruscoHandler(supera_umbral_handler)

    print("\nEjemplo de operaciones encadenadas:")
    for i in range(5):
        input("\nPulsa Enter para recibir una nueva actualización de temperatura...")
        last_60_seconds = list(temperatura.base_de_datos.values())[-12:]
        temperatures = [temp[temperatura.sensor_id] for temp in last_60_seconds]

        estrategias = [
            EstrategiaMedia(data=temperatura.base_de_datos, sensor_id=temperatura.sensor_id),
            EstrategiaDesviacion(data=temperatura.base_de_datos, sensor_id=temperatura.sensor_id),
            EstrategiaCuantiles(data=temperatura.base_de_datos, sensor_id=temperatura.sensor_id),
            EstrategiaMaxMin(data=temperatura.base_de_datos, sensor_id=temperatura.sensor_id)
        ]

        for estrategia in estrategias:
            estrategia.execute()

        nueva_temperatura = random.randint(0, 100)
        request2 = Request(step="SuperaUmbral", current_temperature=nueva_temperatura, threshold=80)
        request3 = Request(step="AumentoBrusco", temperatures=temperatura.base_de_datos, sensor_id=temperatura.sensor_id, last_temperature_diff=random.randint(0, 20), aumento_brusco_threshold=10)

        supera_umbral_handler.handle_request(request2)
        aumento_brusco_handler.handle_request(request3)