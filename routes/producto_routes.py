from flask import Blueprint, request, jsonify
from db import get_connection
from psycopg2 import extras

producto_bp = Blueprint('productos', __name__)

@producto_bp.route('/productos', methods=['GET'])
def obtener_productos():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""
        SELECT p.*, d.nombre AS distribuidor_nombre
        FROM producto p
        JOIN distribuidor d ON p.id_distribuidor = d.id_distribuidor
        ORDER BY p.id_producto ASC;
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@producto_bp.route('/productos', methods=['POST'])
def agregar_producto():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO producto (codigo, nombre, descripcion, unidad, id_distribuidor)
        VALUES (%s, %s, %s, %s, %s) RETURNING id_producto;
    """, (data['codigo'], data['nombre'], data.get('descripcion'),
          data.get('unidad'), data['id_distribuidor']))
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Producto agregado', 'id_producto': id_nuevo})

@producto_bp.route('/productos/<int:id_producto>', methods=['PUT'])
def actualizar_producto(id_producto):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE producto
        SET codigo=%s, nombre=%s, descripcion=%s, unidad=%s, id_distribuidor=%s
        WHERE id_producto=%s;
    """, (data['codigo'], data['nombre'], data.get('descripcion'),
          data.get('unidad'), data['id_distribuidor'], id_producto))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Producto actualizado'})

@producto_bp.route('/productos/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM producto WHERE id_producto = %s;", (id_producto,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Producto eliminado'})
