from flask import Blueprint, request, jsonify
from db import get_connection
from extensions import bcrypt

bp = Blueprint('movimiento', __name__, url_prefix='/api')

@bp.route('/movimiento', methods=['GET'])
def obtener_movimiento():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT m.id_movimiento, m.tipo, m.fecha, m.glosa, m.observacion,
               u.username, c.nombre, d.numero
        FROM movimiento m
        LEFT JOIN usuario u ON m.id_elaborador = u.id_usuario
        LEFT JOIN cliente c ON m.id_cliente = c.id_cliente
        LEFT JOIN documento d ON m.id_documento = d.id_documento
        ORDER BY m.id_movimiento;
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{
        "id_movimiento": m[0],
        "tipo": m[1],
        "fecha": str(m[2]),
        "glosa": m[3],
        "observacion": m[4],
        "elaborado_por": m[5],
        "cliente": m[6],
        "documento_numero": m[7]
    } for m in data])

@bp.route('/movimiento', methods=['POST'])
def agregar_movimiento():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO movimiento (tipo, fecha, glosa, observacion, id_elaborador, id_cliente, id_documento)
        VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id_movimiento;
    """, (data['tipo'], data['fecha'], data.get('glosa'), data.get('observacion'),
          data['id_elaborador'], data['id_cliente'], data['id_documento']))
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Movimiento agregado", "id_movimiento": id_nuevo})

@bp.route('/movimiento/<int:id_movimiento>', methods=['PUT'])
def actualizar_movimiento(id_movimiento):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE movimiento
        SET tipo=%s, fecha=%s, glosa=%s, observacion=%s
        WHERE id_movimiento=%s;
    """, (data['tipo'], data['fecha'], data.get('glosa'), data.get('observacion'), id_movimiento))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Movimiento actualizado"})

@bp.route('/movimiento/<int:id_movimiento>', methods=['DELETE'])
def eliminar_movimiento(id_movimiento):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM movimiento WHERE id_movimiento=%s;", (id_movimiento,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Movimiento eliminado"})
