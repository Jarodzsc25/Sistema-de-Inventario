from flask import Blueprint, request, jsonify
from db_config import execute_query

persona_bp = Blueprint('persona_bp', __name__)


# Funciones de utilidad para manejar los datos de Persona
def get_persona_fields(data):
    """Extrae y retorna los campos de persona de un diccionario."""
    return (
        data.get('nombre'),
        data.get('primer_apellido'),
        data.get('segundo_apellido'),
        data.get('numero_ci'),
        data.get('complemento_ci'),
        data.get('correo'),
        data.get('telefono'),
        data.get('direccion')
    )


# Obtener todas las personas y crear una nueva (GET y POST)
@persona_bp.route('/', methods=['GET', 'POST'])
def handle_personas():
    if request.method == 'POST':
        # --- CREATE (Crear nueva Persona) ---
        data = request.get_json()
        nombre, primer_apellido, segundo_apellido, numero_ci, complemento_ci, correo, telefono, direccion = get_persona_fields(
            data)

        if not nombre:
            return jsonify({"error": "El campo 'nombre' es obligatorio."}), 400

        sql = """
            INSERT INTO persona (nombre, primer_apellido, segundo_apellido, numero_ci, complemento_ci, correo, telefono, direccion) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
            RETURNING id_persona
        """
        params = (nombre, primer_apellido, segundo_apellido, numero_ci, complemento_ci, correo, telefono, direccion)

        try:
            results = execute_query(sql, params, fetch=True)
            new_id = results[0]['id_persona'] if results else None
            return jsonify({
                "mensaje": "Persona creada con éxito.",
                "id_persona": new_id,
                "nombre": nombre
            }), 201
        except Exception as e:
            return jsonify({"error": "Error al crear persona", "detalle": str(e)}), 400

    else:
        # --- READ ALL (Obtener todas las Personas) ---
        sql = "SELECT * FROM persona ORDER BY id_persona"
        try:
            personas = execute_query(sql, fetch=True)
            return jsonify(personas), 200
        except Exception:
            return jsonify({"error": "Error al obtener lista de personas"}), 500


# Obtener, actualizar o eliminar una Persona por ID (GET, PUT, DELETE)
@persona_bp.route('/<int:id_persona>', methods=['GET', 'PUT', 'DELETE'])
def handle_persona(id_persona):
    if request.method == 'GET':
        # --- READ ONE (Obtener una Persona) ---
        sql = "SELECT * FROM persona WHERE id_persona = %s"
        try:
            persona = execute_query(sql, (id_persona,), fetch=True)
            if persona:
                return jsonify(persona[0]), 200
            return jsonify({"error": "Persona no encontrada."}), 404
        except Exception:
            return jsonify({"error": "Error al obtener persona"}), 500

    elif request.method == 'PUT':
        # --- UPDATE (Actualizar Persona) ---
        data = request.get_json()
        nombre, primer_apellido, segundo_apellido, numero_ci, complemento_ci, correo, telefono, direccion = get_persona_fields(
            data)

        if not nombre:
            return jsonify({"error": "El campo 'nombre' es obligatorio."}), 400

        sql = """
            UPDATE persona SET 
                nombre = %s, primer_apellido = %s, segundo_apellido = %s, 
                numero_ci = %s, complemento_ci = %s, correo = %s, 
                telefono = %s, direccion = %s 
            WHERE id_persona = %s
        """
        params = (nombre, primer_apellido, segundo_apellido, numero_ci, complemento_ci, correo, telefono, direccion,
                  id_persona)

        try:
            row_count = execute_query(sql, params)
            if row_count > 0:
                return jsonify({"mensaje": "Persona actualizada con éxito.", "id_persona": id_persona}), 200
            return jsonify({"error": "Persona no encontrada para actualizar."}), 404
        except Exception as e:
            return jsonify({"error": "Error al actualizar persona", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        # --- DELETE (Eliminar Persona) ---
        sql = "DELETE FROM persona WHERE id_persona = %s"
        try:
            row_count = execute_query(sql, (id_persona,))
            if row_count > 0:
                return jsonify({"mensaje": "Persona eliminada con éxito.", "id_persona": id_persona}), 200
            return jsonify({"error": "Persona no encontrada para eliminar."}), 404
        except Exception as e:
            # CASCADE está activado, si es un usuario se borra de usuario también.
            return jsonify({"error": "Error al eliminar persona.", "detalle": str(e)}), 400