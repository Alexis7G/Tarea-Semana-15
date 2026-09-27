import os

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_PRODUCTOS = os.path.join(BASE_DIR, "datos", "productos.json")
RUTA_USUARIOS = os.path.join(BASE_DIR, "datos", "usuarios.json")
RUTA_VENTAS = os.path.join(BASE_DIR, "datos", "ventas.json")


class RestauranteServicio:
    """Contenedor central de la lógica de negocio del restaurante.

    Coordina el acceso a productos y usuarios, delegando la persistencia
    en ArchivoServicio y exponiendo una única interfaz para la capa de UI,
    de modo que las vistas (componentes) nunca acceden a los archivos
    directamente.
    """

    def __init__(self):
        self._productos = self._cargar_productos()
        self._usuarios = self._cargar_usuarios()
        self._ventas = self._cargar_ventas()

    # ---------- Carga inicial ----------
    def _cargar_productos(self):
        datos = ArchivoServicio.cargar(RUTA_PRODUCTOS)
        return [Producto.from_dict(d) for d in datos]

    def _cargar_usuarios(self):
        datos = ArchivoServicio.cargar(RUTA_USUARIOS)
        return [Usuario.from_dict(d) for d in datos]

    def _cargar_ventas(self):
        datos = ArchivoServicio.cargar(RUTA_VENTAS)
        return [Venta.from_dict(d) for d in datos]

    # ---------- Autenticación ----------
    def validar_usuario(self, usuario, password):
        for u in self._usuarios:
            if u.usuario == usuario and u.password == password:
                return u
        return None

    # ---------- Consultas ----------
    def listar_productos(self):
        return list(self._productos)

    def listar_usuarios(self):
        return list(self._usuarios)

    def buscar_producto(self, id_producto):
        for p in self._productos:
            if str(p.id) == str(id_producto):
                return p
        return None

    def _siguiente_id(self):
        if not self._productos:
            return 1
        return max(int(p.id) for p in self._productos) + 1

    # ---------- Operaciones CRUD ----------
    def agregar_producto(self, nombre, categoria, precio, disponible=True):
        nuevo = Producto(self._siguiente_id(), nombre, categoria, precio, disponible)
        self._productos.append(nuevo)
        self._guardar_productos()
        return nuevo

    def actualizar_producto(self, id_producto, **campos):
        producto = self.buscar_producto(id_producto)
        if producto is None:
            return False
        if campos.get("nombre"):
            producto.nombre = campos["nombre"]
        if campos.get("categoria"):
            producto.categoria = campos["categoria"]
        if campos.get("precio") not in (None, ""):
            producto.precio = float(campos["precio"])
        if "disponible" in campos:
            producto.disponible = bool(campos["disponible"])
        self._guardar_productos()
        return True

    def eliminar_producto(self, id_producto):
        producto = self.buscar_producto(id_producto)
        if producto is None:
            return False
        self._productos.remove(producto)
        self._guardar_productos()
        return True

    # ---------- Ventas ----------
    def listar_ventas(self):
        return list(self._ventas)

    def _siguiente_id_venta(self):
        if not self._ventas:
            return 1
        return max(int(v.id) for v in self._ventas) + 1

    def registrar_venta(self, usuario, id_producto, cantidad):
        """Valida y registra una venta a partir de un usuario y un producto.

        Aplica las reglas de negocio (producto existente y disponible,
        cantidad válida) antes de calcular el total y persistir el
        resultado en ventas.json. La UI solo debe invocar este método;
        nunca debe calcular totales ni escribir el archivo directamente.
        """
        if not usuario:
            raise ValueError("Debe seleccionar un usuario.")

        producto = self.buscar_producto(id_producto)
        if producto is None:
            raise ValueError("El producto seleccionado no existe.")
        if not producto.disponible:
            raise ValueError("El producto seleccionado no está disponible.")

        try:
            cantidad = int(cantidad)
        except (TypeError, ValueError):
            raise ValueError("La cantidad debe ser un número entero.")
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        total = round(producto.precio * cantidad, 2)
        venta = Venta(
            id_venta=self._siguiente_id_venta(),
            usuario=usuario,
            id_producto=producto.id,
            nombre_producto=producto.nombre,
            cantidad=cantidad,
            total=total,
        )
        self._ventas.append(venta)
        self._guardar_ventas()
        return venta

    def _guardar_ventas(self):
        ArchivoServicio.guardar(RUTA_VENTAS, [v.to_dict() for v in self._ventas])

    # ---------- Persistencia ----------
    def _guardar_productos(self):
        ArchivoServicio.guardar(RUTA_PRODUCTOS, [p.to_dict() for p in self._productos])
