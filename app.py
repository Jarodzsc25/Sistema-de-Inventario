from flask import Flask, jsonify, request
from psycopg2 import OperationalError, DatabaseError
from db_config import execute_query
import base64
# --- CAMBIO: JWT y utilidades ahora en security.py ---
from flask_cors import CORS
import jwt  # Necesario solo para la función login()

# --- IMPORTAR DESDE EL NUEVO ARCHIVO ---
# Asume que ya creaste security.py y tiene la función token_required
from security import token_required
# -------------------------------------

# *** CORRECCIÓN: Se agrega timezone para resolver DeprecationWarning ***
from datetime import datetime, timedelta, timezone  # Necesario para la función login()

# --- INICIALIZACIÓN DE LA APLICACIÓN Y CONFIGURACIÓN ---
app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'tv7CdjDRtCQnLL0f6cUPrJ1LYoSDX0N25aQ_IP4uHh0'

# --- IMPORTAR BLUEPRINTS DESPUÉS DE LA CONFIGURACIÓN ---
# ... (Las importaciones de tus blueprints) ...
from routes.rol import rol_bp
from routes.persona import persona_bp
from routes.usuario import usuario_bp
from routes.distribuidor import distribuidor_bp
from routes.producto import producto_bp
from routes.documento import documento_bp
from routes.movimiento import movimiento_bp
from routes.kardex import kardex_bp
from routes.cliente import cliente_bp


# Registrar Blueprints
# ... (El registro de tus blueprints) ...
app.register_blueprint(rol_bp, url_prefix='/api/rol')
app.register_blueprint(persona_bp, url_prefix='/api/persona')
app.register_blueprint(usuario_bp, url_prefix='/api/usuario')
app.register_blueprint(distribuidor_bp, url_prefix='/api/distribuidor')
app.register_blueprint(producto_bp, url_prefix='/api/producto')
app.register_blueprint(documento_bp, url_prefix='/api/documento')
app.register_blueprint(movimiento_bp, url_prefix='/api/movimiento')
app.register_blueprint(kardex_bp, url_prefix='/api/kardex')
app.register_blueprint(cliente_bp, url_prefix='/api/cliente')


# --- RUTA DE LOGIN (CORREGIDA) ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    # --- LÍNEAS CORREGIDAS ---
    username = data.get('username')
    password = data.get('password')
    # -------------------------

    if not username or not password:
        return jsonify({"error": "Usuario y contraseña requeridos"}), 400

    try:
        sql = """
            SELECT 
                u.id_usuario, u.username, u.password, r.nombre AS rol_nombre
            FROM usuario u
            JOIN rol r ON u.id_rol = r.id_rol
            WHERE u.username = %s
        """
        user = execute_query(sql, (username,), fetch=True)
        if not user:
            return jsonify({"error": "Usuario no encontrado"}), 404

        user = user[0]
        encoded_pass = base64.b64encode(password.encode()).decode()
        if encoded_pass != user['password']:
            return jsonify({"error": "Contraseña incorrecta"}), 401

        # Generar Token JWT
        payload = {
            'id_usuario': user['id_usuario'],
            'username': user['username'],
            'rol_nombre': user['rol_nombre'],
            # *** CORRECCIÓN DE LA DEPRECATION WARNING ***
            'exp': datetime.now(timezone.utc) + timedelta(hours=24)  # Token expira en 24 horas
        }

        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

        # Login exitoso: devolver el token
        return jsonify({
            "mensaje": "Login exitoso",
            "token": token,
            "usuario": {
                "id_usuario": user['id_usuario'],
                "username": user['username'],
                "rol_nombre": user['rol_nombre']
            }
        }), 200

    except Exception as e:
        return jsonify({"error": "Error en login", "detalle": str(e)}), 500


@app.route('/')
def home():
    return jsonify({"mensaje": "API del Sistema de Ventas en funcionamiento", "version": "2.0"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)