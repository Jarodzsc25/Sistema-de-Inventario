from flask import Blueprint, request, jsonify
from db import get_connection
from extensions import bcrypt

bp = Blueprint('documento', __name__, url_prefix='/api')

@bp.route('/documento', methods=['GET'])
def obtener_documento():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM documento ORDER BY id_documento;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([{
        "id_documento": d[0],
        "numero": d[1],
        "fecha": str(d[2])
    } for d in data])

@bp.route('/documento', methods=['POST'])
def agregar_documento():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO documento (numero, fecha) VALUES (%s,%s) RETURNING id_documento;",
        (data['numero'], data['fecha'])
    )
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Documento agregado", "id_documento": id_nuevo})

@bp.route('/documento/<int:id_documento>', methods=['PUT'])
def actualizar_documento(id_documento):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE documento SET numero=%s, fecha=%s WHERE id_documento=%s;",
        (data['numero'], data['fecha'], id_documento)
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Documento actualizado"})

@bp.route('/documento/<int:id_documento>', methods=['DELETE'])
def eliminar_documento(id_documento):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM documento WHERE id_documento=%s;", (id_documento,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Documento eliminado"})
