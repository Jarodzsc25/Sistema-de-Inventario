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
# CRUD DOCUMENTO
# =====================
@app.route('/documentos', methods=['GET'])
def obtener_documentos():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""
        SELECT * FROM documento ORDER BY id_documento ASC;
    """)
    documentos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(documentos)

@app.route('/documentos', methods=['POST'])
def agregar_documento():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO documento (numero, fecha)
        VALUES (%s, %s)
        RETURNING id_documento;
    """, (data['numero'], data['fecha']))
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Documento agregado', 'id_documento': id_nuevo})

@app.route('/documentos/<int:id_documento>', methods=['PUT'])
def actualizar_documento(id_documento):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE documento
        SET numero=%s, fecha=%s
        WHERE id_documento=%s;
    """, (data['numero'], data['fecha'], id_documento))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Documento actualizado'})

@app.route('/documentos/<int:id_documento>', methods=['DELETE'])
def eliminar_documento(id_documento):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM documento WHERE id_documento = %s;", (id_documento,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Documento eliminado'})


# =====================
# CRUD MOVIMIENTO
# =====================
@app.route('/movimientos', methods=['GET'])
def obtener_movimientos():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""
        SELECT 
            m.id_movimiento,
            m.tipo,
            m.fecha,
            m.glosa,
            m.observacion,
            u.username AS elaborado_por,
            p.nombre AS cliente,
            d.numero AS documento_numero
        FROM movimiento m
        LEFT JOIN usuario u ON m.id_elaborador = u.id_usuario
        LEFT JOIN persona p ON m.id_cliente = p.id_persona
        LEFT JOIN documento d ON m.id_documento = d.id_documento
        ORDER BY m.id_movimiento ASC;
    """)
    movimientos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(movimientos)

@app.route('/movimientos', methods=['POST'])
def agregar_movimiento():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO movimiento (tipo, fecha, glosa, observacion, id_elaborador, id_cliente, id_documento)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id_movimiento;
    """, (
        data['tipo'], data['fecha'], data.get('glosa'),
        data.get('observacion'), data.get('id_elaborador'),
        data.get('id_cliente'), data.get('id_documento')
    ))
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Movimiento agregado', 'id_movimiento': id_nuevo})

@app.route('/movimientos/<int:id_movimiento>', methods=['PUT'])
def actualizar_movimiento(id_movimiento):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE movimiento
        SET tipo=%s, fecha=%s, glosa=%s, observacion=%s, id_elaborador=%s, id_cliente=%s, id_documento=%s
        WHERE id_movimiento=%s;
    """, (
        data['tipo'], data['fecha'], data.get('glosa'),
        data.get('observacion'), data.get('id_elaborador'),
        data.get('id_cliente'), data.get('id_documento'), id_movimiento
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Movimiento actualizado'})

@app.route('/movimientos/<int:id_movimiento>', methods=['DELETE'])
def eliminar_movimiento(id_movimiento):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM movimiento WHERE id_movimiento = %s;", (id_movimiento,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Movimiento eliminado'})


# =====================
# CRUD KARDEX
# =====================
@app.route('/kardex', methods=['GET'])
def obtener_kardex():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""
        SELECT 
            k.id_movimiento,
            k.id_producto,
            p.nombre AS producto,
            m.tipo AS tipo_movimiento,
            m.fecha,
            k.cantidad,
            k.unitario,
            k.suttotal
        FROM kardex k
        JOIN producto p ON k.id_producto = p.id_producto
        JOIN movimiento m ON k.id_movimiento = m.id_movimiento
        ORDER BY k.id_movimiento ASC;
    """)
    kardex = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(kardex)

@app.route('/kardex', methods=['POST'])
def agregar_kardex():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO kardex (id_movimiento, id_producto, cantidad, unitario, suttotal)
        VALUES (%s, %s, %s, %s, %s);
    """, (
        data['id_movimiento'],
        data['id_producto'],
        data['cantidad'],
        data['unitario'],
        data['suttotal']
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Kardex agregado'})

@app.route('/kardex', methods=['DELETE'])
def eliminar_kardex():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        DELETE FROM kardex
        WHERE id_movimiento = %s AND id_producto = %s;
    """, (data['id_movimiento'], data['id_producto']))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Kardex eliminado'})


# =====================
# CRUD PERSONA
# =====================
@app.route('/personas', methods=['GET'])
def obtener_personas():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM persona ORDER BY id_persona ASC;")
    personas = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(personas)

@app.route('/personas', methods=['POST'])
def agregar_persona():
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO persona (nombre, primer_apellido, segundo_apellido, telefono, correo)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id_persona;
    """, (
        data['nombre'],
        data.get('primer_apellido'),
        data.get('segundo_apellido'),
        data.get('telefono'),
        data.get('correo')
    ))
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Persona agregada', 'id_persona': id_nuevo})

@app.route('/personas/<int:id_persona>', methods=['PUT'])
def actualizar_persona(id_persona):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE persona
        SET nombre=%s, primer_apellido=%s, segundo_apellido=%s, telefono=%s, correo=%s
        WHERE id_persona=%s;
    """, (
        data['nombre'],
        data.get('primer_apellido'),
        data.get('segundo_apellido'),
        data.get('telefono'),
        data.get('correo'),
        id_persona
    ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Persona actualizada'})

@app.route('/personas/<int:id_persona>', methods=['DELETE'])
def eliminar_persona(id_persona):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM persona WHERE id_persona = %s;", (id_persona,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Persona eliminada'})


# =====================
# CRUD USUARIO
# =====================
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""
        SELECT 
            u.id_usuario, u.username, u.id_rol, r.nombre AS rol, 
            p.nombre AS persona_nombre, p.primer_apellido, p.correo
        FROM usuario u
        JOIN rol r ON u.id_rol = r.id_rol
        JOIN persona p ON u.id_usuario = p.id_persona
        ORDER BY u.id_usuario ASC;
    """)
    usuarios = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(usuarios)

@app.route('/usuarios', methods=['POST'])
def agregar_usuario():
    data = request.get_json()
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO usuario (username, password, id_rol)
        VALUES (%s, %s, %s)
        RETURNING id_usuario;
    """, (
        data['username'],
        hashed_pw,
        data['id_rol']
    ))
    id_nuevo = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Usuario agregado', 'id_usuario': id_nuevo})

@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def actualizar_usuario(id_usuario):
    data = request.get_json()
    conn = get_connection()
    cur = conn.cursor()
    if 'password' in data and data['password']:
        hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        cur.execute("""
            UPDATE usuario
            SET username=%s, password=%s, id_rol=%s
            WHERE id_usuario=%s;
        """, (
            data['username'],
            hashed_pw,
            data['id_rol'],
            id_usuario
        ))
    else:
        cur.execute("""
            UPDATE usuario
            SET username=%s, id_rol=%s
            WHERE id_usuario=%s;
        """, (
            data['username'],
            data['id_rol'],
            id_usuario
        ))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Usuario actualizado'})

@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def eliminar_usuario(id_usuario):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuario WHERE id_usuario = %s;", (id_usuario,))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({'mensaje': 'Usuario eliminado'})



# =====================
# Ejecutar servidor
# =====================
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
