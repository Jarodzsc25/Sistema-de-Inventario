from flask import Blueprint, request, jsonify
from db import get_connection
from extensions import bcrypt


bp = Blueprint('login', __name__, url_prefix='/api')

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario, username, password, rol FROM usuario WHERE username=%s;", (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and bcrypt.check_password_hash(user[2], password):
        return jsonify({
            "usuario": {
                "id_usuario": user[0],
                "username": user[1],
                "rol": user[3]
            }
        })
    return jsonify({"error": "Usuario o contraseña incorrectos"}), 401
