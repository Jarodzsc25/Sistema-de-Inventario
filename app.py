# backend/app.py
from flask import Flask, jsonify, request
from psycopg2 import OperationalError, DatabaseError
from db_config import execute_query
from routes.rol import rol_bp
from routes.persona import persona_bp
from routes.usuario import usuario_bp
from routes.distribuidor import distribuidor_bp
from routes.producto import producto_bp
from routes.documento import documento_bp
from routes.movimiento import movimiento_bp
from routes.kardex import kardex_bp
import base64

app = Flask(__name__)
app.config['DEBUG'] = True

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Registrar Blueprints
app.register_blueprint(rol_bp, url_prefix='/api/rol')
app.register_blueprint(persona_bp, url_prefix='/api/persona')
app.register_blueprint(usuario_bp, url_prefix='/api/usuario')
app.register_blueprint(distribuidor_bp, url_prefix='/api/distribuidor')
app.register_blueprint(producto_bp, url_prefix='/api/producto')
app.register_blueprint(documento_bp, url_prefix='/api/documento')
app.register_blueprint(movimiento_bp, url_prefix='/api/movimiento')
app.register_blueprint(kardex_bp, url_prefix='/api/kardex')


# --- NUEVA RUTA DE LOGIN ---
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

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

        # Login exitoso
        return jsonify({
            "mensaje": "Login exitoso",
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
