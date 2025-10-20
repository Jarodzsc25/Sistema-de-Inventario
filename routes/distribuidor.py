from flask import Blueprint, request, jsonify
from db_config import execute_query
import sys

distribuidor_bp = Blueprint('distribuidor_bp', __name__)

# --- GET y POST ---
@distribuidor_bp.route('/', methods=['GET', 'POST'])
def handle_distribuidores():
    if request.method == 'POST':
        # --- CREATE ---
        data = request.get_json()
        nit = data.get('nit')
        nombre = data.get('nombre')
        contacto = data.get('contacto')
        telefono = data.get('telefono')
        direccion = data.get('direccion')

        if not all([nit, nombre]):
            return jsonify({"error": "Faltan campos obligatorios: nit, nombre."}), 400

        sql = """
            INSERT INTO distribuidor (nit, nombre, contacto, telefono, direccion) 
            VALUES (%s, %s, %s, %s, %s) 
            RETURNING id_distribuidor
        """
        params = (nit, nombre, contacto, telefono, direccion)

        try:
            results = execute_query(sql, params, fetch=True)
            new_id = results[0]['id_distribuidor'] if results else None
            print(f"Distribuidor creado: {nombre} (id_distribuidor={new_id})")
            return jsonify({
                "mensaje": "Distribuidor creado con éxito.",
                "distribuidor": {
                    "id_distribuidor": new_id,
                    "nombre": nombre,
                    "nit": nit
                }
            }), 201
        except Exception as e:
            print(f"Error en POST /api/distribuidor/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al crear distribuidor", "detalle": str(e)}), 400

    else:
        # --- READ ALL ---
        sql = "SELECT * FROM distribuidor ORDER BY id_distribuidor"
        try:
            distribuidores = execute_query(sql, fetch=True)
            return jsonify(distribuidores), 200
        except Exception as e:
            print(f"Error en GET /api/distribuidor/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener lista de distribuidores"}), 500

# --- GET, PUT, DELETE por id_distribuidor ---
@distribuidor_bp.route('/<int:id_distribuidor>', methods=['GET', 'PUT', 'DELETE'])
def handle_distribuidor(id_distribuidor):
    if request.method == 'GET':
        # --- READ ONE ---
        sql = "SELECT * FROM distribuidor WHERE id_distribuidor = %s"
        try:
            distribuidor = execute_query(sql, (id_distribuidor,), fetch=True)
            if distribuidor:
                return jsonify(distribuidor[0]), 200
            return jsonify({"error": "Distribuidor no encontrado."}), 404
        except Exception as e:
            print(f"Error en GET /api/distribuidor/{id_distribuidor}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener distribuidor"}), 500

    elif request.method == 'PUT':
        # --- UPDATE ---
        data = request.get_json()
        nit = data.get('nit')
        nombre = data.get('nombre')
        contacto = data.get('contacto')
        telefono = data.get('telefono')
        direccion = data.get('direccion')

        if not all([nit, nombre]):
            return jsonify({"error": "Los campos 'nit' y 'nombre' son obligatorios para actualizar."}), 400

        sql = """
            UPDATE distribuidor SET 
                nit = %s, nombre = %s, contacto = %s, 
                telefono = %s, direccion = %s 
            WHERE id_distribuidor = %s
        """
        params = (nit, nombre, contacto, telefono, direccion, id_distribuidor)

        try:
            row_count = execute_query(sql, params)
            if row_count > 0:
                print(f"Distribuidor actualizado: id_distribuidor={id_distribuidor}")
                return jsonify({
                    "mensaje": "Distribuidor actualizado con éxito.",
                    "id_distribuidor": id_distribuidor
                }), 200
            return jsonify({"error": "Distribuidor no encontrado para actualizar."}), 404
        except Exception as e:
            print(f"Error en PUT /api/distribuidor/{id_distribuidor}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al actualizar distribuidor", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        # --- DELETE ---
        sql = "DELETE FROM distribuidor WHERE id_distribuidor = %s"
        try:
            row_count = execute_query(sql, (id_distribuidor,))
            if row_count > 0:
                print(f"Distribuidor eliminado: id_distribuidor={id_distribuidor}")
                return jsonify({
                    "mensaje": "Distribuidor eliminado con éxito.",
                    "id_distribuidor": id_distribuidor
                }), 200
            return jsonify({"error": "Distribuidor no encontrado para eliminar."}), 404
        except Exception as e:
            print(f"Error en DELETE /api/distribuidor/{id_distribuidor}: {e}", file=sys.stderr)
            return jsonify({
                "error": "Error al eliminar distribuidor. Puede que tenga productos asociados.",
                "detalle": str(e)
            }), 400
