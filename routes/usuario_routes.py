from flask import Blueprint, request, jsonify
from db import get_connection
from extensions import bcrypt


bp = Blueprint('usuario', __name__, url_prefix='/api')

@bp.route('/usuario', methods=['GET'])
def obtener_usuario():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id_usuario, username, rol FROM usuario ORDER BY id_usuario;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{"id_usuario": u[0], "username": u[1], "rol": u[2]} for u in data])

@bp.route('/usuario', methods=['POST'])
def agregar_usuario():
    data = request.get_json()
    password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO usuario (username, password, rol) VALUES (%s,%s,%s) RETURNING id_usuario;",
        (data['username'], password_hash, data['rol'])
    )
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Usuario agregado", "id_usuario": id_nuevo})

@bp.route('/usuario/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    data = request.get_json()
    password_hash = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE usuario SET username=%s, password=%s, rol=%s WHERE id_usuario=%s;",
        (data['username'], password_hash, data['rol'], id_usuario)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Usuario actualizado"})

@bp.route('/usuario/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuario WHERE id_usuario=%s;", (id_usuario,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Usuario eliminado"})
