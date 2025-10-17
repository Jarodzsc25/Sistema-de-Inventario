from flask import Blueprint, request, jsonify
from db import get_connection
from extensions import bcrypt

bp = Blueprint('producto', __name__, url_prefix='/api')

@bp.route('/producto', methods=['GET'])
def obtener_producto():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.id_producto, p.codigo, p.nombre, p.descripcion, p.unidad, p.id_distribuidor, d.nombre
        FROM producto p
        LEFT JOIN distribuidor d ON p.id_distribuidor = d.id_distribuidor
        ORDER BY p.id_producto;
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{
        "id_producto": p[0],
        "codigo": p[1],
        "nombre": p[2],
        "descripcion": p[3],
        "unidad": p[4],
        "id_distribuidor": p[5],
        "distribuidor_nombre": p[6]
    } for p in data])

@bp.route('/producto', methods=['POST'])
def agregar_producto():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO producto (codigo, nombre, descripcion, unidad, id_distribuidor) VALUES (%s,%s,%s,%s,%s) RETURNING id_producto;",
        (data['codigo'], data['nombre'], data.get('descripcion'), data.get('unidad'), data['id_distribuidor'])
    )
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Producto agregado", "id_producto": id_nuevo})

@bp.route('/producto/<int:id_producto>', methods=['PUT'])
def actualizar_producto(id_producto):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE producto SET codigo=%s, nombre=%s, descripcion=%s, unidad=%s, id_distribuidor=%s WHERE id_producto=%s;",
        (data['codigo'], data['nombre'], data.get('descripcion'), data.get('unidad'), data['id_distribuidor'], id_producto)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Producto actualizado"})

@bp.route('/producto/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM producto WHERE id_producto=%s;", (id_producto,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Producto eliminado"})
