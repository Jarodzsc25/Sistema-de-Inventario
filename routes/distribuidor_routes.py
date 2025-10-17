from flask import Blueprint, request, jsonify
from db import get_connection
from psycopg2 import extras

distribuidor_bp = Blueprint('distribuidores', __name__)

@distribuidor_bp.route('/distribuidores', methods=['GET'])
def obtener_distribuidores():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM distribuidor ORDER BY id_distribuidor ASC;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@distribuidor_bp.route('/distribuidores', methods=['POST'])
def agregar_distribuidor():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO distribuidor (nit, nombre, contacto, telefono, direccion)
        VALUES (%s, %s, %s, %s, %s) RETURNING id_distribuidor;
    """, (data['nit'], data['nombre'], data.get('contacto'),
          data.get('telefono'), data.get('direccion')))
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Distribuidor agregado', 'id_distribuidor': id_nuevo})

@distribuidor_bp.route('/distribuidores/<int:id_distribuidor>', methods=['PUT'])
def actualizar_distribuidor(id_distribuidor):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE distribuidor
        SET nit=%s, nombre=%s, contacto=%s, telefono=%s, direccion=%s
        WHERE id_distribuidor=%s;
    """, (data['nit'], data['nombre'], data.get('contacto'),
          data.get('telefono'), data.get('direccion'), id_distribuidor))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Distribuidor actualizado'})

@distribuidor_bp.route('/distribuidores/<int:id_distribuidor>', methods=['DELETE'])
def eliminar_distribuidor(id_distribuidor):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM distribuidor WHERE id_distribuidor = %s;", (id_distribuidor,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Distribuidor eliminado'})
