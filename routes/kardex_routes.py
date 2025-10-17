from flask import Blueprint, request, jsonify
from db import get_connection
from psycopg2 import extras

kardex_bp = Blueprint('kardex', __name__)

@kardex_bp.route('/kardex', methods=['GET'])
def obtener_kardex():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""
        SELECT 
            k.id_movimiento,
            k.id_producto,
            p.nombre AS producto,
            m.tipo AS tipo_movimiento,
            m.fecha,
            k.cantidad,
            k.unitario,
            k.suttotal
        FROM kardex k
        JOIN producto p ON k.id_producto = p.id_producto
        JOIN movimiento m ON k.id_movimiento = m.id_movimiento
        ORDER BY k.id_movimiento ASC;
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@kardex_bp.route('/kardex', methods=['POST'])
def agregar_kardex():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO kardex (id_movimiento, id_producto, cantidad, unitario, suttotal)
        VALUES (%s, %s, %s, %s, %s);
    """, (
        data['id_movimiento'], data['id_producto'],
        data['cantidad'], data['unitario'], data['suttotal']
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Kardex agregado'})

@kardex_bp.route('/kardex', methods=['DELETE'])
def eliminar_kardex():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM kardex
        WHERE id_movimiento = %s AND id_producto = %s;
    """, (data['id_movimiento'], data['id_producto']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Kardex eliminado'})
