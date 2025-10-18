from flask import Blueprint, request, jsonify
from db_config import execute_query

distribuidor_bp = Blueprint('distribuidor_bp', __name__)


# Obtener todos los distribuidores y crear uno nuevo (GET y POST)
@distribuidor_bp.route('/', methods=['GET', 'POST'])
def handle_distribuidores():
    if request.method == 'POST':
        # --- CREATE (Crear nuevo Distribuidor) ---
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
            return jsonify({
                "mensaje": "Distribuidor creado con éxito.",
                "id_distribuidor": new_id,
                "nombre": nombre
            }), 201
        except Exception as e:
            return jsonify({"error": "Error al crear distribuidor", "detalle": str(e)}), 400

    else:
        # --- READ ALL (Obtener todos los Distribuidores) ---
        sql = "SELECT * FROM distribuidor ORDER BY id_distribuidor"
        try:
            distribuidores = execute_query(sql, fetch=True)
            return jsonify(distribuidores), 200
        except Exception:
            return jsonify({"error": "Error al obtener lista de distribuidores"}), 500


# Obtener, actualizar o eliminar un Distribuidor por ID (GET, PUT, DELETE)
@distribuidor_bp.route('/<int:id_distribuidor>', methods=['GET', 'PUT', 'DELETE'])
def handle_distribuidor(id_distribuidor):
    if request.method == 'GET':
        # --- READ ONE (Obtener un Distribuidor) ---
        sql = "SELECT * FROM distribuidor WHERE id_distribuidor = %s"
        try:
            distribuidor = execute_query(sql, (id_distribuidor,), fetch=True)
            if distribuidor:
                return jsonify(distribuidor[0]), 200
            return jsonify({"error": "Distribuidor no encontrado."}), 404
        except Exception:
            return jsonify({"error": "Error al obtener distribuidor"}), 500

    elif request.method == 'PUT':
        # --- UPDATE (Actualizar Distribuidor) ---
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
                return jsonify(
                    {"mensaje": "Distribuidor actualizado con éxito.", "id_distribuidor": id_distribuidor}), 200
            return jsonify({"error": "Distribuidor no encontrado para actualizar."}), 404
        except Exception as e:
            return jsonify({"error": "Error al actualizar distribuidor", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        # --- DELETE (Eliminar Distribuidor) ---
        sql = "DELETE FROM distribuidor WHERE id_distribuidor = %s"
        try:
            row_count = execute_query(sql, (id_distribuidor,))
            if row_count > 0:
                return jsonify(
                    {"mensaje": "Distribuidor eliminado con éxito.", "id_distribuidor": id_distribuidor}), 200
            return jsonify({"error": "Distribuidor no encontrado para eliminar."}), 404
        except Exception as e:
            # Restrict violation es común aquí (si hay productos asociados)
            return jsonify({"error": "Error al eliminar distribuidor. Puede que tenga Productos asociados.",
                            "detalle": str(e)}), 400