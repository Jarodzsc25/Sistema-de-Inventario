from flask import Blueprint, request, jsonify
from db import get_connection
from psycopg2 import extras

persona_bp = Blueprint('personas', __name__)

@persona_bp.route('/personas', methods=['GET'])
def obtener_personas():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM persona ORDER BY id_persona ASC;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@persona_bp.route('/personas', methods=['POST'])
def agregar_persona():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO persona (nombre, primer_apellido, segundo_apellido, telefono, correo)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_persona;
    """, (
        data['nombre'], data.get('primer_apellido'),
        data.get('segundo_apellido'), data.get('telefono'), data.get('correo')
    ))
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Persona agregada', 'id_persona': id_nuevo})

@persona_bp.route('/personas/<int:id_persona>', methods=['PUT'])
def actualizar_persona(id_persona):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE persona
        SET nombre=%s, primer_apellido=%s, segundo_apellido=%s, telefono=%s, correo=%s
        WHERE id_persona=%s;
    """, (
        data['nombre'], data.get('primer_apellido'),
        data.get('segundo_apellido'), data.get('telefono'),
        data.get('correo'), id_persona
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Persona actualizada'})

@persona_bp.route('/personas/<int:id_persona>', methods=['DELETE'])
def eliminar_persona(id_persona):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM persona WHERE id_persona = %s;", (id_persona,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Persona eliminada'})
