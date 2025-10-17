from flask import Blueprint, request, jsonify
from db import get_connection
from extensions import bcrypt

bp = Blueprint('distribuidor', __name__, url_prefix='/api')

@bp.route('/distribuidor', methods=['GET'])
def obtener_distribuidores():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM distribuidor ORDER BY id_distribuidor;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{
        "id_distribuidor": d[0],
        "nit": d[1],
        "nombre": d[2],
        "contacto": d[3],
        "telefono": d[4],
        "direccion": d[5]
    } for d in data])

@bp.route('/distribuidor', methods=['POST'])
def agregar_distribuidor():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO distribuidor (nit, nombre, contacto, telefono, direccion) VALUES (%s,%s,%s,%s,%s) RETURNING id_distribuidor;",
        (data['nit'], data['nombre'], data.get('contacto'), data.get('telefono'), data.get('direccion'))
    )
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Distribuidor agregado", "id_distribuidor": id_nuevo})

@bp.route('/distribuidor/<int:id_distribuidor>', methods=['PUT'])
def actualizar_distribuidor(id_distribuidor):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE distribuidor SET nit=%s, nombre=%s, contacto=%s, telefono=%s, direccion=%s WHERE id_distribuidor=%s;",
        (data['nit'], data['nombre'], data.get('contacto'), data.get('telefono'), data.get('direccion'), id_distribuidor)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Distribuidor actualizado"})

@bp.route('/distribuidor/<int:id_distribuidor>', methods=['DELETE'])
def eliminar_distribuidor(id_distribuidor):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM distribuidor WHERE id_distribuidor=%s;", (id_distribuidor,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Distribuidor eliminado"})
