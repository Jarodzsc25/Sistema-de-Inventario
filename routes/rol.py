from flask import Blueprint, request, jsonify
from db_config import execute_query
import sys  # Para logging detallado en consola

# Blueprint para Rol
rol_bp = Blueprint('rol_bp', __name__)

# --- GET y POST ---
@rol_bp.route('/', methods=['GET', 'POST'])
def handle_roles():
    if request.method == 'POST':
        # --- CREATE (Crear nuevo Rol) ---
        data = request.get_json()
        nombre = data.get('nombre')

        if not nombre:
            return jsonify({"error": "Falta el campo 'nombre'."}), 400

        sql = "INSERT INTO rol (nombre) VALUES (%s)"
        params = (nombre,)

        try:
            # Ejecutar sin fetch para asegurar commit
            execute_query(sql, params)

            # Recuperar el rol recién creado (último insertado)
            new_rol = execute_query(
                "SELECT * FROM rol ORDER BY id_rol DESC LIMIT 1",
                fetch=True
            )[0]

            print("Rol insertado correctamente:", new_rol)

            return jsonify({
                "mensaje": "Rol creado con éxito.",
                "rol": new_rol
            }), 201

        except Exception as e:
            print(f"Error en POST /api/rol/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al crear rol", "detalle": str(e)}), 400

    else:
        # --- READ ALL (Obtener todos los Roles) ---
        sql = "SELECT id_rol, nombre FROM rol ORDER BY id_rol"
        try:
            roles = execute_query(sql, fetch=True)
            return jsonify(roles), 200
        except Exception as e:
            print(f"Error en GET /api/rol/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener lista de roles"}), 500


# --- GET, PUT y DELETE por ID ---
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
        except Exception as e:
            print(f"Error en GET /api/rol/{id_rol}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener rol"}), 500

    elif request.method == 'PUT':
        # --- UPDATE (Actualizar Rol) ---
        data = request.get_json()
        nombre = data.get('nombre')

        if not nombre:
            return jsonify({"error": "Falta el campo 'nombre'."}), 400

        sql = "UPDATE rol SET nombre = %s WHERE id_rol = %s"
        params = (nombre, id_rol)

        try:
            row_count = execute_query(sql, params)
            if row_count and row_count > 0:
                updated_rol = execute_query(
                    "SELECT * FROM rol WHERE id_rol = %s",
                    (id_rol,),
                    fetch=True
                )[0]
                print("Rol actualizado:", updated_rol)
                return jsonify({
                    "mensaje": "Rol actualizado con éxito.",
                    "rol": updated_rol
                }), 200
            return jsonify({"error": "Rol no encontrado para actualizar."}), 404
        except Exception as e:
            print(f"Error en PUT /api/rol/{id_rol}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al actualizar rol", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        # --- DELETE (Eliminar Rol) ---
        sql = "DELETE FROM rol WHERE id_rol = %s"
        try:
            row_count = execute_query(sql, (id_rol,))
            if row_count and row_count > 0:
                print(f"Rol eliminado: id_rol={id_rol}")
                return jsonify({
                    "mensaje": "Rol eliminado con éxito.",
                    "id_rol": id_rol
                }), 200
            return jsonify({"error": "Rol no encontrado para eliminar."}), 404
        except Exception as e:
            print(f"Error en DELETE /api/rol/{id_rol}: {e}", file=sys.stderr)
            return jsonify({
                "error": "Error al eliminar rol. Puede estar asignado a un usuario.",
                "detalle": str(e)
            }), 400
