from flask import Blueprint, request, jsonify
from db_config import execute_query
import sys
from security import token_required
from datetime import date, datetime

# Blueprint
# Asegúrate de que este Blueprint esté registrado en tu app.py
kardex_bp = Blueprint('kardex_bp', __name__, url_prefix='/api/kardex')


# --- GET y POST (Maneja el REPORTE GET y la CREACIÓN POST) ---
@kardex_bp.route('/', methods=['GET', 'POST'])
@token_required
def handle_kardex_entries():
    if request.method == 'POST':
        # --- CREATE (Crear nuevo registro de Kardex) ---
        # Asume que estos datos vienen del frontend (por ejemplo, después de crear un detalle de venta/compra)
        data = request.get_json()
        id_movimiento = data.get('id_movimiento')
        id_producto = data.get('id_producto')
        cantidad = data.get('cantidad')
        unitario = data.get('unitario')
        # Tu campo se llama 'subtotal' en el esquema de DB (no 'suttotal' como en la versión anterior)
        subtotal = data.get('subtotal')

        # Validación
        if not all([id_movimiento, id_producto, cantidad, unitario]):
            return jsonify({
                "error": "Faltan campos obligatorios: id_movimiento, id_producto, cantidad, unitario."
            }), 400

        # Calcular subtotal si no se envía
        subtotal = subtotal if subtotal is not None else (cantidad * unitario)

        sql = """
            INSERT INTO kardex (id_movimiento, id_producto, cantidad, unitario, subtotal)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (id_movimiento, id_producto, cantidad, unitario, subtotal)

        try:
            execute_query(sql, params)

            # Recuperar el registro recién insertado para la respuesta
            new_entry = execute_query(
                "SELECT * FROM kardex WHERE id_movimiento = %s AND id_producto = %s",
                (id_movimiento, id_producto),
                fetch=True
            )
            # Asegúrate de que new_entry no esté vacío antes de acceder al índice
            if new_entry:
                print("Registro de Kardex insertado correctamente:", new_entry[0])
                return jsonify({
                    "mensaje": "Registro de Kardex creado con éxito.",
                    "registro": new_entry[0]
                }), 201

            return jsonify({"error": "Registro creado, pero no se pudo recuperar."}), 201

        except Exception as e:
            print(f"Error en POST /api/kardex/: {e}", file=sys.stderr)
            return jsonify({
                "error": "Error al crear registro de Kardex.",
                "detalle": str(e)
            }), 400

    else:
        # --- READ ALL (Reporte de Kardex) - LÓGICA CORREGIDA ---
        sql_reporte = """
            SELECT 
                k.id_movimiento,
                m.fecha,
                p.nombre AS producto_nombre,
                m.glosa,
                m.tipo,
                k.cantidad,
                k.subtotal
            FROM kardex k
            -- 1. Unir Kardex y Movimiento por id_movimiento (La tabla movimiento NO tiene id_producto)
            JOIN movimiento m ON k.id_movimiento = m.id_movimiento
            -- 2. Unir Kardex y Producto por id_producto
            JOIN producto p ON k.id_producto = p.id_producto
            ORDER BY m.fecha ASC, k.id_movimiento ASC;
        """

        try:
            # ⭐ CORRECCIÓN CLAVE: Se usa 'fetch=True' para obtener todos los resultados
            data = execute_query(sql_reporte, fetch=True)

            if not data:
                return jsonify([]), 200

            kardex_list = []
            for item in data:
                # Mapeo de columnas por índice (asumiendo tuplas o listas desde execute_query)
                tipo_char = item[4]  # Ej: 'V', 'C', 'A'

                kardex_list.append({
                    # id_kardex no existe en el esquema, usamos id_movimiento como ID principal para el reporte
                    "id_kardex": item[0],
                    "id_movimiento": item[0],
                    "fecha": item[1].isoformat() if isinstance(item[1], (date, datetime)) else item[1],
                    "producto_nombre": item[2],
                    "glosa": item[3],
                    "tipo_movimiento": tipo_char,

                    # El esquema usa CHAR(1) para el tipo. Asumimos 'C' (Compra) es ENTRADA y 'V' (Venta) es SALIDA.
                    "cantidad_entrada": item[5] if tipo_char in ('C', 'A', 'E') else None,
                    "cantidad_salida": item[5] if tipo_char in ('V', 'S') else None,
                    "saldo_final": None,  # NO EXISTE en la DB, se deja N/A en el frontend
                    "subtotal": item[6]
                })

            return jsonify(kardex_list), 200

        except Exception as e:
            print(f"Error en GET /api/kardex/ (REPORTE): {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener reporte de Kardex", "detalle": str(e)}), 500


# --- GET, PUT, DELETE por clave compuesta ---
@kardex_bp.route('/<int:id_movimiento>/<int:id_producto>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def handle_kardex_entry(id_movimiento, id_producto):
    # Lógica de GET, PUT, DELETE individual... (Mantener el código anterior)
    # ...
    if request.method == 'GET':
        sql = "SELECT * FROM kardex WHERE id_movimiento = %s AND id_producto = %s"
        try:
            entry = execute_query(sql, (id_movimiento, id_producto), fetch=True)
            if entry:
                return jsonify(entry[0]), 200
            return jsonify({"error": "Registro de Kardex no encontrado."}), 404
        except Exception as e:
            return jsonify({"error": "Error al obtener registro de Kardex"}), 500

    # ... (Resto de la lógica PUT y DELETE)
    # ...