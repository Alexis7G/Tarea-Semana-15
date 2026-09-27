from tkinter import ttk

from ui.componentes import (
    FormularioProducto,
    TablaProductos,
    BarraEstado,
    TablaUsuarios,
    FormularioVenta,
    TablaVentas,
)
from ui.recursos import cargar_imagen


class VistaProductos(ttk.Frame):
    """Contenedor que integra el formulario y la tabla para gestionar productos."""

    def __init__(self, master, servicio, barra_estado, **kwargs):
        super().__init__(master, **kwargs)
        self.servicio = servicio
        self.barra_estado = barra_estado

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.formulario = FormularioProducto(self, al_guardar=self._guardar_producto)
        self.formulario.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        panel_derecho = ttk.Frame(self)
        panel_derecho.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        panel_derecho.rowconfigure(0, weight=1)
        panel_derecho.columnconfigure(0, weight=1)

        self.tabla = TablaProductos(panel_derecho, al_seleccionar=self._seleccionar_producto)
        self.tabla.grid(row=0, column=0, sticky="nsew")

        botones = ttk.Frame(panel_derecho)
        botones.grid(row=1, column=0, pady=8, sticky="w")
        ttk.Button(botones, text="Eliminar seleccionado", command=self._eliminar_producto).pack(side="left", padx=4)
        ttk.Button(botones, text="Actualizar lista", command=self.refrescar).pack(side="left", padx=4)

        self.refrescar()

    def refrescar(self):
        self.tabla.refrescar(self.servicio.listar_productos())

    def _seleccionar_producto(self, id_producto):
        producto = self.servicio.buscar_producto(id_producto)
        if producto:
            self.formulario.cargar_producto(producto)

    def _guardar_producto(self, datos):
        if not datos["nombre"] or not datos["categoria"] or not datos["precio"]:
            self.barra_estado.mostrar("Complete todos los campos obligatorios.", es_error=True)
            return
        try:
            precio = float(datos["precio"])
        except ValueError:
            self.barra_estado.mostrar("El precio debe ser un número válido.", es_error=True)
            return

        if datos["id"] is None:
            self.servicio.agregar_producto(datos["nombre"], datos["categoria"], precio, datos["disponible"])
            self.barra_estado.mostrar("Producto registrado correctamente.")
        else:
            self.servicio.actualizar_producto(
                datos["id"], nombre=datos["nombre"], categoria=datos["categoria"],
                precio=precio, disponible=datos["disponible"],
            )
            self.barra_estado.mostrar("Producto actualizado correctamente.")

        self.formulario.limpiar()
        self.refrescar()

    def _eliminar_producto(self):
        id_sel = self.tabla.obtener_id_seleccionado()
        if not id_sel:
            self.barra_estado.mostrar("Seleccione un producto para eliminar.", es_error=True)
            return
        self.servicio.eliminar_producto(id_sel)
        self.formulario.limpiar()
        self.refrescar()
        self.barra_estado.mostrar("Producto eliminado.")


class VistaUsuarios(ttk.Frame):
    """Sección de solo consulta de los usuarios registrados en el sistema."""

    def __init__(self, master, servicio, **kwargs):
        super().__init__(master, padding=10, **kwargs)
        self.servicio = servicio

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        ttk.Label(self, text="Usuarios del sistema", font=("Segoe UI", 13, "bold")).grid(
            row=0, column=0, sticky="w", pady=(0, 8)
        )

        self.tabla = TablaUsuarios(self)
        self.tabla.grid(row=1, column=0, sticky="nsew")

        self.refrescar()

    def refrescar(self):
        self.tabla.refrescar(self.servicio.listar_usuarios())


class VistaVentas(ttk.Frame):
    """Sección de Ventas: coordina la interfaz de registro con RestauranteServicio.

    Reconstruye, para el dominio del restaurante, el mismo flujo de eventos
    trabajado en la actividad de referencia:
    USUARIO -> BOTÓN (command=) -> CALLBACK -> RestauranteServicio ->
    PERSISTENCIA (ventas.json) -> RESPUESTA visual en la interfaz.
    """

    def __init__(self, master, servicio, barra_estado, **kwargs):
        super().__init__(master, **kwargs)
        self.servicio = servicio
        self.barra_estado = barra_estado

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.formulario = FormularioVenta(
            self,
            usuarios=self.servicio.listar_usuarios(),
            productos=self.servicio.listar_productos(),
            al_registrar=self._registrar_venta,
        )
        self.formulario.grid(row=0, column=0, sticky="n", padx=10, pady=10)

        panel_derecho = ttk.Frame(self)
        panel_derecho.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        panel_derecho.rowconfigure(0, weight=1)
        panel_derecho.columnconfigure(0, weight=1)

        self.tabla = TablaVentas(panel_derecho)
        self.tabla.grid(row=0, column=0, sticky="nsew")

        ttk.Button(panel_derecho, text="Actualizar lista", command=self.refrescar).grid(
            row=1, column=0, pady=8, sticky="w"
        )

        self.refrescar()

    def refrescar(self):
        self.tabla.refrescar(self.servicio.listar_ventas())
        self.formulario.actualizar_opciones(
            self.servicio.listar_usuarios(), self.servicio.listar_productos()
        )

    def _registrar_venta(self, datos):
        """Callback invocado por el botón 'Registrar venta' (command=).

        Delega toda la validación y el cálculo del total en
        RestauranteServicio; esta vista solo recoge datos y muestra el
        resultado al usuario.
        """
        try:
            self.servicio.registrar_venta(
                datos["usuario"], datos["id_producto"], datos["cantidad"]
            )
        except ValueError as error:
            self.barra_estado.mostrar(str(error), es_error=True)
            return

        self.barra_estado.mostrar("Venta registrada correctamente.")
        self.formulario.limpiar()
        self.refrescar()


class VistaInicio(ttk.Frame):
    """Pantalla de bienvenida mostrada tras iniciar sesión."""

    def __init__(self, master, usuario, **kwargs):
        super().__init__(master, padding=30, **kwargs)
        ttk.Label(
            self, text=f"Bienvenido/a, {usuario.nombre_completo}", font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", pady=10)
        ttk.Label(self, text=f"Rol: {usuario.rol.capitalize()}").pack(anchor="w")
        ttk.Label(
            self, text="Utilice el menú lateral para navegar por las secciones del sistema."
        ).pack(anchor="w", pady=10)


class MainWindow(ttk.Frame):
    """Ventana principal: organiza la navegación y el área de contenido.

    Actúa como contenedor de alto nivel que intercambia vistas
    (componentes) según la sección elegida en la barra de navegación,
    manteniendo separada la lógica de presentación de la lógica de negocio.
    """

    def __init__(self, master, servicio, usuario, al_cerrar_sesion, **kwargs):
        super().__init__(master, **kwargs)
        self.servicio = servicio
        self.usuario = usuario
        self.al_cerrar_sesion = al_cerrar_sesion

        self.pack(fill="both", expand=True)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Barra de estado: componente compartido por las distintas vistas
        self.barra_estado = BarraEstado(master)
        self.barra_estado.pack(side="bottom", fill="x")

        # Íconos y logo (obligatorio usar assets/ en la interfaz)
        self._icono_inicio = cargar_imagen("icon_inicio.png", reduccion=2)
        self._icono_usuarios = cargar_imagen("icon_usuarios.png", reduccion=2)
        self._icono_productos = cargar_imagen("icon_productos.png", reduccion=2)
        self._icono_ventas = cargar_imagen("icon_ventas.png", reduccion=2)
        self._icono_logout = cargar_imagen("icon_logout.png", reduccion=2)
        self._logo = cargar_imagen("logo.png", reduccion=5)

        # Contenedor de navegación (sidebar)
        nav = ttk.Frame(self, padding=10)
        nav.grid(row=0, column=0, sticky="ns")

        if self._logo is not None:
            ttk.Label(nav, image=self._logo).pack(pady=(0, 12))
        ttk.Label(nav, text="Menú", font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))
        ttk.Button(
            nav, text=" Inicio", image=self._icono_inicio, compound="left", command=self.mostrar_inicio
        ).pack(fill="x", pady=3)
        ttk.Button(
            nav, text=" Usuarios", image=self._icono_usuarios, compound="left", command=self.mostrar_usuarios
        ).pack(fill="x", pady=3)
        ttk.Button(
            nav, text=" Productos", image=self._icono_productos, compound="left", command=self.mostrar_productos
        ).pack(fill="x", pady=3)
        ttk.Button(
            nav, text=" Ventas", image=self._icono_ventas, compound="left", command=self.mostrar_ventas
        ).pack(fill="x", pady=3)
        ttk.Separator(nav, orient="horizontal").pack(fill="x", pady=10)
        ttk.Button(
            nav, text=" Cerrar sesión", image=self._icono_logout, compound="left", command=self._cerrar_sesion
        ).pack(fill="x", pady=3)

        # Contenedor de contenido: aquí se intercambian las vistas
        self.contenido = ttk.Frame(self)
        self.contenido.grid(row=0, column=1, sticky="nsew")
        self.contenido.rowconfigure(0, weight=1)
        self.contenido.columnconfigure(0, weight=1)

        self._vista_actual = None
        self.mostrar_inicio()

    def _mostrar_vista(self, vista_cls, *args, **kwargs):
        if self._vista_actual is not None:
            self._vista_actual.destroy()
        self._vista_actual = vista_cls(self.contenido, *args, **kwargs)
        self._vista_actual.grid(row=0, column=0, sticky="nsew")

    def mostrar_inicio(self):
        self._mostrar_vista(VistaInicio, self.usuario)
        self.barra_estado.mostrar("Listo.")

    def mostrar_usuarios(self):
        self._mostrar_vista(VistaUsuarios, self.servicio)
        self.barra_estado.mostrar("Listo.")

    def mostrar_productos(self):
        self._mostrar_vista(VistaProductos, self.servicio, self.barra_estado)

    def mostrar_ventas(self):
        self._mostrar_vista(VistaVentas, self.servicio, self.barra_estado)

    def _cerrar_sesion(self):
        self.barra_estado.destroy()
        self.destroy()
        self.al_cerrar_sesion()
