from flask import Blueprint, request, jsonify
from db_config import execute_query
import base64
import sys  # Para logging de errores en consola



usuario_bp = Blueprint('usuario_bp', __name__)

# --- Función de hash (solo ejemplo, en producción usar bcrypt/passlib) ---
def hash_password(password):
    """Simulación simple de hash de contraseña."""
    return base64.b64encode(password.encode()).decode()

# --- GET y POST ---
@usuario_bp.route('/', methods=['GET', 'POST'])
def handle_usuarios():
    if request.method == 'POST':
        # --- CREATE (Crear Usuario) ---
        data = request.get_json()
        id_usuario = data.get('id_usuario')
        username = data.get('username')
        password = data.get('password')
        id_rol = data.get('id_rol')

        if not all([id_usuario, username, password, id_rol]):
            return jsonify({"error": "Faltan campos obligatorios: id_usuario, username, password, id_rol."}), 400

        hashed_password = hash_password(password)

        sql = "INSERT INTO usuario (id_usuario, username, password, id_rol) VALUES (%s, %s, %s, %s)"
        params = (id_usuario, username, hashed_password, id_rol)

        try:
            execute_query(sql, params)
            print(f"Usuario creado: {username} (id_usuario={id_usuario})")
            return jsonify({
                "mensaje": "Usuario creado con éxito.",
                "usuario": {
                    "id_usuario": id_usuario,
                    "username": username,
                    "id_rol": id_rol
                }
            }), 201
        except Exception as e:
            print(f"Error en POST /api/usuario/: {e}", file=sys.stderr)
            return jsonify({
                "error": "Error al crear usuario. Verifica id_usuario, id_rol o username duplicado.",
                "detalle": str(e)
            }), 400

    else:
        # --- READ ALL (Obtener todos los usuarios) ---
        sql = """
            SELECT 
                u.id_usuario, u.username, u.id_rol, 
                r.nombre AS rol_nombre,
                p.nombre AS nombre_persona, p.primer_apellido
            FROM usuario u
            JOIN persona p ON u.id_usuario = p.id_persona
            JOIN rol r ON u.id_rol = r.id_rol
            ORDER BY u.id_usuario
        """
        try:
            usuarios = execute_query(sql, fetch=True)
            return jsonify(usuarios), 200
        except Exception as e:
            print(f"Error en GET /api/usuario/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener lista de usuarios"}), 500

# --- GET, PUT, DELETE por id_usuario ---
@usuario_bp.route('/<int:id_usuario>', methods=['GET', 'PUT', 'DELETE'])
def handle_usuario(id_usuario):
    if request.method == 'GET':
        # --- READ ONE ---
        sql = """
            SELECT 
                u.id_usuario, u.username, u.id_rol, 
                r.nombre AS rol_nombre,
                p.nombre AS nombre_persona, p.primer_apellido
            FROM usuario u
            JOIN persona p ON u.id_usuario = p.id_persona
            JOIN rol r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = %s
        """
        try:
            usuario = execute_query(sql, (id_usuario,), fetch=True)
            if usuario:
                return jsonify(usuario[0]), 200
            return jsonify({"error": "Usuario no encontrado."}), 404
        except Exception as e:
            print(f"Error en GET /api/usuario/{id_usuario}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener usuario"}), 500

    elif request.method == 'PUT':
        # --- UPDATE ---
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        id_rol = data.get('id_rol')

        if not any([username, password, id_rol]):
            return jsonify({"error": "Al menos uno de los campos (username, password, id_rol) debe estar presente."}), 400

        updates = []
        params = []

        if username:
            updates.append("username = %s")
            params.append(username)
        if password:
            updates.append("password = %s")
            params.append(hash_password(password))
        if id_rol:
            updates.append("id_rol = %s")
            params.append(id_rol)

        sql = f"UPDATE usuario SET {', '.join(updates)} WHERE id_usuario = %s"
        params.append(id_usuario)

        try:
            row_count = execute_query(sql, tuple(params))
            if row_count > 0:
                print(f"Usuario actualizado: id_usuario={id_usuario}")
                return jsonify({"mensaje": "Usuario actualizado con éxito.", "id_usuario": id_usuario}), 200
            return jsonify({"error": "Usuario no encontrado para actualizar."}), 404
        except Exception as e:
            print(f"rror en PUT /api/usuario/{id_usuario}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al actualizar usuario", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        # --- DELETE ---
        sql = "DELETE FROM usuario WHERE id_usuario = %s"
        try:
            row_count = execute_query(sql, (id_usuario,))
            if row_count > 0:
                print(f"Usuario eliminado: id_usuario={id_usuario}")
                return jsonify({"mensaje": "Usuario eliminado con éxito.", "id_usuario": id_usuario}), 200
            return jsonify({"error": "Usuario no encontrado para eliminar."}), 404
        except Exception as e:
            print(f"Error en DELETE /api/usuario/{id_usuario}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al eliminar usuario", "detalle": str(e)}), 400
