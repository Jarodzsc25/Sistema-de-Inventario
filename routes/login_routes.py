from flask import Blueprint, request, jsonify, render_template
from flask_bcrypt import Bcrypt
from db import get_connection
from psycopg2 import extras

login_bp = Blueprint('login', __name__)
bcrypt = Bcrypt()

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""
        SELECT u.id_usuario, u.username, u.password, r.nombre AS rol,
               p.nombre AS persona_nombre, p.primer_apellido, p.correo
        FROM usuario u
        JOIN rol r ON u.id_rol = r.id_rol
        JOIN persona p ON u.id_usuario = p.id_persona
        WHERE u.username = %s;
    """, (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        del user['password']
        return jsonify({"mensaje": "Login exitoso", "usuario": user}), 200
    else:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

@login_bp.route('/')
def login_page():
    return render_template('login.html')

@login_bp.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')
