class Usuario:
    """Representa un usuario del sistema (administrador o mesero)."""

    def __init__(self, usuario, password, rol="mesero", nombre_completo=""):
        self.usuario = usuario
        self.password = password
        self.rol = rol
        self.nombre_completo = nombre_completo or usuario

    def to_dict(self):
        return {
            "usuario": self.usuario,
            "password": self.password,
            "rol": self.rol,
            "nombre_completo": self.nombre_completo,
        }

    @staticmethod
    def from_dict(data):
        return Usuario(
            usuario=data.get("usuario"),
            password=data.get("password"),
            rol=data.get("rol", "mesero"),
            nombre_completo=data.get("nombre_completo", ""),
        )

    def es_admin(self):
        return self.rol.lower() == "admin"
