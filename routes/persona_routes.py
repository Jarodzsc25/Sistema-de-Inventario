from flask import Blueprint, request, jsonify
from db import get_connection
from extensions import bcrypt

bp = Blueprint('persona', __name__, url_prefix='/api')

@bp.route('/persona', methods=['GET'])
def obtener_persona():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM persona ORDER BY id_persona;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{
        "id_persona": p[0],
        "nombre": p[1],
        "apellido": p[2],
        "correo": p[3],
        "telefono": p[4]
    } for p in data])

@bp.route('/persona', methods=['POST'])
def agregar_persona():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO persona (nombre, apellido, correo, telefono) VALUES (%s,%s,%s,%s) RETURNING id_persona;",
        (data['nombre'], data['apellido'], data.get('correo'), data.get('telefono'))
    )
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Persona agregada", "id_persona": id_nuevo})

@bp.route('/persona/<int:id_persona>', methods=['PUT'])
def actualizar_persona(id_persona):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE persona SET nombre=%s, apellido=%s, correo=%s, telefono=%s WHERE id_persona=%s;",
        (data['nombre'], data['apellido'], data.get('correo'), data.get('telefono'), id_persona)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Persona actualizada"})

@bp.route('/persona/<int:id_persona>', methods=['DELETE'])
def eliminar_persona(id_persona):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM persona WHERE id_persona=%s;", (id_persona,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Persona eliminada"})
