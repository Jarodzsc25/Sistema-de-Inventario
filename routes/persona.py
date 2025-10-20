from flask import Blueprint, request, jsonify
from db_config import execute_query
import sys  # Para logging detallado

# Define el Blueprint para las rutas de Persona
persona_bp = Blueprint('persona_bp', __name__)

# --- Función de utilidad ---
def get_persona_fields(data):
    """
    Extrae y retorna los campos de persona de un diccionario,
    alineado con el esquema de la tabla.
    """
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

# --- Rutas principales ---
@persona_bp.route('/', methods=['GET', 'POST'])
def handle_personas():
    if request.method == 'POST':
        # --- CREATE ---
        data = request.get_json()
        nombre, primer_apellido, segundo_apellido, numero_ci, complemento_ci, correo, telefono, direccion = get_persona_fields(data)

        # Validación mínima
        if not nombre:
            return jsonify({"error": "El campo 'nombre' es obligatorio."}), 400

        sql = """
            INSERT INTO persona (nombre, primer_apellido, segundo_apellido, numero_ci, complemento_ci, correo, telefono, direccion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_persona
        """
        params = (nombre, primer_apellido, segundo_apellido, numero_ci, complemento_ci, correo, telefono, direccion)

        try:
            # Ejecutar sin fetch para asegurar commit
            execute_query(sql, params)

            # Recuperar la persona recién creada (último registro)
            new_persona = execute_query(
                "SELECT * FROM persona ORDER BY id_persona DESC LIMIT 1",
                fetch=True
            )[0]

            print("Persona insertada correctamente:", new_persona)

            return jsonify({
                "mensaje": "Persona creada con éxito.",
                "persona": new_persona
            }), 201

        except Exception as e:
            print(f"Error en POST /api/persona/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al crear persona", "detalle": str(e)}), 400

    else:
        # --- READ ALL ---
        sql = "SELECT * FROM persona ORDER BY id_persona"
        try:
            personas = execute_query(sql, fetch=True)
            return jsonify(personas), 200
        except Exception as e:
            print(f"Error en GET /api/persona/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener lista de personas", "detalle": str(e)}), 500


@persona_bp.route('/<int:id_persona>', methods=['GET', 'PUT', 'DELETE'])
def handle_persona(id_persona):
    if request.method == 'GET':
        # --- READ ONE ---
        sql = "SELECT * FROM persona WHERE id_persona = %s"
        try:
            persona = execute_query(sql, (id_persona,), fetch=True)
            if persona:
                return jsonify(persona[0]), 200
            return jsonify({"error": "Persona no encontrada."}), 404
        except Exception as e:
            print(f"Error en GET /api/persona/{id_persona}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener persona", "detalle": str(e)}), 500

    elif request.method == 'PUT':
        # --- UPDATE ---
        data = request.get_json()
        nombre, primer_apellido, segundo_apellido, numero_ci, complemento_ci, correo, telefono, direccion = get_persona_fields(data)

        if not nombre:
            return jsonify({"error": "El campo 'nombre' es obligatorio."}), 400

        sql = """
            UPDATE persona SET 
                nombre = %s, primer_apellido = %s, segundo_apellido = %s,
                numero_ci = %s, complemento_ci = %s, correo = %s,
                telefono = %s, direccion = %s 
            WHERE id_persona = %s
        """
        params = (nombre, primer_apellido, segundo_apellido, numero_ci, complemento_ci, correo, telefono, direccion, id_persona)

        try:
            row_count = execute_query(sql, params)
            if row_count and row_count > 0:
                return jsonify({"mensaje": "Persona actualizada con éxito.", "id_persona": id_persona}), 200
            return jsonify({"error": "Persona no encontrada para actualizar."}), 404
        except Exception as e:
            print(f"Error en PUT /api/persona/{id_persona}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al actualizar persona", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        # --- DELETE ---
        sql = "DELETE FROM persona WHERE id_persona = %s"
        try:
            row_count = execute_query(sql, (id_persona,))
            if row_count and row_count > 0:
                return jsonify({"mensaje": "Persona eliminada con éxito.", "id_persona": id_persona}), 200
            return jsonify({"error": "Persona no encontrada para eliminar."}), 404
        except Exception as e:
            print(f"Error en DELETE /api/persona/{id_persona}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al eliminar persona.", "detalle": str(e)}), 400
