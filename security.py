# backend/security.py
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app


# --- DECORADOR DE AUTENTICACIÓN ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # 1. Obtener el token de la cabecera Authorization
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Acceso no autorizado. Token de autenticación es necesario.'}), 401

        try:
            # 2. Decodificar y verificar el token usando la clave de la app
            # Usamos current_app para acceder a la configuración sin importar app.py
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user_id = data.get('id_usuario')
            request.user_rol = data.get('rol_nombre')

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token ha expirado. Vuelva a iniciar sesión.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido o corrupto.'}), 401
        except Exception:
            return jsonify({'error': 'Error de autenticación.'}), 401

        return f(*args, **kwargs)

    return decorated
# --- FIN DECORADOR ---