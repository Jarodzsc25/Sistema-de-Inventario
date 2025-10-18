from flask import Blueprint, request, jsonify
from db_config import execute_query
from datetime import datetime

movimiento_bp = Blueprint('movimiento_bp', __name__)


# Función para obtener los campos de Movimiento
def get_movimiento_fields(data):
    """Extrae y retorna los campos de movimiento de un diccionario."""
    # Usamos datetime.now().isoformat() como default si 'fecha' no está
    fecha_default = datetime.now().isoformat()
    return (
        data.get('tipo'),
        data.get('fecha', fecha_default),
        data.get('glosa'),
        data.get('observacion'),
        data.get('id_elaborador'),
        data.get('id_cliente'),
        data.get('id_documento')
    )


# Obtener todos los movimientos y crear uno nuevo (GET y POST)
@movimiento_bp.route('/', methods=['GET', 'POST'])
def handle_movimientos():
    if request.method == 'POST':
        # --- CREATE (Crear nuevo Movimiento) ---
        data = request.get_json()
        tipo, fecha, glosa, observacion, id_elaborador, id_cliente, id_documento = get_movimiento_fields(data)

        if not all([tipo, glosa]):
            return jsonify({"error": "Faltan campos obligatorios: tipo (E/S) y glosa."}), 400
        if tipo not in ('E', 'S'):
            return jsonify({"error": "El campo 'tipo' debe ser 'E' (Entrada) o 'S' (Salida)."}), 400

        sql = """
            INSERT INTO movimiento (tipo, fecha, glosa, observacion, id_elaborador, id_cliente, id_documento) 
            VALUES (%s, %s, %s, %s, %s, %s, %s) 
            RETURNING id_movimiento
        """
        params = (tipo, fecha, glosa, observacion, id_elaborador, id_cliente, id_documento)

        try:
            results = execute_query(sql, params, fetch=True)
            new_id = results[0]['id_movimiento'] if results else None
            return jsonify({
                "mensaje": "Movimiento creado con éxito.",
                "id_movimiento": new_id,
                "tipo": tipo
            }), 201
        except Exception as e:
            return jsonify({"error": "Error al crear movimiento. Verifica las FK (elaborador, cliente, documento).",
                            "detalle": str(e)}), 400

    else:
        # --- READ ALL (Obtener todos los Movimientos) ---
        sql = "SELECT * FROM movimiento ORDER BY id_movimiento DESC"
        try:
            movimientos = execute_query(sql, fetch=True)
            return jsonify(movimientos), 200
        except Exception:
            return jsonify({"error": "Error al obtener lista de movimientos"}), 500


# Obtener, actualizar o eliminar un Movimiento por ID (GET, PUT, DELETE)
@movimiento_bp.route('/<int:id_movimiento>', methods=['GET', 'PUT', 'DELETE'])
def handle_movimiento(id_movimiento):
    if request.method == 'GET':
        # --- READ ONE (Obtener un Movimiento) ---
        sql = "SELECT * FROM movimiento WHERE id_movimiento = %s"
        try:
            movimiento = execute_query(sql, (id_movimiento,), fetch=True)
            if movimiento:
                return jsonify(movimiento[0]), 200
            return jsonify({"error": "Movimiento no encontrado."}), 404
        except Exception:
            return jsonify({"error": "Error al obtener movimiento"}), 500

    elif request.method == 'PUT':
        # --- UPDATE (Actualizar Movimiento) ---
        data = request.get_json()
        tipo, fecha, glosa, observacion, id_elaborador, id_cliente, id_documento = get_movimiento_fields(data)

        if not all([tipo, glosa]):
            return jsonify({"error": "Los campos 'tipo' y 'glosa' son obligatorios para actualizar."}), 400
        if tipo not in ('E', 'S'):
            return jsonify({"error": "El campo 'tipo' debe ser 'E' (Entrada) o 'S' (Salida)."}), 400

        sql = """
            UPDATE movimiento SET 
                tipo = %s, fecha = %s, glosa = %s, observacion = %s, 
                id_elaborador = %s, id_cliente = %s, id_documento = %s 
            WHERE id_movimiento = %s
        """
        params = (tipo, fecha, glosa, observacion, id_elaborador, id_cliente, id_documento, id_movimiento)

        try:
            row_count = execute_query(sql, params)
            if row_count > 0:
                return jsonify({"mensaje": "Movimiento actualizado con éxito.", "id_movimiento": id_movimiento}), 200
            return jsonify({"error": "Movimiento no encontrado para actualizar."}), 404
        except Exception as e:
            return jsonify({"error": "Error al actualizar movimiento. Verifica las FK.", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        # --- DELETE (Eliminar Movimiento) ---
        sql = "DELETE FROM movimiento WHERE id_movimiento = %s"
        try:
            row_count = execute_query(sql, (id_movimiento,))
            if row_count > 0:
                # La eliminación del Movimiento en cascada eliminará las entradas de Kardex asociadas.
                return jsonify({"mensaje": "Movimiento eliminado con éxito. Se eliminaron sus Kardex asociados.",
                                "id_movimiento": id_movimiento}), 200
            return jsonify({"error": "Movimiento no encontrado para eliminar."}), 404
        except Exception as e:
            return jsonify({"error": "Error al eliminar movimiento.", "detalle": str(e)}), 400
