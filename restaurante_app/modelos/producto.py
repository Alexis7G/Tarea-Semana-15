class Producto:
    """Representa un producto del menú del restaurante."""

    def __init__(self, id_producto, nombre, categoria, precio, disponible=True):
        self.id = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = float(precio)
        self.disponible = bool(disponible)

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio,
            "disponible": self.disponible,
        }

    @staticmethod
    def from_dict(data):
        return Producto(
            id_producto=data.get("id"),
            nombre=data.get("nombre"),
            categoria=data.get("categoria"),
            precio=data.get("precio", 0),
            disponible=data.get("disponible", True),
        )

    def __str__(self):
        estado = "Disponible" if self.disponible else "No disponible"
        return f"[{self.id}] {self.nombre} - {self.categoria} - ${self.precio:.2f} - {estado}"
