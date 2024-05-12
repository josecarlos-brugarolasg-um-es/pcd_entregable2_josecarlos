import pytest
from pcd_entregable2 import *


# Importamos las clases y funciones del código principal aquí

# Prueba para la generación de temperatura aleatoria
def test_generar_temperatura_aleatoria():
    temperatura = Temperatura()
    temp = temperatura.generar_temperatura_aleatoria()
    assert 0 <= temp <= 100, "La temperatura generada está fuera del rango esperado"

# Probamos para el acceso a la base de datos de temperatura
def test_almacenar_en_base_de_datos():
    sistema = Sistema.obtener_instancia()
    sistema.almacenar_en_base_de_datos(25)  # Almacenar una temperatura en la base de datos
    assert len(sistema.base_de_datos) == 1, "Error al almacenar en la base de datos"

# Probamos para el cálculo de estadísticas de temperatura
def test_estadisticas_temperatura():
    sistema = Sistema.obtener_instancia()
    estrategia_media = EstrategiaMedia(data=sistema.base_de_datos, sensor_id=sistema.sensor_id)
    estrategia_media.execute()  # Calcula la media de temperatura
    # Agrega más pruebas para otras estrategias...

# Probamos para el manejo de solicitudes en la cadena de responsabilidad
def test_cadena_de_responsabilidad():
    supera_umbral_handler = SuperaUmbralHandler()
    aumento_brusco_handler = AumentoBruscoHandler(supera_umbral_handler)
    request = Request(step="SuperaUmbral", current_temperature=85, threshold=80)
    aumento_brusco_handler.handle_request(request)  # Verifica si el umbral se supera correctamente
    # Agrega más pruebas para otros pasos de la cadena de responsabilidad...

# Probamos para la notificación de observadores
def test_notificar_observadores():
    sistema = Sistema.obtener_instancia()
    sistema_observer = SistemaObserver()
    sistema.attach(sistema_observer)
    sistema.actualizar(30)  # Actualiza el sistema con una nueva temperatura
    assert len(sistema_observer.datos) == 1, "Error en la notificación de observadores"

# Ejecutamos las pruebas
if __name__ == "__main__":
    pytest.main()

