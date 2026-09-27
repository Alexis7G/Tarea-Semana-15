import tkinter as tk
from tkinter import ttk

from ui.recursos import cargar_imagen


class LoginView(ttk.Frame):
    """Vista de inicio de sesión, independiente de la ventana principal."""

    def __init__(self, master, servicio, al_iniciar_sesion, **kwargs):
        super().__init__(master, padding=20, **kwargs)
        self.servicio = servicio
        self.al_iniciar_sesion = al_iniciar_sesion

        self._logo = cargar_imagen("logo.png", reduccion=3)
        if self._logo is not None:
            ttk.Label(self, image=self._logo).grid(row=0, column=0, columnspan=2, pady=(0, 10))
        else:
            ttk.Label(self, text="Restaurante App", font=("Segoe UI", 18, "bold")).grid(
                row=0, column=0, columnspan=2, pady=(0, 15)
            )

        ttk.Label(self, text="Usuario:").grid(row=1, column=0, sticky="e", padx=5, pady=6)
        self.var_usuario = tk.StringVar()
        ttk.Entry(self, textvariable=self.var_usuario, width=22).grid(row=1, column=1, padx=5, pady=6)

        ttk.Label(self, text="Contraseña:").grid(row=2, column=0, sticky="e", padx=5, pady=6)
        self.var_password = tk.StringVar()
        ttk.Entry(self, textvariable=self.var_password, show="*", width=22).grid(row=2, column=1, padx=5, pady=6)

        self.var_mensaje = tk.StringVar()
        ttk.Label(self, textvariable=self.var_mensaje, foreground="red").grid(
            row=3, column=0, columnspan=2, pady=4
        )

        ttk.Button(self, text="Iniciar sesión", command=self._intentar_login).grid(
            row=4, column=0, columnspan=2, pady=10
        )

        self.bind_all("<Return>", lambda e: self._intentar_login())

    def _intentar_login(self):
        usuario = self.var_usuario.get().strip()
        password = self.var_password.get().strip()

        if not usuario or not password:
            self.var_mensaje.set("Ingrese usuario y contraseña.")
            return

        usuario_valido = self.servicio.validar_usuario(usuario, password)
        if usuario_valido:
            self.var_mensaje.set("")
            self.al_iniciar_sesion(usuario_valido)
        else:
            self.var_mensaje.set("Usuario o contraseña incorrectos.")
