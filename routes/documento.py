from flask import Blueprint, request, jsonify
from db_config import execute_query
from datetime import datetime

documento_bp = Blueprint('documento_bp', __name__)


# Obtener todos los documentos y crear uno nuevo (GET y POST)
@documento_bp.route('/', methods=['GET', 'POST'])
def handle_documentos():
    if request.method == 'POST':
        # --- CREATE (Crear nuevo Documento) ---
        data = request.get_json()
        numero = data.get('numero')
        # Si no se proporciona fecha, usa la fecha y hora actual de la API
        fecha = data.get('fecha', datetime.now().isoformat())

        if not numero:
            return jsonify({"error": "Falta el campo 'numero'."}), 400

        sql = "INSERT INTO documento (numero, fecha) VALUES (%s, %s) RETURNING id_documento"
        params = (numero, fecha)

        try:
            results = execute_query(sql, params, fetch=True)
            new_id = results[0]['id_documento'] if results else None
            return jsonify({
                "mensaje": "Documento creado con éxito.",
                "id_documento": new_id,
                "numero": numero,
                "fecha": fecha
            }), 201
        except Exception as e:
            return jsonify({"error": "Error al crear documento", "detalle": str(e)}), 400

    else:
        # --- READ ALL (Obtener todos los Documentos) ---
        sql = "SELECT id_documento, numero, fecha FROM documento ORDER BY id_documento DESC"
        try:
            documentos = execute_query(sql, fetch=True)
            return jsonify(documentos), 200
        except Exception:
            return jsonify({"error": "Error al obtener lista de documentos"}), 500


# Obtener, actualizar o eliminar un Documento por ID (GET, PUT, DELETE)
@documento_bp.route('/<int:id_documento>', methods=['GET', 'PUT', 'DELETE'])
def handle_documento(id_documento):
    if request.method == 'GET':
        # --- READ ONE (Obtener un Documento) ---
        sql = "SELECT id_documento, numero, fecha FROM documento WHERE id_documento = %s"
        try:
            documento = execute_query(sql, (id_documento,), fetch=True)
            if documento:
                return jsonify(documento[0]), 200
            return jsonify({"error": "Documento no encontrado."}), 404
        except Exception:
            return jsonify({"error": "Error al obtener documento"}), 500

    elif request.method == 'PUT':
        # --- UPDATE (Actualizar Documento) ---
        data = request.get_json()
        numero = data.get('numero')
        fecha = data.get('fecha')

        if not numero:
            return jsonify({"error": "Falta el campo 'numero'."}), 400

        sql = "UPDATE documento SET numero = %s, fecha = %s WHERE id_documento = %s"
        params = (numero, fecha, id_documento)

        try:
            row_count = execute_query(sql, params)
            if row_count > 0:
                return jsonify({"mensaje": "Documento actualizado con éxito.", "id_documento": id_documento}), 200
            return jsonify({"error": "Documento no encontrado para actualizar."}), 404
        except Exception as e:
            return jsonify({"error": "Error al actualizar documento", "detalle": str(e)}), 400

    elif request.method == 'DELETE':
        # --- DELETE (Eliminar Documento) ---
        sql = "DELETE FROM documento WHERE id_documento = %s"
        try:
            row_count = execute_query(sql, (id_documento,))
            if row_count > 0:
                return jsonify({"mensaje": "Documento eliminado con éxito.", "id_documento": id_documento}), 200
            return jsonify({"error": "Documento no encontrado para eliminar."}), 404
        except Exception as e:
            # Si hay Movimientos asociados, esto fallará.
            return jsonify(
                {"error": "Error al eliminar documento. Puede tener Movimientos asociados.", "detalle": str(e)}), 400