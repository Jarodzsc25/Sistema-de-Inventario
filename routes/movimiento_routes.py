from flask import Blueprint, request, jsonify
from db import get_connection
from psycopg2 import extras

movimiento_bp = Blueprint('movimientos', __name__)

@movimiento_bp.route('/movimientos', methods=['GET'])
def obtener_movimientos():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""
        SELECT 
            m.id_movimiento,
            m.tipo,
            m.fecha,
            m.glosa,
            m.observacion,
            u.username AS elaborado_por,
            p.nombre AS cliente,
            d.numero AS documento_numero
        FROM movimiento m
        LEFT JOIN usuario u ON m.id_elaborador = u.id_usuario
        LEFT JOIN persona p ON m.id_cliente = p.id_persona
        LEFT JOIN documento d ON m.id_documento = d.id_documento
        ORDER BY m.id_movimiento ASC;
    """)
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@movimiento_bp.route('/movimientos', methods=['POST'])
def agregar_movimiento():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO movimiento (tipo, fecha, glosa, observacion, id_elaborador, id_cliente, id_documento)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id_movimiento;
    """, (
        data['tipo'], data['fecha'], data.get('glosa'),
        data.get('observacion'), data.get('id_elaborador'),
        data.get('id_cliente'), data.get('id_documento')
    ))
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Movimiento agregado', 'id_movimiento': id_nuevo})

@movimiento_bp.route('/movimientos/<int:id_movimiento>', methods=['PUT'])
def actualizar_movimiento(id_movimiento):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE movimiento
        SET tipo=%s, fecha=%s, glosa=%s, observacion=%s, id_elaborador=%s, id_cliente=%s, id_documento=%s
        WHERE id_movimiento=%s;
    """, (
        data['tipo'], data['fecha'], data.get('glosa'),
        data.get('observacion'), data.get('id_elaborador'),
        data.get('id_cliente'), data.get('id_documento'), id_movimiento
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Movimiento actualizado'})

@movimiento_bp.route('/movimientos/<int:id_movimiento>', methods=['DELETE'])
def eliminar_movimiento(id_movimiento):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM movimiento WHERE id_movimiento = %s;", (id_movimiento,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Movimiento eliminado'})
