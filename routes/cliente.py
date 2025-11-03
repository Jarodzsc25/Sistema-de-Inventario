from flask import Blueprint, request, jsonify
from db_config import execute_query
from datetime import datetime
import sys
from security import token_required

# Blueprint Corregido (Eliminar strict_slashes=False del constructor)
cliente_bp = Blueprint('cliente_bp', __name__)


# --- GET ALL / POST ---
# Aplicar strict_slashes=False a la ruta principal para evitar 308
@cliente_bp.route('/', methods=['GET', 'POST'], strict_slashes=False)
@token_required
def handle_clientes(current_user):
    if request.method == 'POST':
        # --- CREATE ---
        data = request.get_json()
        id_persona = data.get('id_persona')

        if not id_persona:
            return jsonify({"error": "Falta el campo 'id_persona'."}), 400

        sql = "INSERT INTO cliente (id_persona) VALUES (%s) RETURNING id_cliente"
        try:
            results = execute_query(sql, (id_persona,), fetch=True)
            new_id = results[0]['id_cliente'] if results else None
            return jsonify({
                "mensaje": "Cliente creado con éxito.",
                "cliente": {
                    "id_cliente": new_id,
                    "id_persona": id_persona
                }
            }), 201
        except Exception as e:
            print(f"Error en POST /api/cliente/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al crear cliente", "detalle": str(e)}), 400

    else:
        # --- READ ALL ---
        sql = """
            SELECT c.id_cliente, p.id_persona, p.nombre, p.primer_apellido, p.segundo_apellido,
                   p.numero_ci, p.complemento_ci, p.correo, p.telefono, p.direccion
            FROM cliente c
            JOIN persona p ON c.id_persona = p.id_persona
            ORDER BY c.id_cliente DESC
        """
        try:
            clientes = execute_query(sql, fetch=True)
            return jsonify(clientes), 200
        except Exception as e:
            print(f"Error en GET /api/cliente/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener lista de clientes"}), 500


# --- GET / PUT / DELETE por id_cliente ---
@cliente_bp.route('/<int:id_cliente>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def handle_cliente(current_user, id_cliente):
    if request.method == 'GET':
        sql = """
            SELECT c.id_cliente, p.id_persona, p.nombre, p.primer_apellido, p.segundo_apellido,
                   p.numero_ci, p.complemento_ci, p.correo, p.telefono, p.direccion
            FROM cliente c
            JOIN persona p ON c.id_persona = p.id_persona
            WHERE c.id_cliente = %s
        """
        try:
            cliente = execute_query(sql, (id_cliente,), fetch=True)
            if cliente:
                return jsonify(cliente[0]), 200
            return jsonify({"error": "Cliente no encontrado."}), 404
        except Exception as e:
            print(f"Error en GET /api/cliente/{id_cliente}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener cliente"}), 500

    elif request.method == 'PUT':
        data = request.get_json()
        nueva_persona = data.get('id_persona')

        if not nueva_persona:
            return jsonify({"error": "Falta el campo 'id_persona'."}), 400

        sql = "UPDATE cliente SET id_persona = %s WHERE id_cliente = %s"
        try:
            row_count = execute_query(sql, (nueva_persona, id_cliente))
            if row_count > 0:
                return jsonify({"mensaje": "Cliente actualizado con éxito.", "id_cliente": id_cliente}), 200
            return jsonify({"error": "Cliente no encontrado."}), 404
        except Exception as e:
            print(f"Error en PUT /api/cliente/{id_cliente}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al actualizar cliente", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        sql = "DELETE FROM cliente WHERE id_cliente = %s"
        try:
            row_count = execute_query(sql, (id_cliente,))
            if row_count > 0:
                return jsonify({"mensaje": "Cliente eliminado con éxito.", "id_cliente": id_cliente}), 200
            return jsonify({"error": "Cliente no encontrado."}), 404
        except Exception as e:
            print(f"Error en DELETE /api/cliente/{id_cliente}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al eliminar cliente", "detalle": str(e)}), 400