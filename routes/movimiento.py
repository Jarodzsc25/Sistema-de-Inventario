from flask import Blueprint, request, jsonify
from db_config import execute_query
from datetime import datetime
import sys
from security import token_required

# Blueprint (Se asume que la URL es /api/movimiento)
movimiento_bp = Blueprint('movimiento_bp', __name__, url_prefix='/api/movimiento')


# Función para obtener los campos de Movimiento
def get_movimiento_fields(data):
    """Extrae y retorna los campos de movimiento de un diccionario."""
    fecha_default = datetime.now().isoformat()
    return (
        data.get('tipo'),
        data.get('fecha', fecha_default),
        data.get('glosa'),
        data.get('observacion'),
        data.get('id_cliente'),
        data.get('id_documento'),
        # Campos necesarios para la inserción en KARDEX:
        data.get('id_producto'),
        data.get('cantidad'),
        data.get('unitario')
    )


# --- GET y POST ---
@movimiento_bp.route('/', methods=['GET', 'POST'], strict_slashes=False)
@token_required
def handle_movimientos():
    # Obtener el ID del usuario logeado desde el request (asumiendo que 'token_required' lo setea)
    id_usuario_loggeado = request.user_id

    if request.method == 'POST':
        # --- CREATE (Crea Movimiento y la entrada de Kardex) ---
        data = request.get_json()

        # Obtenemos todos los campos, incluyendo los de Kardex
        tipo, fecha, glosa, observacion, id_cliente, id_documento, \
            id_producto, cantidad, unitario = get_movimiento_fields(data)

        # Usamos el id_usuario del token como id_elaborador
        id_elaborador = id_usuario_loggeado

        # --- Validación de campos obligatorios para Movimiento y Kardex ---
        if not all([tipo, glosa, id_producto, cantidad, unitario]):
            # Este error 400 ocurre si el frontend no está enviando los 5 campos
            return jsonify({
                "error": "Faltan campos obligatorios: tipo (E/S), glosa, id_producto, cantidad y unitario."
            }), 400

        if tipo not in ('E', 'S'):
            return jsonify({"error": "El campo 'tipo' debe ser 'E' (Entrada) o 'S' (Salida)."}), 400

        try:
            cantidad = float(cantidad)
            unitario = float(unitario)
            subtotal = cantidad * unitario  # Cálculo del subtotal

            # 1. INSERTAR EN TABLA MOVIMIENTO
            sql_movimiento = """
                INSERT INTO movimiento (tipo, fecha, glosa, observacion, id_elaborador, id_cliente, id_documento) 
                VALUES (%s, %s, %s, %s, %s, %s, %s) 
                RETURNING id_movimiento
            """
            params_movimiento = (tipo, fecha, glosa, observacion, id_elaborador, id_cliente, id_documento)

            # Usamos fetch=True para obtener el ID del movimiento
            results = execute_query(sql_movimiento, params_movimiento, fetch=True)
            id_movimiento_generado = results[0]['id_movimiento'] if results else None

            if not id_movimiento_generado:
                raise Exception("No se pudo obtener el ID del movimiento recién insertado.")

            # 2. INSERTAR EN TABLA KARDEX
            # 🚀 La columna es 'subtotal' (corregido)
            sql_kardex = """
                INSERT INTO kardex (id_movimiento, id_producto, cantidad, unitario, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """
            params_kardex = (
                id_movimiento_generado,
                id_producto,
                cantidad,
                unitario,
                subtotal
            )
            execute_query(sql_kardex, params_kardex)

            print(f"Movimiento y Kardex creados: id_movimiento={id_movimiento_generado}, tipo={tipo}")

            return jsonify({
                "mensaje": "Movimiento y registro de Kardex creados con éxito.",
                "movimiento": {
                    "id_movimiento": id_movimiento_generado,
                    "tipo": tipo,
                    "fecha": fecha,
                    "glosa": glosa
                }
            }), 201

        except Exception as e:
            print(f"Error en POST /api/movimiento/: {e}", file=sys.stderr)
            # El error "suttotal" aparece aquí si la DB está mal o si el SQL no está corregido
            return jsonify({
                "error": "Error al crear movimiento o su registro de Kardex. Verifica FKs o datos numéricos.",
                "detalle": str(e)
            }), 400

    else:
        # --- READ ALL ---
        sql = "SELECT * FROM movimiento ORDER BY id_movimiento DESC"
        try:
            movimientos = execute_query(sql, fetch=True)
            return jsonify(movimientos), 200
        except Exception as e:
            print(f"Error en GET /api/movimiento/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener lista de movimientos"}), 500


# --- GET, PUT, DELETE por id_movimiento ---
@movimiento_bp.route('/<int:id_movimiento>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def handle_movimiento(id_movimiento):
    id_usuario_loggeado = request.user_id

    if request.method == 'GET':
        # --- READ ONE ---
        sql = "SELECT * FROM movimiento WHERE id_movimiento = %s"
        try:
            movimiento = execute_query(sql, (id_movimiento,), fetch=True)
            if movimiento:
                return jsonify(movimiento[0]), 200
            return jsonify({"error": "Movimiento no encontrado."}), 404
        except Exception as e:
            print(f"Error en GET /api/movimiento/{id_movimiento}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener movimiento"}), 500

    elif request.method == 'PUT':
        # --- UPDATE ---
        data = request.get_json()

        # Obtenemos los campos de Movimiento. Los campos de Kardex no se actualizan en este endpoint
        tipo, fecha, glosa, observacion, id_cliente, id_documento, *rest = get_movimiento_fields(data)

        id_elaborador = id_usuario_loggeado

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
                print(f"Movimiento actualizado: id_movimiento={id_movimiento}, nuevo_elaborador={id_elaborador}")
                return jsonify({"mensaje": "Movimiento actualizado con éxito.", "id_movimiento": id_movimiento}), 200
            return jsonify({"error": "Movimiento no encontrado para actualizar."}), 404
        except Exception as e:
            print(f"Error en PUT /api/movimiento/{id_movimiento}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al actualizar movimiento. Verifica las FK.", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        # --- DELETE ---
        # ATENCIÓN: La restricción FOREIGN KEY ON DELETE CASCADE en la tabla 'kardex'
        # debe asegurar que al eliminar el movimiento, su registro de Kardex se elimine automáticamente.
        sql = "DELETE FROM movimiento WHERE id_movimiento = %s"
        try:
            row_count = execute_query(sql, (id_movimiento,))
            if row_count > 0:
                print(f"Movimiento eliminado: id_movimiento={id_movimiento}")
                return jsonify({
                    "mensaje": "Movimiento eliminado con éxito. Se eliminaron sus Kardex asociados.",
                    "id_movimiento": id_movimiento
                }), 200
            return jsonify({"error": "Movimiento no encontrado para eliminar."}), 404
        except Exception as e:
            print(f"Error en DELETE /api/movimiento/{id_movimiento}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al eliminar movimiento.", "detalle": str(e)}), 400