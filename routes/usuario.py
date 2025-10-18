from flask import Blueprint, request, jsonify
from db_config import execute_query
# Usaremos una simulación de hash simple, en un ambiente real se debe usar bcrypt/passlib
import base64

usuario_bp = Blueprint('usuario_bp', __name__)


# Función para simular el hashing (solo para este ejemplo de CRUD)
def hash_password(password):
    """Simulación simple de hash de contraseña."""
    return base64.b64encode(password.encode()).decode()


# Obtener todos los usuarios y crear uno nuevo (GET y POST)
@usuario_bp.route('/', methods=['GET', 'POST'])
def handle_usuarios():
    if request.method == 'POST':
        # --- CREATE (Crear nuevo Usuario) ---
        data = request.get_json()
        id_usuario = data.get('id_usuario')
        username = data.get('username')
        password = data.get('password')
        id_rol = data.get('id_rol')

        if not all([id_usuario, username, password, id_rol]):
            return jsonify({"error": "Faltan campos obligatorios: id_usuario, username, password, id_rol."}), 400

        # Simulación de hash de contraseña
        hashed_password = hash_password(password)

        sql = "INSERT INTO usuario (id_usuario, username, password, id_rol) VALUES (%s, %s, %s, %s)"
        params = (id_usuario, username, hashed_password, id_rol)

        try:
            execute_query(sql, params)
            return jsonify({
                "mensaje": "Usuario creado con éxito.",
                "id_usuario": id_usuario,
                "username": username
            }), 201
        except Exception as e:
            return jsonify({
                               "error": "Error al crear usuario. Verifica que id_usuario y id_rol existan, o si el username ya está en uso.",
                               "detalle": str(e)}), 400

    else:
        # --- READ ALL (Obtener todos los Usuarios) ---
        # Se unen con persona y rol para dar más contexto
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
        except Exception:
            return jsonify({"error": "Error al obtener lista de usuarios"}), 500


# Obtener, actualizar o eliminar un Usuario por ID (GET, PUT, DELETE)
@usuario_bp.route('/<int:id_usuario>', methods=['GET', 'PUT', 'DELETE'])
def handle_usuario(id_usuario):
    if request.method == 'GET':
        # --- READ ONE (Obtener un Usuario) ---
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
        except Exception:
            return jsonify({"error": "Error al obtener usuario"}), 500

    elif request.method == 'PUT':
        # --- UPDATE (Actualizar Usuario) ---
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')  # Opcional
        id_rol = data.get('id_rol')  # Opcional

        if not username and not password and not id_rol:
            return jsonify(
                {"error": "Al menos uno de los campos (username, password, id_rol) debe estar presente."}), 400

        updates = []
        params = []

        if username:
            updates.append("username = %s")
            params.append(username)
        if password:
            # Simulación de hash de contraseña al actualizar
            hashed_password = hash_password(password)
            updates.append("password = %s")
            params.append(hashed_password)
        if id_rol:
            updates.append("id_rol = %s")
            params.append(id_rol)

        sql = f"UPDATE usuario SET {', '.join(updates)} WHERE id_usuario = %s"
        params.append(id_usuario)

        try:
            row_count = execute_query(sql, tuple(params))
            if row_count > 0:
                return jsonify({"mensaje": "Usuario actualizado con éxito.", "id_usuario": id_usuario}), 200
            return jsonify({"error": "Usuario no encontrado para actualizar."}), 404
        except Exception as e:
            return jsonify({"error": "Error al actualizar usuario", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        # --- DELETE (Eliminar Usuario) ---
        # La tabla usuario tiene FK a persona con ON DELETE CASCADE, por lo que
        # al eliminar el usuario, se debe eliminar la persona asociada.
        # Pero según tu DDL, la FK va de Usuario(id_usuario) a Persona(id_persona),
        # lo que significa que el ID ya debe existir en Persona.
        # Para eliminar un usuario, simplemente lo borramos de la tabla usuario.

        sql = "DELETE FROM usuario WHERE id_usuario = %s"
        try:
            row_count = execute_query(sql, (id_usuario,))
            if row_count > 0:
                # OJO: La persona asociada (id_persona) seguirá existiendo.
                # Si deseas eliminar la persona también, borra en /api/persona/<id_usuario>
                return jsonify(
                    {"mensaje": "Usuario (solo el acceso) eliminado con éxito.", "id_usuario": id_usuario}), 200
            return jsonify({"error": "Usuario no encontrado para eliminar."}), 404
        except Exception as e:
            return jsonify({"error": "Error al eliminar usuario", "detalle": str(e)}), 400
