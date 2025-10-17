from flask import Blueprint, request, jsonify
from db import get_connection
from extensions import bcrypt

bp = Blueprint('kardex', __name__, url_prefix='/api')

@bp.route('/kardex', methods=['GET'])
def obtener_kardex():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT k.id_movimiento, k.id_producto, p.nombre, k.tipo_movimiento,
               k.fecha, k.cantidad, k.unitario, k.suttotal
        FROM kardex k
        LEFT JOIN producto p ON k.id_producto = p.id_producto
        ORDER BY k.id_movimiento, k.id_producto;
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{
        "id_movimiento": k[0],
        "id_producto": k[1],
        "producto": k[2],
        "tipo_movimiento": k[3],
        "fecha": str(k[4]),
        "cantidad": float(k[5]),
        "unitario": float(k[6]),
        "suttotal": float(k[7])
    } for k in data])

@bp.route('/kardex', methods=['POST'])
def agregar_kardex():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO kardex (id_movimiento, id_producto, cantidad, unitario, suttotal)
        VALUES (%s,%s,%s,%s,%s);
    """, (data['id_movimiento'], data['id_producto'], data['cantidad'], data['unitario'], data['suttotal']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Registro de Kardex agregado"})

@bp.route('/kardex', methods=['DELETE'])
def eliminar_kardex():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM kardex WHERE id_movimiento=%s AND id_producto=%s;", (data['id_movimiento'], data['id_producto']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Registro de Kardex eliminado"})
