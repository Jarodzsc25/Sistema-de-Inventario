from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import extras

from flask_bcrypt import Bcrypt
from flask_cors import CORS


app = Flask(__name__)

#Conexión a la base de datos PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "database": "ventas",
    "user": "postgres",
    "password": "latorrededruaka",
    "port": "5432"
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


#Ruta principal (para probar conexión)
@app.route('/')
def index():
    return "✅ API funcionando correctamente. Usa /personas"


#Obtener todas las personas
@app.route('/personas', methods=['GET'])
def get_personas():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM persona ORDER BY id_persona ASC;")
    personas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(personas)


#Obtener una persona por ID
@app.route('/personas/<int:id_persona>', methods=['GET'])
def get_persona(id_persona):
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM persona WHERE id_persona = %s;", (id_persona,))
    persona = cur.fetchone()
    cur.close()
    conn.close()

    if persona:
        return jsonify(persona)
    return jsonify({"error": "Persona no encontrada"}), 404


#Crear nueva persona
@app.route('/personas', methods=['POST'])
def create_persona():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO persona (nombre, primer_apellido, segundo_apellido, numero_ci, complemento_ci, correo, telefono, direccion)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        RETURNING id_persona;
    """, (
        data.get('nombre'),
        data.get('primer_apellido'),
        data.get('segundo_apellido'),
        data.get('numero_ci'),
        data.get('complemento_ci'),
        data.get('correo'),
        data.get('telefono'),
        data.get('direccion')
    ))

    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensaje": "Persona creada correctamente", "id_persona": id_nuevo}), 201


#Editar persona
@app.route('/personas/<int:id_persona>', methods=['PUT'])
def update_persona(id_persona):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE persona
        SET nombre=%s, primer_apellido=%s, segundo_apellido=%s, numero_ci=%s, complemento_ci=%s, correo=%s, telefono=%s, direccion=%s
        WHERE id_persona=%s;
    """, (
        data.get('nombre'),
        data.get('primer_apellido'),
        data.get('segundo_apellido'),
        data.get('numero_ci'),
        data.get('complemento_ci'),
        data.get('correo'),
        data.get('telefono'),
        data.get('direccion'),
        id_persona
    ))

    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Persona actualizada correctamente"})


#Eliminar persona
@app.route('/personas/<int:id_persona>', methods=['DELETE'])
def delete_persona(id_persona):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM persona WHERE id_persona = %s;", (id_persona,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"mensaje": "Persona eliminada correctamente"})






bcrypt = Bcrypt(app)
CORS(app)

#Ruta para registrar usuario (asociado a una persona existente)
@app.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()

    # Encriptar contraseña antes de guardarla
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    try:
        cur.execute("""
            INSERT INTO usuario (id_usuario, username, password, id_rol)
            VALUES (%s, %s, %s, %s)
            RETURNING id_usuario;
        """, (
            data['id_persona'],   # id_usuario = id_persona
            data['username'],
            hashed_password,
            data['id_rol']
        ))
        conn.commit()
        new_id = cur.fetchone()[0]
        return jsonify({"mensaje": "Usuario creado correctamente", "id_usuario": new_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()


# 🔓 Ruta de login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""
        SELECT u.id_usuario, u.username, u.password, r.nombre AS rol, 
               p.nombre AS persona_nombre, p.primer_apellido, p.correo
        FROM usuario u
        JOIN rol r ON u.id_rol = r.id_rol
        JOIN persona p ON u.id_usuario = p.id_persona
        WHERE u.username = %s;
    """, (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user and bcrypt.check_password_hash(user['password'], password):
        # No devolvemos la contraseña
        del user['password']
        return jsonify({"mensaje": "Login exitoso", "usuario": user}), 200
    else:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401


#Iniciar servidor
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)