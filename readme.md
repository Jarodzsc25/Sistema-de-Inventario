# Sistema de Ventas

Este proyecto es un **Sistema de Gestión de Ventas e Inventario** diseñado para administrar productos, distribuidores, movimientos de inventario, usuarios y personas. Cuenta con una arquitectura de **Backend (Flask/Python)** y un **Frontend (HTML/CSS/JavaScript)**.

## Características Principales

* **Gestión de Productos:** Creación, edición y listado de productos con detalles como código, nombre, descripción, unidad y distribuidor.
* **Gestión de Movimientos:** Registro y listado de movimientos de inventario (entradas/salidas).
* **Gestión de Distribuidores, Usuarios y Personas** (Funcionalidad `admin-only` en el menú).
* **Autenticación de Usuarios:** Login seguro con manejo de roles (se asume *Administrador* y *Vendedor* por la estructura del menú).
* **Interfaz de Usuario:** Interfaz simple y responsive construida con **Bootstrap 5**.

## Tecnologías Utilizadas

| Componente | Tecnología | Descripción |
| :--- | :--- | :--- |
| **Backend** | **Python / Flask** | Servidor API RESTful para la lógica de negocio y la conexión a la base de datos. |
| **Base de Datos** | **PostgreSQL** (se asume por `psycopg2` en `app.py`) | Base de datos relacional para almacenar toda la información del sistema. |
| **Frontend** | **HTML5, CSS3, JavaScript** | Interfaz de usuario con manejo de la lógica de presentación y consumo de la API. |
| **Estilos** | **Bootstrap 5** | Framework CSS para el diseño y la responsividad. |


---

## Estructura del proyecto

```
flask_api_sistema/
│
├── app.py                   # Punto de entrada principal
├── db_config.py              # Configuración de la base de datos
├── openapi.yaml              # Documentación OpenAPI
│
├── blueprints/
│   ├── usuario.py            # CRUD de usuarios
│   ├── rol.py                # CRUD de roles
│   ├── persona.py            # CRUD de personas
│   ├── producto.py           # CRUD de productos
│   ├── movimiento.py         # CRUD de movimientos
│   ├── distribuidor.py       # CRUD de distribuidores
│   ├── documento.py          # CRUD de documentos
│   └── kardex.py             # CRUD de kardex
frontend/
├── index.html               # Página de inicio.
├── dashboard.html           # Interfaz principal de la aplicación.
│
├── css/
│   └── style.css            # Estilos CSS generales.
│
└── js/
    ├── api.js               # Funciones para realizar llamadas a la API (fetch, axios).
    ├── auth.js              # Lógica para la autenticación de usuarios (login/logout).
    ├── ui_admin.js          # Scripts específicos para la interfaz del administrador.
    └── ui_vendedor.js       # Scripts específicos para la interfaz del vendedor.

```

---
## Puesta en Marcha

Sigue estos pasos para configurar y ejecutar el proyecto en tu entorno local.

### 1. Backend (API Flask)

El backend maneja las rutas API y la interacción con la base de datos.

**Requisitos Previos de Aplicaciones Instaladas:**
* PyCharm 2025.2.1.1
* PostgreSQL

**Como Configurar el Sistema:**

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/Jarodzsc25/Sistema-de-Inventario.git
    cd sistema de inventario
    ```
2.  **Descarga el Zip del Repositorio:**
    ```bash
    Entre a esta URL seleccione codigo y descargar zip: https://github.com/Jarodzsc25/Sistema-de-Inventario.git
    Una vez descargado copiar el zip en un directorio y descomprima el archivo.
    Luego entre a la aplicacion de Pycharm, acceda a archivos ve al apartado de open y busque la carpeta de descomprimio, acepte y se le cargara todo el sistema. 
    ```
3.  **Instala las dependencias:**

    ```bash
    En la terminal de pycharm introduzca el siguiente comando:
    pip install -r requirements.txt
    ```
4.  **Configura la Base de Datos:**
    * Acceda a la Aplicacion de Postgresql, una vez dentro se le pedira crear un usuario y contraseña(nota no olvide los datos que pondra sin eso no podra avanzar).
    * Una vez creado el usuario y contraseña, ve al apartado de Postgresql 16(Click derecho crear base de datos nueva), en esa seccion ponga el siguiente nombre:"bd_ventas".
    * Una vez creada baje hasta esqumas(1) haga click izquierdo, ahora click derecho en public y seleccione Scrip Create.
    * Una vez creado borre el texto que tiene; en la aplicacion de Pycharm, en la carpeta documento hay un archivo "llamado codigo sql.txt", copie el contenido en el scrip de postgresql.
    * Una vez copiado el codigo dentro el scrip, oprima f5 para que se ejecute el codigo.
    * Seleciona public y otra vez f5 para actualizar; para verificar que se creo correctamente baje hasta el apartado que diga tablas seleciona y deberia aparecer ya las tablas, si le aparece esta todo correcto.
    * ### Configurar la base de datos
En el archivo `db_config.py`, agrega tus credenciales:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'tu_usuario',
    'password': 'tu_password',
    'database': 'nombre_db'
}
```
5.  **Ejecuta el servidor:**
    ```bash
    En la terminar de Pycharm escriba lo siguiente:
    python app.py
    ```
    El servidor se ejecutará por defecto en `http://localhost:5000`. La API base es `http://localhost:5000/api`.

### 2. Frontend (Interfaz de Usuario)

El frontend es una aplicación web pura que consume la API del backend.

**Configuración:**

1.  **Navega a la carpeta del frontend:**
    ```bash
    En la carpta del frontend ve al archivo login.html click derecho y baja hasta "open in" y selecciona "browser", luego seleciona tu navegador favorito.
    ```
2.  **Servir los archivos:**
    * Simplemente abre `index.html` en tu navegador para la pantalla de login.
    * **Importante:** Para evitar problemas de CORS y de carga de módulos, se recomienda utilizar un servidor web local simple (como Live Server en VS Code o `python -m http.server`).

---

## Estructura del Proyecto (Resumen)

| Archivo/Ruta | Descripción |
| :--- | :--- |
| **`app.py`** | Punto de entrada del backend (Flask). Define la aplicación, CORS y registra los Blueprints de las rutas. |
| **`routes/*.py`** | Módulos con las rutas API específicas (e.g., `routes/producto.py`, `routes/usuario.py`, `routes/cliente.py`). |
| **`db_config.py`** | Módulo para la conexión y ejecución de consultas a la BD. |
| **`index.html`** | Estructura principal, incluye el formulario de **Login** y la plantilla principal del sistema. |
| **`ui_vendedor.js`** | Lógica JavaScript del frontend, manejo de eventos de menú (Productos, Movimientos) y renderizado de tablas. |
| **`api.js`** | Funciones JavaScript para interactuar con el Backend (p.ej., `getProductos()`, `loginUser()`). |
| **`frontend.txt`** | (Asumido como `ui_vendedor.js` o similar) Contiene la lógica para la visualización de listas de productos y movimientos. |

---

## Base de Datos

El diseño de la base de datos es clave para la estructura de la aplicación. 

> La imagen anterior muestra el **diagrama de la base de datos** (o similar), que incluye tablas como `usuario`, `persona`, `rol`, `cliente`, `producto`, `distribuidor`, `movimiento`, entre otras.

**Tablas Relevantes (Basado en el código):**

* `persona`
* `usuario`
* `rol`
* `distribuidor`
* `producto`
* `movimiento`
* `cliente`

---

## Contribución

Si deseas contribuir, por favor:

1.  Haz un *Fork* de este repositorio.
2.  Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`).
3.  Comitéa tus cambios (`git commit -m 'feat: Añadir nueva característica X'`).
4.  Empuja la rama (`git push origin feature/nueva-caracteristica`).
5.  Abre un *Pull Request*.

---

## Licencia
Este proyecto está bajo la licencia **MIT**.  
Puedes usarlo, modificarlo y distribuirlo libremente citando la fuente original.

---

## Autor

**Jarod Zarian Cádiz Salanova**  
*cadizsalanovajarodzarian@gmail.com*  
Proyecto académico - API REST con Flask y OpenAPI