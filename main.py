from flask import Flask, request, jsonify, render_template
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from psycopg2 import connect, extras

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)

DB_CONFIG = {
    "host": "localhost",
    "database": "ventas",
    "user": "postgres",
    "password": "latorrededruaka",
    "port": "5432"
}

def get_connection():
    return connect(**DB_CONFIG)

# =====================
# LOGIN
# =====================
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
        del user['password']
        return jsonify({"mensaje": "Login exitoso", "usuario": user}), 200
    else:
        return jsonify({"error": "Usuario o contraseña incorrectos"}), 401

# =====================
# RUTAS HTML
# =====================
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

# =====================
# CRUD Distribuidor
# =====================
@app.route('/distribuidores', methods=['GET'])
def obtener_distribuidores():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM distribuidor ORDER BY id_distribuidor ASC;")
    distribuidores = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(distribuidores)

@app.route('/distribuidores', methods=['POST'])
def agregar_distribuidor():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO distribuidor (nit, nombre, contacto, telefono, direccion)
        VALUES (%s, %s, %s, %s, %s) RETURNING id_distribuidor;
    """, (data['nit'], data['nombre'], data.get('contacto'), data.get('telefono'), data.get('direccion')))
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Distribuidor agregado', 'id_distribuidor': id_nuevo})

@app.route('/distribuidores/<int:id_distribuidor>', methods=['PUT'])
def actualizar_distribuidor(id_distribuidor):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE distribuidor
        SET nit=%s, nombre=%s, contacto=%s, telefono=%s, direccion=%s
        WHERE id_distribuidor=%s;
    """, (data['nit'], data['nombre'], data.get('contacto'), data.get('telefono'), data.get('direccion'), id_distribuidor))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Distribuidor actualizado'})

@app.route('/distribuidores/<int:id_distribuidor>', methods=['DELETE'])
def eliminar_distribuidor(id_distribuidor):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM distribuidor WHERE id_distribuidor = %s;", (id_distribuidor,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Distribuidor eliminado'})

# =====================
# CRUD Producto
# =====================
@app.route('/productos', methods=['GET'])
def obtener_productos():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""
        SELECT p.*, d.nombre AS distribuidor_nombre
        FROM producto p
        JOIN distribuidor d ON p.id_distribuidor = d.id_distribuidor
        ORDER BY p.id_producto ASC;
    """)
    productos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(productos)

@app.route('/productos', methods=['POST'])
def agregar_producto():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO producto (codigo, nombre, descripcion, unidad, id_distribuidor)
        VALUES (%s, %s, %s, %s, %s) RETURNING id_producto;
    """, (data['codigo'], data['nombre'], data.get('descripcion'), data.get('unidad'), data['id_distribuidor']))
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Producto agregado', 'id_producto': id_nuevo})

@app.route('/productos/<int:id_producto>', methods=['PUT'])
def actualizar_producto(id_producto):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE producto
        SET codigo=%s, nombre=%s, descripcion=%s, unidad=%s, id_distribuidor=%s
        WHERE id_producto=%s;
    """, (data['codigo'], data['nombre'], data.get('descripcion'), data.get('unidad'), data['id_distribuidor'], id_producto))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Producto actualizado'})

@app.route('/productos/<int:id_producto>', methods=['DELETE'])
def eliminar_producto(id_producto):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM producto WHERE id_producto = %s;", (id_producto,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Producto eliminado'})

# =====================
# Ejecutar servidor
# =====================
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
