
# API REST - Sistema de Inventario y Gestión de Usuarios

Este proyecto es una **API RESTful** desarrollada en **Flask (Python)** que permite la gestión de usuarios, roles, personas, productos, movimientos, documentos, distribuidores y kardex dentro de un sistema de inventario.  
La aplicación está organizada de forma modular mediante **Blueprints** y documentada con **OpenAPI (Swagger)**.

---

## Características principales

- Arquitectura modular usando **Flask Blueprints**  
- CRUD completo para:
  - **Usuarios**
  - **Roles**
  - **Personas**
  - **Productos**
  - **Movimientos**
  - **Distribuidores**
  - **Documentos**
  - **Kardex**
- Conexión con base de datos **PostgreSQL/MySQL**
- Documentación de endpoints con **OpenAPI 3.1.0**
- Validaciones básicas y manejo de errores
- Respuestas en formato **JSON**

---

## Tecnologías utilizadas

| Tecnología | Descripción |
|-------------|-------------|
| **Python 3.x** | Lenguaje principal |
| **Flask** | Framework web |
| **Blueprints** | Modularización de rutas |
| **PostgreSQL / MySQL** | Base de datos |
| **Swagger / OpenAPI** | Documentación interactiva |
| **Werkzeug** | Utilidades de seguridad |
| **JWT (opcional)** | Autenticación basada en tokens |

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
```

---

## Instalación y configuración

### Clonar el repositorio
```bash
git clone https://github.com/tu_usuario/flask_api_sistema.git
cd flask_api_sistema
```

### Crear entorno virtual
```bash
python -m venv venv
source venv/bin/activate   # En Linux/Mac
venv\Scripts\activate      # En Windows
```

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Configurar la base de datos
En el archivo `db_config.py`, agrega tus credenciales:
```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'tu_usuario',
    'password': 'tu_password',
    'database': 'nombre_db'
}
```

---

## Ejecución del servidor

Ejecuta el servidor Flask:
```bash
python app.py
```

Accede a la API en:
```
http://127.0.0.1:5000
```

---

## Documentación de la API

El archivo [`openapi.yaml`](./openapi.yaml) contiene toda la documentación de los endpoints.  
Puedes visualizarla en **Swagger Editor**:

1. Abre [https://editor.swagger.io](https://editor.swagger.io)
2. Carga el archivo `openapi.yaml`
3. Prueba los endpoints de forma interactiva

---

## Endpoints principales

### Usuarios
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| GET | `/usuarios` | Lista todos los usuarios |
| POST | `/usuarios` | Crea un nuevo usuario |
| GET | `/usuarios/{id}` | Obtiene un usuario por ID |
| PUT | `/usuarios/{id}` | Actualiza un usuario |
| DELETE | `/usuarios/{id}` | Elimina un usuario |

---

### Roles
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| GET | `/roles` | Obtiene todos los roles |
| POST | `/roles` | Crea un nuevo rol |
| GET | `/roles/{id}` | Obtiene un rol por ID |
| PUT | `/roles/{id}` | Actualiza un rol |
| DELETE | `/roles/{id}` | Elimina un rol |

---

### Personas
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| GET | `/personas` | Lista todas las personas |
| POST | `/personas` | Crea una nueva persona |
| GET | `/personas/{id}` | Obtiene una persona por ID |
| PUT | `/personas/{id}` | Actualiza una persona |
| DELETE | `/personas/{id}` | Elimina una persona |

---

### Productos
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| GET | `/productos` | Lista todos los productos |
| POST | `/productos` | Crea un nuevo producto |
| GET | `/productos/{id}` | Obtiene un producto por ID |
| PUT | `/productos/{id}` | Actualiza un producto |
| DELETE | `/productos/{id}` | Elimina un producto |

---

### Distribuidores
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| GET | `/distribuidores` | Lista todos los distribuidores |
| POST | `/distribuidores` | Crea un nuevo distribuidor |
| GET | `/distribuidores/{id}` | Obtiene un distribuidor por ID |
| PUT | `/distribuidores/{id}` | Actualiza un distribuidor |
| DELETE | `/distribuidores/{id}` | Elimina un distribuidor |

---

### Documentos
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| GET | `/documentos` | Lista todos los documentos |
| POST | `/documentos` | Crea un nuevo documento |
| GET | `/documentos/{id}` | Obtiene un documento por ID |
| PUT | `/documentos/{id}` | Actualiza un documento |
| DELETE | `/documentos/{id}` | Elimina un documento |

---

### Movimientos
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| GET | `/movimientos` | Lista todos los movimientos |
| POST | `/movimientos` | Crea un nuevo movimiento |
| GET | `/movimientos/{id}` | Obtiene un movimiento por ID |
| PUT | `/movimientos/{id}` | Actualiza un movimiento |
| DELETE | `/movimientos/{id}` | Elimina un movimiento |

---

### Kardex
| Método | Endpoint | Descripción |
|--------|-----------|-------------|
| GET | `/kardex` | Lista todos los registros del kardex |
| POST | `/kardex` | Crea un nuevo registro en el kardex |
| GET | `/kardex/{id}` | Obtiene un registro por ID |
| PUT | `/kardex/{id}` | Actualiza un registro del kardex |
| DELETE | `/kardex/{id}` | Elimina un registro del kardex |

---

## Ejemplo de petición

```json
POST /usuarios
{
  "username": "Jose",
  "password": "J@se25",
  "email": "jose25@gmail.com"
}
```

Respuesta:
```json
{
  "message": "Usuario creado exitosamente",
  "id_usuario": 1
}
```

---

## Autenticación (opcional)

Para proteger tus endpoints, puedes usar **JWT**:

```bash
pip install Flask-JWT-Extended
```

Ejemplo:
```python
from flask_jwt_extended import jwt_required

@usuario_bp.route('/usuarios', methods=['GET'])
@jwt_required()
def get_usuarios():
    ...
```

---

## Integración con Swagger UI (local)

Puedes montar tu propia interfaz Swagger ejecutando:
```bash
pip install flask-swagger-ui
```

Y en `app.py`:
```python
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/openapi.yaml'

swagger_bp = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)
```

Accede en:
```
http://127.0.0.1:5000/api/docs
```

---

## Licencia

Este proyecto está bajo la licencia **MIT**.  
Puedes usarlo, modificarlo y distribuirlo libremente citando la fuente original.

---

## Autor

**Jarod Zarian Cádiz Salanova**  
*cadizsalanovajarodzarian@gmail.com*  
Proyecto académico - API REST con Flask y OpenAPI
