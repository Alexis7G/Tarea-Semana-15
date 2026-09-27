from datetime import datetime


class Venta:
    """Representa una venta registrada en el restaurante.

    Relaciona a un usuario (mesero/admin que atiende) con un producto del
    menú y la cantidad vendida, calculando el total de la operación.
    """

    def __init__(self, id_venta, usuario, id_producto, nombre_producto, cantidad, total, fecha=None):
        self.id = id_venta
        self.usuario = usuario
        self.id_producto = id_producto
        self.nombre_producto = nombre_producto
        self.cantidad = int(cantidad)
        self.total = float(total)
        self.fecha = fecha or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario": self.usuario,
            "id_producto": self.id_producto,
            "nombre_producto": self.nombre_producto,
            "cantidad": self.cantidad,
            "total": self.total,
            "fecha": self.fecha,
        }

    @staticmethod
    def from_dict(data):
        return Venta(
            id_venta=data.get("id"),
            usuario=data.get("usuario"),
            id_producto=data.get("id_producto"),
            nombre_producto=data.get("nombre_producto"),
            cantidad=data.get("cantidad", 0),
            total=data.get("total", 0),
            fecha=data.get("fecha"),
        )

    def __str__(self):
        return (
            f"[{self.id}] {self.usuario} - {self.nombre_producto} "
            f"x{self.cantidad} - ${self.total:.2f} ({self.fecha})"
        )
