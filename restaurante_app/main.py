import tkinter as tk
from tkinter import ttk

from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainWindow
from ui.recursos import cargar_imagen


class Aplicacion:
    """Punto de entrada del sistema.

    Coordina el ciclo de vida entre la pantalla de login y la ventana
    principal, sin contener lógica de negocio ni de presentación propia.
    """

    def __init__(self):
        self.servicio = RestauranteServicio()
        self.root = tk.Tk()
        self.root.title("Restaurante App")
        self.root.geometry("800x500")
        self.root.minsize(700, 450)

        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        self._icono_app = cargar_imagen("logo.png")
        if self._icono_app is not None:
            self.root.iconphoto(True, self._icono_app)

        self._mostrar_login()

    def _mostrar_login(self):
        self._limpiar_ventana()
        vista = LoginView(self.root, self.servicio, al_iniciar_sesion=self._iniciar_sesion)
        vista.pack(fill="both", expand=True)

    def _iniciar_sesion(self, usuario):
        self._limpiar_ventana()
        MainWindow(self.root, self.servicio, usuario, al_cerrar_sesion=self._mostrar_login)

    def _limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def ejecutar(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = Aplicacion()
    app.ejecutar()
