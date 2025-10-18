from flask import Blueprint, request, jsonify
from db_config import execute_query

kardex_bp = Blueprint('kardex_bp', __name__)


# Obtener todos los registros de Kardex y crear uno nuevo (GET y POST)
@kardex_bp.route('/', methods=['GET', 'POST'])
def handle_kardex_entries():
    if request.method == 'POST':
        # --- CREATE (Crear nuevo Registro de Kardex) ---
        data = request.get_json()
        id_movimiento = data.get('id_movimiento')
        id_producto = data.get('id_producto')
        cantidad = data.get('cantidad')
        unitario = data.get('unitario')
        subtotal = data.get('subtotal')  # Opcional: podrías calcularlo en el backend (cantidad * unitario)

        if not all([id_movimiento, id_producto, cantidad, unitario]):
            return jsonify(
                {"error": "Faltan campos obligatorios: id_movimiento, id_producto, cantidad, unitario."}), 400

        # Si subtotal no se proporciona, calcularlo (o dejar que la BD lo maneje si hubiera trigger)
        subtotal = subtotal if subtotal is not None else (cantidad * unitario)

        sql = """
            INSERT INTO kardex (id_movimiento, id_producto, cantidad, unitario, subtotal) 
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id_movimiento, id_producto
        """
        params = (id_movimiento, id_producto, cantidad, unitario, subtotal)

        try:
            execute_query(sql, params)
            return jsonify({
                "mensaje": "Registro de Kardex creado con éxito.",
                "id_movimiento": id_movimiento,
                "id_producto": id_producto
            }), 201
        except Exception as e:
            # Error común: duplicado de clave primaria (Movimiento + Producto ya existe) o FK inexistente
            return jsonify({
                               "error": "Error al crear registro de Kardex. Revise que las IDs sean válidas y la combinación sea única.",
                               "detalle": str(e)}), 400

    else:
        # --- READ ALL (Obtener todos los Registros de Kardex) ---
        sql = "SELECT * FROM kardex ORDER BY id_movimiento DESC, id_producto"
        try:
            kardex_entries = execute_query(sql, fetch=True)
            return jsonify(kardex_entries), 200
        except Exception:
            return jsonify({"error": "Error al obtener lista de registros de Kardex"}), 500


# Obtener, actualizar o eliminar un Registro de Kardex por CLAVE COMPUESTA (GET, PUT, DELETE)
@kardex_bp.route('/<int:id_movimiento>/<int:id_producto>', methods=['GET', 'PUT', 'DELETE'])
def handle_kardex_entry(id_movimiento, id_producto):
    if request.method == 'GET':
        # --- READ ONE (Obtener un Registro de Kardex) ---
        sql = "SELECT * FROM kardex WHERE id_movimiento = %s AND id_producto = %s"
        try:
            entry = execute_query(sql, (id_movimiento, id_producto), fetch=True)
            if entry:
                return jsonify(entry[0]), 200
            return jsonify({"error": "Registro de Kardex no encontrado con esa clave compuesta."}), 404
        except Exception:
            return jsonify({"error": "Error al obtener registro de Kardex"}), 500

    elif request.method == 'PUT':
        # --- UPDATE (Actualizar Registro de Kardex) ---
        data = request.get_json()
        cantidad = data.get('cantidad')
        unitario = data.get('unitario')
        subtotal = data.get('subtotal')  # Opcional: podrías calcularlo

        if not all([cantidad, unitario]):
            return jsonify({"error": "Los campos 'cantidad' y 'unitario' son obligatorios para actualizar."}), 400

        # Si subtotal no se proporciona, calcularlo (o dejar que la BD lo maneje)
        subtotal = subtotal if subtotal is not None else (cantidad * unitario)

        sql = """
            UPDATE kardex SET 
                cantidad = %s, unitario = %s, subtotal = %s 
            WHERE id_movimiento = %s AND id_producto = %s
        """
        params = (cantidad, unitario, subtotal, id_movimiento, id_producto)

        try:
            row_count = execute_query(sql, params)
            if row_count > 0:
                return jsonify({"mensaje": "Registro de Kardex actualizado con éxito.", "id_movimiento": id_movimiento,
                                "id_producto": id_producto}), 200
            return jsonify({"error": "Registro de Kardex no encontrado para actualizar."}), 404
        except Exception as e:
            return jsonify({"error": "Error al actualizar registro de Kardex", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        # --- DELETE (Eliminar Registro de Kardex) ---
        sql = "DELETE FROM kardex WHERE id_movimiento = %s AND id_producto = %s"
        try:
            row_count = execute_query(sql, (id_movimiento, id_producto))
            if row_count > 0:
                return jsonify({"mensaje": "Registro de Kardex eliminado con éxito.", "id_movimiento": id_movimiento,
                                "id_producto": id_producto}), 200
            return jsonify({"error": "Registro de Kardex no encontrado para eliminar."}), 404
        except Exception as e:
            return jsonify({"error": "Error al eliminar registro de Kardex.", "detalle": str(e)}), 400