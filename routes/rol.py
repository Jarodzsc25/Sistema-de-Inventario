from flask import Blueprint, request, jsonify
from db_config import execute_query

rol_bp = Blueprint('rol_bp', __name__)


# Obtener todos los roles y crear uno nuevo (GET y POST)
@rol_bp.route('/', methods=['GET', 'POST'])
def handle_roles():
    if request.method == 'POST':
        # --- CREATE (Crear nuevo Rol) ---
        data = request.get_json()
        nombre = data.get('nombre')

        if not nombre:
            return jsonify({"error": "Falta el campo 'nombre'."}), 400

        sql = "INSERT INTO rol (nombre) VALUES (%s) RETURNING id_rol"
        try:
            # La función execute_query está diseñada para lanzar excepciones en caso de error.
            results = execute_query(sql, (nombre,), fetch=True)
            new_id = results[0]['id_rol'] if results else None
            return jsonify({
                "mensaje": "Rol creado con éxito.",
                "id_rol": new_id,
                "nombre": nombre
            }), 201
        except Exception as e:
            # La excepción se maneja globalmente en app.py, pero capturamos por seguridad
            return jsonify({"error": "Error al crear rol", "detalle": str(e)}), 400

    else:
        # --- READ ALL (Obtener todos los Roles) ---
        sql = "SELECT id_rol, nombre FROM rol ORDER BY id_rol"
        try:
            roles = execute_query(sql, fetch=True)
            return jsonify(roles), 200
        except Exception:
            # Si hay un error, el manejador global lo captura
            return jsonify({"error": "Error al obtener lista de roles"}), 500


# Obtener, actualizar o eliminar un Rol por ID (GET, PUT, DELETE)
@rol_bp.route('/<int:id_rol>', methods=['GET', 'PUT', 'DELETE'])
def handle_rol(id_rol):
    if request.method == 'GET':
        # --- READ ONE (Obtener un Rol) ---
        sql = "SELECT id_rol, nombre FROM rol WHERE id_rol = %s"
        try:
            rol = execute_query(sql, (id_rol,), fetch=True)
            if rol:
                return jsonify(rol[0]), 200
            return jsonify({"error": "Rol no encontrado."}), 404
        except Exception:
            return jsonify({"error": "Error al obtener rol"}), 500

    elif request.method == 'PUT':
        # --- UPDATE (Actualizar Rol) ---
        data = request.get_json()
        nombre = data.get('nombre')

        if not nombre:
            return jsonify({"error": "Falta el campo 'nombre'."}), 400

        sql = "UPDATE rol SET nombre = %s WHERE id_rol = %s"
        try:
            row_count = execute_query(sql, (nombre, id_rol))
            if row_count > 0:
                return jsonify({"mensaje": "Rol actualizado con éxito.", "id_rol": id_rol, "nombre": nombre}), 200
            return jsonify({"error": "Rol no encontrado para actualizar."}), 404
        except Exception as e:
            return jsonify({"error": "Error al actualizar rol", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        # --- DELETE (Eliminar Rol) ---
        sql = "DELETE FROM rol WHERE id_rol = %s"
        try:
            row_count = execute_query(sql, (id_rol,))
            if row_count > 0:
                return jsonify({"mensaje": "Rol eliminado con éxito.", "id_rol": id_rol}), 200
            return jsonify({"error": "Rol no encontrado para eliminar."}), 404
        except Exception as e:
            # Restrict violation es común aquí (si hay usuarios con este rol)
            return jsonify({"error": "Error al eliminar rol. Puede que esté siendo utilizado por un Usuario.",
                            "detalle": str(e)}), 400