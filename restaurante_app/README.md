# Restaurante App

Aplicación de escritorio en Python (Tkinter) para la gestión modular de un
restaurante, desarrollada como evolución del proyecto de la asignatura
**Programación Orientada a Objetos** — Taller Semana 15: *Fundamentos
básicos de manejo de eventos*.

## Datos de la entrega

- **Universidad:** Universidad Estatal Amazónica
- **Asignatura:** Programación Orientada a Objetos
- **Actividad:** Semana 15 — Taller Práctico: Conceptos fundamentales de
  manejo de eventos en restaurante_app
- **Estudiante:** Alexis Gustavo Gualán Gualán
- **Repositorio:** _(pega aquí el enlace público de GitHub una vez subido)_

## Propósito

Comprender los fundamentos básicos de manejo de eventos en interfaces
gráficas: cómo una acción del usuario (click en un botón) dispara un
`command=`, cómo ese callback coordina la operación con el servicio de
dominio (`RestauranteServicio`) y cómo el resultado se refleja de vuelta en
la interfaz, conservando la arquitectura modular construida en semanas
anteriores.

## Estructura del proyecto

```
restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── componentes.py
│   ├── login_view.py
│   ├── main_view.py
│   └── recursos.py
├── assets/
│   ├── logo.png
│   ├── icon_inicio.png
│   ├── icon_usuarios.png
│   ├── icon_productos.png
│   ├── icon_ventas.png
│   └── icon_logout.png
├── main.py
└── README.md
```

- **modelos/**: clases de dominio `Producto`, `Usuario` y `Venta` (nueva),
  todas con serialización a/desde diccionario para persistencia en JSON.
  `Venta` relaciona un usuario, un producto, la cantidad y el total.
- **servicios/**: `ArchivoServicio` (persistencia genérica en archivos
  JSON) y `RestauranteServicio` (lógica de negocio: autenticación, CRUD de
  productos, consulta de usuarios y registro de ventas), única capa que
  accede a los datos. La UI nunca manipula los archivos JSON directamente.
- **ui/**: capa de presentación.
  - `componentes.py`: componentes reutilizables — `FormularioProducto`,
    `TablaProductos`, `BarraEstado`, y los nuevos `TablaUsuarios`,
    `FormularioVenta` y `TablaVentas` — todos independientes de la lógica
    de negocio.
  - `login_view.py`: vista de inicio de sesión (incluye el logo del
    sistema).
  - `main_view.py`: contenedores de la ventana principal — barra de
    navegación (sidebar) con logo e íconos, área de contenido
    intercambiable, y las vistas `VistaInicio`, `VistaUsuarios`,
    `VistaProductos` y `VistaVentas` (nueva).
  - `recursos.py` (nuevo): helper que centraliza la carga de imágenes
    desde `assets/` como `PhotoImage` de Tkinter.
- **assets/** (nuevo, obligatorio para esta semana): logo del sistema e
  íconos usados en el login, el sidebar y el ícono de la ventana.
- **main.py**: punto de entrada; orquesta el flujo login → ventana
  principal, sin lógica propia de negocio ni de presentación.

## Evolución realizada en la Semana 15

- Se incorporó el **modelo `Venta`**, siguiendo el mismo patrón de
  `Producto` y `Usuario` (constructor, `to_dict`/`from_dict`).
- Se agregó a `RestauranteServicio` el método `registrar_venta(usuario,
  id_producto, cantidad)`, que valida (usuario seleccionado, producto
  existente y disponible, cantidad entera positiva), calcula el total y
  persiste el resultado en `ventas.json`; y `listar_ventas()` /
  `listar_usuarios()` para las consultas de la interfaz.
- Se agregó la **sección Ventas** (`VistaVentas`), que combina
  `FormularioVenta` (selección de usuario y producto, cantidad) con
  `TablaVentas` (historial de ventas registradas).
- Se agregó la **sección Usuarios** (`VistaUsuarios`) de solo consulta,
  reutilizando el mismo patrón de componente de tabla.
- Se incorporó la carpeta **assets/** con el logo y los íconos del
  sistema, integrados en el login, el menú lateral y el ícono de la
  ventana (`root.iconphoto`).
- Se mantuvieron intactas las funciones de `Productos` desarrolladas
  previamente (alta, edición, eliminación, listado).

## Fundamento de eventos evidenciado

```
USUARIO
   │ realiza una acción
   ▼
BOTÓN "Registrar venta"  (widget con command=)
   │
   ▼
CALLBACK  (VistaVentas._registrar_venta)
   │
   ▼
RestauranteServicio.registrar_venta()   (valida y calcula el total)
   │
   ▼
PERSISTENCIA en ventas.json  (vía ArchivoServicio)
   │
   ▼
RESPUESTA VISUAL EN LA INTERFAZ
   (BarraEstado + refresco de TablaVentas)
```

El botón de la interfaz solo dispara el callback mediante `command=`; toda
la validación, el cálculo del total y el acceso a los datos quedan
delegados en `RestauranteServicio`. La interfaz nunca contiene lógica de
negocio ni manipula `ventas.json` directamente.

## Flujo funcional

1. `main.py` inicia la aplicación, aplica el ícono del sistema y muestra
   `LoginView` (con el logo de la app).
2. El usuario ingresa credenciales; `RestauranteServicio.validar_usuario`
   las verifica contra `usuarios.json`.
3. Al autenticar, se construye `MainWindow`, que arma la navegación
   (Inicio / Usuarios / Productos / Ventas / Cerrar sesión), con íconos y
   el logo en el sidebar.
4. En **Usuarios** se listan los usuarios registrados (consulta).
5. En **Productos** se mantiene la gestión ya existente (alta, edición,
   eliminación) delegada en `RestauranteServicio`.
6. En **Ventas**, el usuario elige un usuario y un producto disponible,
   define la cantidad y presiona **"Registrar venta"**.
7. El botón (`command=`) dispara el callback de `VistaVentas`, que llama a
   `RestauranteServicio.registrar_venta`.
8. El servicio valida los datos, calcula el total y persiste la venta en
   `ventas.json` a través de `ArchivoServicio`.
9. La `TablaVentas` se refresca con la nueva venta y la `BarraEstado`
   informa el resultado (éxito o el error de validación correspondiente).

## Requisitos

- Python 3.9 o superior (Tkinter incluido en la instalación estándar).
- Librería `Pillow` **no** es necesaria para ejecutar la app: los assets ya
  están generados como `.png` y se cargan con `tkinter.PhotoImage`.

## Ejecución

Desde la carpeta raíz del proyecto:

```bash
python main.py
```

### Credenciales de prueba

| Usuario  | Contraseña | Rol    |
|----------|------------|--------|
| admin    | admin123   | admin  |
| mesero1  | mesero123  | mesero |

## Alcance

Conforme a lo solicitado para esta semana, se implementó el uso de
`command=` para el botón de registro de venta y el flujo evento → callback
→ servicio → persistencia → respuesta visual. **No** se implementó manejo
avanzado de eventos con `bind`, doble clic, eventos específicos de
teclado/mouse, `TreeviewSelect` para selección múltiple de filas,
facturación, carrito de compra, inventario avanzado ni bases de datos; la
persistencia se mantiene mediante archivos JSON.
