from flask import Blueprint, request, jsonify
from db_config import execute_query
from datetime import datetime
import sys

documento_bp = Blueprint('documento_bp', __name__)

# --- GET y POST ---
@documento_bp.route('/', methods=['GET', 'POST'])
def handle_documentos():
    if request.method == 'POST':
        # --- CREATE ---
        data = request.get_json()
        numero = data.get('numero')
        fecha = data.get('fecha', datetime.now().isoformat())

        if not numero:
            return jsonify({"error": "Falta el campo 'numero'."}), 400

        sql = "INSERT INTO documento (numero, fecha) VALUES (%s, %s) RETURNING id_documento"
        params = (numero, fecha)

        try:
            results = execute_query(sql, params, fetch=True)
            new_id = results[0]['id_documento'] if results else None
            print(f"Documento creado: numero={numero} (id_documento={new_id})")
            return jsonify({
                "mensaje": "Documento creado con éxito.",
                "documento": {
                    "id_documento": new_id,
                    "numero": numero,
                    "fecha": fecha
                }
            }), 201
        except Exception as e:
            print(f"Error en POST /api/documento/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al crear documento", "detalle": str(e)}), 400

    else:
        # --- READ ALL ---
        sql = "SELECT id_documento, numero, fecha FROM documento ORDER BY id_documento DESC"
        try:
            documentos = execute_query(sql, fetch=True)
            return jsonify(documentos), 200
        except Exception as e:
            print(f"Error en GET /api/documento/: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener lista de documentos"}), 500

# --- GET, PUT, DELETE por id_documento ---
@documento_bp.route('/<int:id_documento>', methods=['GET', 'PUT', 'DELETE'])
def handle_documento(id_documento):
    if request.method == 'GET':
        # --- READ ONE ---
        sql = "SELECT id_documento, numero, fecha FROM documento WHERE id_documento = %s"
        try:
            documento = execute_query(sql, (id_documento,), fetch=True)
            if documento:
                return jsonify(documento[0]), 200
            return jsonify({"error": "Documento no encontrado."}), 404
        except Exception as e:
            print(f"Error en GET /api/documento/{id_documento}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al obtener documento"}), 500

    elif request.method == 'PUT':
        # --- UPDATE ---
        data = request.get_json()
        numero = data.get('numero')
        fecha = data.get('fecha', datetime.now().isoformat())

        if not numero:
            return jsonify({"error": "Falta el campo 'numero'."}), 400

        sql = "UPDATE documento SET numero = %s, fecha = %s WHERE id_documento = %s"
        params = (numero, fecha, id_documento)

        try:
            row_count = execute_query(sql, params)
            if row_count > 0:
                print(f"Documento actualizado: id_documento={id_documento}")
                return jsonify({"mensaje": "Documento actualizado con éxito.", "id_documento": id_documento}), 200
            return jsonify({"error": "Documento no encontrado para actualizar."}), 404
        except Exception as e:
            print(f"Error en PUT /api/documento/{id_documento}: {e}", file=sys.stderr)
            return jsonify({"error": "Error al actualizar documento", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        # --- DELETE ---
        sql = "DELETE FROM documento WHERE id_documento = %s"
        try:
            row_count = execute_query(sql, (id_documento,))
            if row_count > 0:
                print(f"Documento eliminado: id_documento={id_documento}")
                return jsonify({"mensaje": "Documento eliminado con éxito.", "id_documento": id_documento}), 200
            return jsonify({"error": "Documento no encontrado para eliminar."}), 404
        except Exception as e:
            print(f"Error en DELETE /api/documento/{id_documento}: {e}", file=sys.stderr)
            return jsonify({
                "error": "Error al eliminar documento. Puede tener Movimientos asociados.",
                "detalle": str(e)
            }), 400
