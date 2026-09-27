import os
import tkinter as tk

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


def cargar_imagen(nombre_archivo, reduccion=1):
    """Carga un PNG de assets/ como PhotoImage de Tkinter.

    ``reduccion`` permite reducir el tamaño original de forma entera
    (p. ej. 2 reduce el ícono a la mitad), útil para reutilizar los mismos
    archivos de assets/ en botones e íconos de distinto tamaño.
    Devuelve None si el archivo no existe, para que la interfaz pueda
    seguir funcionando aunque falte algún recurso gráfico.
    """
    ruta = os.path.join(ASSETS_DIR, nombre_archivo)
    if not os.path.exists(ruta):
        return None
    imagen = tk.PhotoImage(file=ruta)
    if reduccion > 1:
        imagen = imagen.subsample(reduccion, reduccion)
    return imagen
