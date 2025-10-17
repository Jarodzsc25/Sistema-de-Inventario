from flask import Blueprint, request, jsonify
from db import get_connection
from flask_bcrypt import Bcrypt
from psycopg2 import extras

usuario_bp = Blueprint('usuarios', __name__)
bcrypt = Bcrypt()

@usuario_bp.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""
        SELECT 
            u.id_usuario, u.username, u.id_rol, r.nombre AS rol, 
            p.nombre AS persona_nombre, p.primer_apellido, p.correo
        FROM usuario u
        JOIN rol r ON u.id_rol = r.id_rol
        JOIN persona p ON u.id_usuario = p.id_persona
        ORDER BY u.id_usuario ASC;
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@usuario_bp.route('/usuarios', methods=['POST'])
def agregar_usuario():
    data = request.get_json()
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO usuario (username, password, id_rol)
        VALUES (%s, %s, %s)
        RETURNING id_usuario;
    """, (data['username'], hashed_pw, data['id_rol']))
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Usuario agregado', 'id_usuario': id_nuevo})

@usuario_bp.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    if 'password' in data and data['password']:
        hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        cur.execute("""
            UPDATE usuario
            SET username=%s, password=%s, id_rol=%s
            WHERE id_usuario=%s;
        """, (data['username'], hashed_pw, data['id_rol'], id_usuario))
    else:
        cur.execute("""
            UPDATE usuario
            SET username=%s, id_rol=%s
            WHERE id_usuario=%s;
        """, (data['username'], data['id_rol'], id_usuario))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Usuario actualizado'})

@usuario_bp.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuario WHERE id_usuario = %s;", (id_usuario,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Usuario eliminado'})
