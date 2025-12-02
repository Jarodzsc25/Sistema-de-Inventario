from flask import Blueprint, request, jsonify
from db_config import execute_query
import sys
from security import token_required
from datetime import date, datetime

# Blueprint
kardex_bp = Blueprint('kardex_bp', __name__, url_prefix='/api/kardex')

# --- Constante para el nombre del campo de subtotal en la DB ---
SUBTOTAL_DB_FIELD = 'subtotal'


# --- GET y POST (Maneja el REPORTE GET y la CREACIÓN POST) ---
@kardex_bp.route('/', methods=['GET', 'POST'], strict_slashes=False)
@token_required
def handle_kardex_entries():
    if request.method == 'POST':
        # --- CREATE (Crear nuevo registro de Kardex) ---
        data = request.get_json()
        id_movimiento = data.get('id_movimiento')
        id_producto = data.get('id_producto')
        cantidad = data.get('cantidad')
        unitario = data.get('unitario')
        subtotal = data.get('subtotal')

        # Validación básica de campos obligatorios
        if not all([id_movimiento, id_producto]):
            return jsonify({
                "error": "Faltan campos obligatorios: id_movimiento e id_producto."
            }), 400

        # Validación y cálculo robusto
        try:
            cantidad = float(cantidad)
            unitario = float(unitario)

            # Calcular subtotal si no se envía o es None
            if subtotal is None:
                subtotal = cantidad * unitario
            else:
                subtotal = float(subtotal)

        except (TypeError, ValueError) as e:
            return jsonify({
                "error": "Cantidad, unitario y subtotal deben ser números válidos.",
                "detalle": str(e)
            }), 400

        # Aseguramos que la columna sea 'subtotal' usando la constante
        sql = f"""
            INSERT INTO kardex (id_movimiento, id_producto, cantidad, unitario, {SUBTOTAL_DB_FIELD})
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (id_movimiento, id_producto, cantidad, unitario, subtotal)

        try:
            execute_query(sql, params)

            # Recuperar el registro recién insertado para la respuesta
            new_entry = execute_query(
                f"SELECT id_movimiento, id_producto, cantidad, unitario, {SUBTOTAL_DB_FIELD} FROM kardex WHERE id_movimiento = %s AND id_producto = %s",
                (id_movimiento, id_producto),
                fetch=True
            )
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
            }), 500

    else:
        # --- READ ALL (Reporte de Kardex) - LÓGICA FINAL ---
        # Usamos COALESCE y LEFT JOIN para garantizar la integridad de las columnas.
        sql_reporte = f"""
            SELECT 
                k.id_movimiento,                                        -- id_movimiento
                COALESCE(m.fecha::text, '') AS fecha,                   -- fecha
                COALESCE(p.nombre, 'Producto Desconocido') AS producto_nombre, -- producto_nombre
                COALESCE(m.glosa, '') AS glosa,                         -- glosa
                COALESCE(m.tipo, '') AS tipo,                           -- tipo
                k.cantidad,                                             -- cantidad
                k.{SUBTOTAL_DB_FIELD} AS subtotal                       -- subtotal
            FROM kardex k
            LEFT JOIN movimiento m ON k.id_movimiento = m.id_movimiento 
            LEFT JOIN producto p ON k.id_producto = p.id_producto
            ORDER BY m.fecha ASC, k.id_movimiento ASC;
        """

        try:
            data = execute_query(sql_reporte, fetch=True)

            if not data:
                return jsonify([]), 200

            kardex_list = []
            for item in data:

                # 🚀 CORRECCIÓN CLAVE: Usamos claves de diccionario en lugar de índices numéricos

                # item['tipo']
                tipo_char = str(item.get('tipo', '') or '').upper()

                # item['cantidad']
                cantidad = item.get('cantidad')
                try:
                    cantidad = float(cantidad) if cantidad is not None else 0.0
                except (ValueError, TypeError):
                    cantidad = 0.0

                # item['subtotal']
                subtotal = item.get('subtotal')
                try:
                    subtotal = float(subtotal) if subtotal is not None else 0.0
                except (ValueError, TypeError):
                    subtotal = 0.0

                kardex_list.append({
                    "id_movimiento": item.get('id_movimiento'),
                    "fecha": item.get('fecha'),
                    "producto_nombre": item.get('producto_nombre'),
                    "glosa": item.get('glosa'),
                    "tipo_movimiento": tipo_char,

                    "cantidad_entrada": cantidad if tipo_char in ('C', 'E') else None,
                    "cantidad_salida": cantidad if tipo_char in ('V', 'S') else None,
                    "subtotal": subtotal
                })

            return jsonify(kardex_list), 200

        except Exception as e:
            print(f"Error en GET /api/kardex/ (REPORTE): {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener reporte de Kardex", "detalle": str(e)}), 500


# --- GET, PUT, DELETE por clave compuesta (id_movimiento, id_producto) ---
@kardex_bp.route('/<int:id_movimiento>/<int:id_producto>', methods=['GET', 'PUT', 'DELETE'])
@token_required
def handle_kardex_entry(id_movimiento, id_producto):
    if request.method == 'GET':
        sql = f"SELECT id_movimiento, id_producto, cantidad, unitario, {SUBTOTAL_DB_FIELD} FROM kardex WHERE id_movimiento = %s AND id_producto = %s"
        try:
            entry = execute_query(sql, (id_movimiento, id_producto), fetch=True)
            if entry:
                return jsonify(entry[0]), 200
            return jsonify({"error": "Registro de Kardex no encontrado."}), 404
        except Exception as e:
            print(f"Error en GET por ID en Kardex: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener registro de Kardex"}), 500

    elif request.method == 'PUT':
        data = request.get_json()
        cantidad = data.get('cantidad')
        unitario = data.get('unitario')
        subtotal = data.get('subtotal')

        if cantidad is None or unitario is None:
            return jsonify({"error": "Cantidad y unitario son obligatorios para la actualización."}), 400

        try:
            cantidad = float(cantidad)
            unitario = float(unitario)
            if subtotal is None:
                subtotal = cantidad * unitario
            else:
                subtotal = float(subtotal)
        except (TypeError, ValueError):
            return jsonify({"error": "Los campos deben ser numéricos."}), 400

        sql = f"""
            UPDATE kardex SET 
                cantidad = %s, 
                unitario = %s, 
                {SUBTOTAL_DB_FIELD} = %s
            WHERE id_movimiento = %s AND id_producto = %s
        """
        params = (cantidad, unitario, subtotal, id_movimiento, id_producto)

        try:
            execute_query(sql, params)
            return jsonify({"mensaje": "Registro de Kardex actualizado con éxito."}), 200
        except Exception as e:
            print(f"Error en PUT de Kardex: {e}", file=sys.stderr)
            return jsonify({"error": "Error al actualizar registro de Kardex"}), 500

    elif request.method == 'DELETE':
        sql = "DELETE FROM kardex WHERE id_movimiento = %s AND id_producto = %s"
        try:
            execute_query(sql, (id_movimiento, id_producto))
            return jsonify({"mensaje": "Registro de Kardex eliminado con éxito."}), 200
        except Exception as e:
            print(f"Error en DELETE de Kardex: {e}", file=sys.stderr)
            return jsonify({"error": "Error al eliminar registro de Kardex"}), 500

    return jsonify({"error": "Método no permitido o no implementado"}), 405