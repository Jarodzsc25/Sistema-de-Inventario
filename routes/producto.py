from flask import Blueprint, request, jsonify
from db_config import execute_query
import sys

producto_bp = Blueprint('producto_bp', __name__)

# --- GET y POST ---
@producto_bp.route('/', methods=['GET', 'POST'])
def handle_productos():
    if request.method == 'POST':
        # --- CREATE ---
        data = request.get_json()
        codigo = data.get('codigo')
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        unidad = data.get('unidad')
        id_distribuidor = data.get('id_distribuidor')

        if not all([nombre, id_distribuidor]):
            return jsonify({"error": "Faltan campos obligatorios: nombre, id_distribuidor."}), 400

        sql = """
            INSERT INTO producto (codigo, nombre, descripcion, unidad, id_distribuidor) 
            VALUES (%s, %s, %s, %s, %s) 
            RETURNING id_producto
        """
        params = (codigo, nombre, descripcion, unidad, id_distribuidor)

        try:
            results = execute_query(sql, params, fetch=True)
            new_id = results[0]['id_producto'] if results else None
            print(f"Producto creado: {nombre} (id_producto={new_id})")
            return jsonify({
                "mensaje": "Producto creado con éxito.",
                "producto": {
                    "id_producto": new_id,
                    "nombre": nombre,
                    "codigo": codigo,
                    "id_distribuidor": id_distribuidor
                }
            }), 201
        except Exception as e:
            print(f"Error en POST /api/producto/: {e}", file=sys.stderr)
            return jsonify({
                "error": "Error al crear producto. Verifica que el distribuidor exista.",
                "detalle": str(e)
            }), 400

    else:
        # --- READ ALL ---
        sql = """
            SELECT 
                p.*, d.nombre AS distribuidor_nombre 
            FROM producto p
            JOIN distribuidor d ON p.id_distribuidor = d.id_distribuidor
            ORDER BY p.id_producto
        """
        try:
            productos = execute_query(sql, fetch=True)
            return jsonify(productos), 200
        except Exception as e:
            print(f"Error en GET /api/producto/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener lista de productos"}), 500

# --- GET, PUT, DELETE por id_producto ---
@producto_bp.route('/<int:id_producto>', methods=['GET', 'PUT', 'DELETE'])
def handle_producto(id_producto):
    if request.method == 'GET':
        # --- READ ONE ---
        sql = """
            SELECT 
                p.*, d.nombre AS distribuidor_nombre 
            FROM producto p
            JOIN distribuidor d ON p.id_distribuidor = d.id_distribuidor
            WHERE p.id_producto = %s
        """
        try:
            producto = execute_query(sql, (id_producto,), fetch=True)
            if producto:
                return jsonify(producto[0]), 200
            return jsonify({"error": "Producto no encontrado."}), 404
        except Exception as e:
            print(f"Error en GET /api/producto/{id_producto}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener producto"}), 500

    elif request.method == 'PUT':
        # --- UPDATE ---
        data = request.get_json()
        codigo = data.get('codigo')
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        unidad = data.get('unidad')
        id_distribuidor = data.get('id_distribuidor')

        if not all([nombre, id_distribuidor]):
            return jsonify({"error": "Los campos 'nombre' y 'id_distribuidor' son obligatorios para actualizar."}), 400

        sql = """
            UPDATE producto SET 
                codigo = %s, nombre = %s, descripcion = %s, 
                unidad = %s, id_distribuidor = %s 
            WHERE id_producto = %s
        """
        params = (codigo, nombre, descripcion, unidad, id_distribuidor, id_producto)

        try:
            row_count = execute_query(sql, params)
            if row_count > 0:
                print(f"Producto actualizado: id_producto={id_producto}")
                return jsonify({"mensaje": "Producto actualizado con éxito.", "id_producto": id_producto}), 200
            return jsonify({"error": "Producto no encontrado para actualizar."}), 404
        except Exception as e:
            print(f"Error en PUT /api/producto/{id_producto}: {e}", file=sys.stderr)
            return jsonify({
                "error": "Error al actualizar producto. Verifica que el distribuidor exista.",
                "detalle": str(e)
            }), 400

    elif request.method == 'DELETE':
        # --- DELETE ---
        sql = "DELETE FROM producto WHERE id_producto = %s"
        try:
            row_count = execute_query(sql, (id_producto,))
            if row_count > 0:
                print(f"Producto eliminado: id_producto={id_producto}")
                return jsonify({"mensaje": "Producto eliminado con éxito.", "id_producto": id_producto}), 200
            return jsonify({"error": "Producto no encontrado para eliminar."}), 404
        except Exception as e:
            print(f"Error en DELETE /api/producto/{id_producto}: {e}", file=sys.stderr)
            return jsonify({
                "error": "Error al eliminar producto. Puede tener movimientos en Kardex.",
                "detalle": str(e)
            }), 400
