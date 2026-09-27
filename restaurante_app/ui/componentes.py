import tkinter as tk
from tkinter import ttk


class BarraEstado(ttk.Frame):
    """Componente reutilizable para mostrar mensajes de estado al usuario."""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.mensaje = tk.StringVar(value="Listo.")
        self.etiqueta = ttk.Label(self, textvariable=self.mensaje, anchor="w")
        self.etiqueta.pack(fill="x", padx=5, pady=2)

    def mostrar(self, texto, es_error=False):
        self.mensaje.set(texto)
        self.etiqueta.configure(foreground="red" if es_error else "black")


class FormularioProducto(ttk.LabelFrame):
    """Componente de formulario para registrar o editar un producto.

    Es independiente de la lógica de negocio: solo recolecta datos y
    delega el procesamiento mediante un callback (al_guardar).
    """

    def __init__(self, master, al_guardar=None, **kwargs):
        super().__init__(master, text="Datos del producto", **kwargs)
        self.al_guardar = al_guardar
        self.id_actual = None

        self.var_nombre = tk.StringVar()
        self.var_categoria = tk.StringVar()
        self.var_precio = tk.StringVar()
        self.var_disponible = tk.BooleanVar(value=True)

        ttk.Label(self, text="Nombre:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(self, textvariable=self.var_nombre, width=25).grid(row=0, column=1, padx=5, pady=4)

        ttk.Label(self, text="Categoría:").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(self, textvariable=self.var_categoria, width=25).grid(row=1, column=1, padx=5, pady=4)

        ttk.Label(self, text="Precio:").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(self, textvariable=self.var_precio, width=25).grid(row=2, column=1, padx=5, pady=4)

        ttk.Checkbutton(self, text="Disponible", variable=self.var_disponible).grid(
            row=3, column=0, columnspan=2, sticky="w", padx=5, pady=4
        )

        botones = ttk.Frame(self)
        botones.grid(row=4, column=0, columnspan=2, pady=8)
        ttk.Button(botones, text="Guardar", command=self._guardar).pack(side="left", padx=4)
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=4)

    def cargar_producto(self, producto):
        self.id_actual = producto.id
        self.var_nombre.set(producto.nombre)
        self.var_categoria.set(producto.categoria)
        self.var_precio.set(str(producto.precio))
        self.var_disponible.set(producto.disponible)

    def limpiar(self):
        self.id_actual = None
        self.var_nombre.set("")
        self.var_categoria.set("")
        self.var_precio.set("")
        self.var_disponible.set(True)

    def obtener_datos(self):
        return {
            "id": self.id_actual,
            "nombre": self.var_nombre.get().strip(),
            "categoria": self.var_categoria.get().strip(),
            "precio": self.var_precio.get().strip(),
            "disponible": self.var_disponible.get(),
        }

    def _guardar(self):
        if self.al_guardar:
            self.al_guardar(self.obtener_datos())


class TablaProductos(ttk.Frame):
    """Componente de tabla (Treeview) para listar productos."""

    COLUMNAS = ("id", "nombre", "categoria", "precio", "disponible")

    def __init__(self, master, al_seleccionar=None, **kwargs):
        super().__init__(master, **kwargs)
        self.al_seleccionar = al_seleccionar

        self.tabla = ttk.Treeview(self, columns=self.COLUMNAS, show="headings", height=12)
        titulos = {
            "id": "ID",
            "nombre": "Nombre",
            "categoria": "Categoría",
            "precio": "Precio",
            "disponible": "Disponible",
        }
        for col in self.COLUMNAS:
            self.tabla.heading(col, text=titulos[col])
            self.tabla.column(col, width=110, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tabla.bind("<<TreeviewSelect>>", self._on_select)

    def refrescar(self, productos):
        self.tabla.delete(*self.tabla.get_children())
        for p in productos:
            self.tabla.insert(
                "", "end", iid=str(p.id),
                values=(p.id, p.nombre, p.categoria, f"{p.precio:.2f}", "Sí" if p.disponible else "No"),
            )

    def obtener_id_seleccionado(self):
        seleccion = self.tabla.selection()
        return seleccion[0] if seleccion else None

    def _on_select(self, event):
        if self.al_seleccionar:
            id_sel = self.obtener_id_seleccionado()
            if id_sel is not None:
                self.al_seleccionar(id_sel)


class TablaUsuarios(ttk.Frame):
    """Componente de solo consulta para listar los usuarios del sistema."""

    COLUMNAS = ("usuario", "nombre_completo", "rol")

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.tabla = ttk.Treeview(self, columns=self.COLUMNAS, show="headings", height=12)
        titulos = {"usuario": "Usuario", "nombre_completo": "Nombre completo", "rol": "Rol"}
        for col in self.COLUMNAS:
            self.tabla.heading(col, text=titulos[col])
            self.tabla.column(col, width=150, anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refrescar(self, usuarios):
        self.tabla.delete(*self.tabla.get_children())
        for u in usuarios:
            self.tabla.insert(
                "", "end", iid=u.usuario,
                values=(u.usuario, u.nombre_completo, u.rol.capitalize()),
            )


class FormularioVenta(ttk.LabelFrame):
    """Componente de formulario para registrar una venta.

    Permite seleccionar un usuario y un producto ya existentes y define la
    cantidad. No calcula totales ni valida reglas de negocio: solo recoge
    los datos y los entrega mediante el callback ``al_registrar`` para que
    sea ``RestauranteServicio`` quien procese la operación.
    """

    def __init__(self, master, usuarios, productos, al_registrar=None, **kwargs):
        super().__init__(master, text="Registrar venta", **kwargs)
        self.al_registrar = al_registrar

        self._usuarios = list(usuarios)
        self._productos = list(productos)

        self.var_usuario = tk.StringVar()
        self.var_producto = tk.StringVar()
        self.var_cantidad = tk.StringVar(value="1")

        ttk.Label(self, text="Usuario:").grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.combo_usuario = ttk.Combobox(
            self, textvariable=self.var_usuario, state="readonly", width=28,
            values=[u.usuario for u in self._usuarios],
        )
        self.combo_usuario.grid(row=0, column=1, padx=5, pady=4)

        ttk.Label(self, text="Producto:").grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.combo_producto = ttk.Combobox(
            self, textvariable=self.var_producto, state="readonly", width=28,
            values=[f"{p.id} - {p.nombre} (${p.precio:.2f})" for p in self._productos if p.disponible],
        )
        self.combo_producto.grid(row=1, column=1, padx=5, pady=4)

        ttk.Label(self, text="Cantidad:").grid(row=2, column=0, sticky="w", padx=5, pady=4)
        ttk.Entry(self, textvariable=self.var_cantidad, width=10).grid(row=2, column=1, sticky="w", padx=5, pady=4)

        ttk.Button(self, text="Registrar venta", command=self._registrar).grid(
            row=3, column=0, columnspan=2, pady=10
        )

    def actualizar_opciones(self, usuarios, productos):
        self._usuarios = list(usuarios)
        self._productos = list(productos)
        self.combo_usuario.configure(values=[u.usuario for u in self._usuarios])
        self.combo_producto.configure(
            values=[f"{p.id} - {p.nombre} (${p.precio:.2f})" for p in self._productos if p.disponible]
        )

    def limpiar(self):
        self.var_usuario.set("")
        self.var_producto.set("")
        self.var_cantidad.set("1")

    def obtener_datos(self):
        id_producto = None
        seleccion = self.var_producto.get()
        if seleccion:
            id_producto = seleccion.split(" - ", 1)[0].strip()
        return {
            "usuario": self.var_usuario.get().strip(),
            "id_producto": id_producto,
            "cantidad": self.var_cantidad.get().strip(),
        }

    def _registrar(self):
        if self.al_registrar:
            self.al_registrar(self.obtener_datos())


class TablaVentas(ttk.Frame):
    """Componente de tabla (Treeview) para listar las ventas registradas."""

    COLUMNAS = ("id", "usuario", "producto", "cantidad", "total", "fecha")

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.tabla = ttk.Treeview(self, columns=self.COLUMNAS, show="headings", height=12)
        titulos = {
            "id": "ID",
            "usuario": "Usuario",
            "producto": "Producto",
            "cantidad": "Cantidad",
            "total": "Total",
            "fecha": "Fecha",
        }
        anchos = {"id": 40, "usuario": 90, "producto": 160, "cantidad": 70, "total": 80, "fecha": 130}
        for col in self.COLUMNAS:
            self.tabla.heading(col, text=titulos[col])
            self.tabla.column(col, width=anchos[col], anchor="center")

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)

        self.tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refrescar(self, ventas):
        self.tabla.delete(*self.tabla.get_children())
        for v in ventas:
            self.tabla.insert(
                "", "end", iid=str(v.id),
                values=(v.id, v.usuario, v.nombre_producto, v.cantidad, f"{v.total:.2f}", v.fecha),
            )
