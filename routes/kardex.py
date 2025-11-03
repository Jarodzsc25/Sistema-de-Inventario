from flask import Blueprint, request, jsonify
from db_config import execute_query
import sys
# --- AÑADIDO: Importar decorador de seguridad ---
from security import token_required

# Blueprint
kardex_bp = Blueprint('kardex_bp', __name__)


# --- GET y POST ---
@kardex_bp.route('/', methods=['GET', 'POST'])
@token_required # PROTEGIDO
def handle_kardex_entries():
    if request.method == 'POST':
        # --- CREATE (Crear nuevo registro de Kardex) ---
        data = request.get_json()
        id_movimiento = data.get('id_movimiento')
        id_producto = data.get('id_producto')
        cantidad = data.get('cantidad')
        unitario = data.get('unitario')
        suttotal = data.get('suttotal') # se llama así en tu BD

        # Validación
        if not all([id_movimiento, id_producto, cantidad, unitario]):
            return jsonify({
                "error": "Faltan campos obligatorios: id_movimiento, id_producto, cantidad, unitario."
            }), 400

        # Calcular subtotal si no se envía
        suttotal = suttotal if suttotal is not None else (cantidad * unitario)

        sql = """
            INSERT INTO kardex (id_movimiento, id_producto, cantidad, unitario, suttotal)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (id_movimiento, id_producto, cantidad, unitario, suttotal)

        try:
            #Ejecutar sin fetch para asegurar commit
            execute_query(sql, params)

            # Recuperar el registro recién insertado
            new_entry = execute_query(
                "SELECT * FROM kardex WHERE id_movimiento = %s AND id_producto = %s",
                (id_movimiento, id_producto),
                fetch=True
            )[0]

            print("Registro de Kardex insertado correctamente:", new_entry)

            return jsonify({
                "mensaje": "Registro de Kardex creado con éxito.",
                "registro": new_entry
            }), 201

        except Exception as e:
            print(f"Error en POST /api/kardex/: {e}", file=sys.stderr)
            return jsonify({
                "error": "Error al crear registro de Kardex. Verifique las claves y valores enviados.",
                "detalle": str(e)
            }), 400

    else:
        # --- READ ALL (Obtener todos los registros) ---
        sql = "SELECT * FROM kardex ORDER BY id_movimiento DESC, id_producto ASC"
        try:
            registros = execute_query(sql, fetch=True)
            return jsonify(registros), 200
        except Exception as e:
            print(f"Error en GET /api/kardex/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener lista de registros de Kardex"}), 500


# --- GET, PUT, DELETE por clave compuesta ---
@kardex_bp.route('/<int:id_movimiento>/<int:id_producto>', methods=['GET', 'PUT', 'DELETE'])
@token_required # PROTEGIDO
def handle_kardex_entry(id_movimiento, id_producto):
    if request.method == 'GET':
        # --- READ ONE ---
        sql = "SELECT * FROM kardex WHERE id_movimiento = %s AND id_producto = %s"
        try:
            entry = execute_query(sql, (id_movimiento, id_producto), fetch=True)
            if entry:
                return jsonify(entry[0]), 200
            return jsonify({"error": "Registro de Kardex no encontrado con esa clave compuesta."}), 404
        except Exception as e:
            print(f"Error en GET /api/kardex/{id_movimiento}/{id_producto}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener registro de Kardex"}), 500

    elif request.method == 'PUT':
        # --- UPDATE ---
        data = request.get_json()
        cantidad = data.get('cantidad')
        unitario = data.get('unitario')
        suttotal = data.get('suttotal')

        if not all([cantidad, unitario]):
            return jsonify({"error": "Los campos 'cantidad' y 'unitario' son obligatorios para actualizar."}), 400

        # Calcular subtotal si no se envía
        suttotal = suttotal if suttotal is not None else (cantidad * unitario)

        sql = """
            UPDATE kardex SET 
                cantidad = %s, unitario = %s, suttotal = %s
            WHERE id_movimiento = %s AND id_producto = %s
        """
        params = (cantidad, unitario, suttotal, id_movimiento, id_producto)

        try:
            row_count = execute_query(sql, params)
            if row_count and row_count > 0:
                updated_entry = execute_query(
                    "SELECT * FROM kardex WHERE id_movimiento = %s AND id_producto = %s",
                    (id_movimiento, id_producto),
                    fetch=True
                )[0]
                print("Registro de Kardex actualizado:", updated_entry)
                return jsonify({
                    "mensaje": "Registro de Kardex actualizado con éxito.",
                    "registro": updated_entry
                }), 200
            return jsonify({"error": "Registro no encontrado para actualizar."}), 404
        except Exception as e:
            print(f"Error en PUT /api/kardex/{id_movimiento}/{id_producto}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al actualizar registro de Kardex", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        # --- DELETE ---
        sql = "DELETE FROM kardex WHERE id_movimiento = %s AND id_producto = %s"
        try:
            row_count = execute_query(sql, (id_movimiento, id_producto))
            if row_count and row_count > 0:
                print(f"Registro de Kardex eliminado: movimiento={id_movimiento}, producto={id_producto}")
                return jsonify({
                    "mensaje": "Registro de Kardex eliminado con éxito.",
                    "id_movimiento": id_movimiento,
                    "id_producto": id_producto
                }), 200
            return jsonify({"error": "Registro no encontrado para eliminar."}), 404
        except Exception as e:
            print(f"Error en DELETE /api/kardex/{id_movimiento}/{id_producto}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al eliminar registro de Kardex.", "detalle": str(e)}), 400