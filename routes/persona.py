from flask import Blueprint, request, jsonify
from db_config import execute_query
import sys
import re   # Para expresiones regulares
from security import token_required

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
        data.get('expedido'),
        data.get('correo'),
        data.get('telefono'),
        data.get('direccion')
    )


# --- Función de validación ---
def validar_datos_persona(numero_ci, telefono, correo):
    errores = []

    # Validar CI (solo 8 dígitos)
    if numero_ci and not re.fullmatch(r'\d{8}', str(numero_ci)):
        errores.append("El número de CI debe contener exactamente 8 dígitos.")

    # Validar teléfono (solo 8 dígitos)
    if telefono and not re.fullmatch(r'\d{8}', str(telefono)):
        errores.append("El teléfono debe contener exactamente 8 dígitos.")

    # Validar correo con dominios permitidos
    if correo:
        dominios_validos = [
            "gmail.com", "outlook.com", "hotmail.com",
            "live.com", "yahoo.com", "icloud.com", "protonmail.com"
        ]
        patron_correo = re.compile(
            r'^[\w\.-]+@(' + '|'.join(dominios_validos).replace('.', r'\.') + r')$'
        )

        if not patron_correo.fullmatch(correo.strip().lower()):
            errores.append("El correo debe tener un dominio válido: " + ", ".join(dominios_validos))

    return errores


# --- GET ALL / POST ---
@persona_bp.route('/', methods=['GET', 'POST'])
@token_required
def handle_personas():
    if request.method == 'POST':
        data = request.get_json()
        nombre, primer_apellido, segundo_apellido, numero_ci, complemento_ci, correo, telefono, direccion = get_persona_fields(data)
        es_cliente = data.get('es_cliente', False)

        if not nombre:
            return jsonify({"error": "El campo 'nombre' es obligatorio."}), 400

        # Validar CI, teléfono y correo
        errores = validar_datos_persona(numero_ci, telefono, correo)
        if errores:
            return jsonify({"errores": errores}), 400

        # Verificar si el correo ya existe
        if correo:
            check_email_sql = "SELECT id_persona FROM persona WHERE correo = %s"
            existing_email = execute_query(check_email_sql, (correo,), fetch=True)
            if existing_email:
                return jsonify({"error": "El correo ya está registrado en otra persona."}), 400

        sql = """
            INSERT INTO persona (nombre, primer_apellido, segundo_apellido, numero_ci, expedido, correo, telefono, direccion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_persona
        """
        params = (nombre, primer_apellido, segundo_apellido, numero_ci, complemento_ci, correo, telefono, direccion)

        try:
            results = execute_query(sql, params, fetch=True)
            id_persona = results[0]['id_persona']

            if es_cliente:
                sql_cliente = "INSERT INTO cliente (id_persona) VALUES (%s)"
                execute_query(sql_cliente, (id_persona,))

            persona_sql = """
                SELECT p.*, 
                        CASE WHEN c.id_cliente IS NOT NULL THEN TRUE ELSE FALSE END AS es_cliente
                FROM persona p
                LEFT JOIN cliente c ON p.id_persona = c.id_persona
                WHERE p.id_persona = %s
            """
            new_persona = execute_query(persona_sql, (id_persona,), fetch=True)[0]

            return jsonify({
                "mensaje": "Persona creada con éxito.",
                "persona": new_persona
            }), 201

        except Exception as e:
            print(f"Error en POST /api/persona/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al crear persona", "detalle": str(e)}), 400

    else:
        sql = """
            SELECT p.*, 
                    CASE WHEN c.id_cliente IS NOT NULL THEN TRUE ELSE FALSE END AS es_cliente
            FROM persona p
            LEFT JOIN cliente c ON p.id_persona = c.id_persona
            ORDER BY p.id_persona
        """
        try:
            personas = execute_query(sql, fetch=True)
            return jsonify(personas), 200
        except Exception as e:
            print(f"Error en GET /api/persona/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener lista de personas", "detalle": str(e)}), 500


# --- GET / PUT / DELETE por id_persona ---
@persona_bp.route('/<int:id_persona>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def handle_persona(id_persona):
    if request.method == 'GET':
        sql = """
            SELECT p.*, 
                    CASE WHEN c.id_cliente IS NOT NULL THEN TRUE ELSE FALSE END AS es_cliente
            FROM persona p
            LEFT JOIN cliente c ON p.id_persona = c.id_persona
            WHERE p.id_persona = %s
        """
        try:
            persona = execute_query(sql, (id_persona,), fetch=True)
            if persona:
                return jsonify(persona[0]), 200
            return jsonify({"error": "Persona no encontrada."}), 404
        except Exception as e:
            print(f"Error en GET /api/persona/{id_persona}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener persona", "detalle": str(e)}), 500

    elif request.method == 'PUT':
        data = request.get_json()
        nombre, primer_apellido, segundo_apellido, numero_ci, complemento_ci, correo, telefono, direccion = get_persona_fields(data)
        es_cliente = data.get('es_cliente', False)

        if not nombre:
            return jsonify({"error": "El campo 'nombre' es obligatorio."}), 400

        # Validar CI, teléfono y correo antes de actualizar
        errores = validar_datos_persona(numero_ci, telefono, correo)
        if errores:
            return jsonify({"errores": errores}), 400

        # Verificar si el nuevo correo ya está en uso por otra persona
        if correo:
            check_email_sql = "SELECT id_persona FROM persona WHERE correo = %s AND id_persona <> %s"
            existing_email = execute_query(check_email_sql, (correo, id_persona), fetch=True)
            if existing_email:
                return jsonify({"error": "El correo ya está registrado en otra persona."}), 400

        sql = """
            UPDATE persona SET 
                nombre = %s, primer_apellido = %s, segundo_apellido = %s,
                numero_ci = %s, expedido = %s, correo = %s,
                telefono = %s, direccion = %s 
            WHERE id_persona = %s
        """
        params = (nombre, primer_apellido, segundo_apellido, numero_ci, complemento_ci, correo, telefono, direccion, id_persona)

        try:
            row_count = execute_query(sql, params)

            if es_cliente:
                check_sql = "SELECT id_cliente FROM cliente WHERE id_persona = %s"
                exists = execute_query(check_sql, (id_persona,), fetch=True)
                if not exists:
                    execute_query("INSERT INTO cliente (id_persona) VALUES (%s)", (id_persona,))
            else:
                execute_query("DELETE FROM cliente WHERE id_persona = %s", (id_persona,))

            if row_count and row_count > 0:
                persona_sql = """
                    SELECT p.*, 
                            CASE WHEN c.id_cliente IS NOT NULL THEN TRUE ELSE FALSE END AS es_cliente
                    FROM persona p
                    LEFT JOIN cliente c ON p.id_persona = c.id_persona
                    WHERE p.id_persona = %s
                """
                updated_persona = execute_query(persona_sql, (id_persona,), fetch=True)[0]
                return jsonify({"mensaje": "Persona actualizada con éxito.", "persona": updated_persona}), 200

            return jsonify({"error": "Persona no encontrada para actualizar."}), 404
        except Exception as e:
            print(f"Error en PUT /api/persona/{id_persona}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al actualizar persona", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        try:
            execute_query("DELETE FROM cliente WHERE id_persona = %s", (id_persona,))
            row_count = execute_query("DELETE FROM persona WHERE id_persona = %s", (id_persona,))
            if row_count and row_count > 0:
                return jsonify({"mensaje": "Persona eliminada con éxito.", "id_persona": id_persona}), 200
            return jsonify({"error": "Persona no encontrada para eliminar."}), 404
        except Exception as e:
            print(f"Error en DELETE /api/persona/{id_persona}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al eliminar persona.", "detalle": str(e)}), 400
