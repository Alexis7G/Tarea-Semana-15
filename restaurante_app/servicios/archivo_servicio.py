import json
import os


class ArchivoServicio:
    """Servicio genérico para leer y escribir información en archivos JSON.

    Se encarga exclusivamente de la persistencia, manteniendo esta
    responsabilidad separada de la lógica de negocio del restaurante.
    """

    @staticmethod
    def cargar(ruta):
        if not os.path.exists(ruta):
            return []
        try:
            with open(ruta, "r", encoding="utf-8") as archivo:
                contenido = json.load(archivo)
                return contenido if isinstance(contenido, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    @staticmethod
    def guardar(ruta, datos):
        carpeta = os.path.dirname(ruta)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta, exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)
