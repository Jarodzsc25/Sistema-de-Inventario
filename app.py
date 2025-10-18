from flask import Flask, jsonify
from psycopg2 import OperationalError, DatabaseError
from db_config import execute_query # Importamos la utilidad de conexión

# Importar Blueprints de Rutas
from routes.rol import rol_bp
from routes.persona import persona_bp
from routes.usuario import usuario_bp
from routes.distribuidor import distribuidor_bp
from routes.producto import producto_bp
from routes.documento import documento_bp
from routes.movimiento import movimiento_bp
from routes.kardex import kardex_bp

app = Flask(__name__)

# Configuración (opcional, para modo debug)
app.config['DEBUG'] = True

# --- Registro de Blueprints de Rutas ---
app.register_blueprint(rol_bp, url_prefix='/api/rol')
app.register_blueprint(persona_bp, url_prefix='/api/persona')
app.register_blueprint(usuario_bp, url_prefix='/api/usuario')
app.register_blueprint(distribuidor_bp, url_prefix='/api/distribuidor')
app.register_blueprint(producto_bp, url_prefix='/api/producto')
app.register_blueprint(documento_bp, url_prefix='/api/documento')
app.register_blueprint(movimiento_bp, url_prefix='/api/movimiento')
app.register_blueprint(kardex_bp, url_prefix='/api/kardex')


# --- Manejadores de Errores Globales ---
@app.errorhandler(404)
def resource_not_found(e):
    """Manejador para errores 404 (Not Found)."""
    return jsonify({"error": "Recurso no encontrado", "mensaje": str(e)}), 404

@app.errorhandler(OperationalError)
def db_connection_error(e):
    """Manejador para errores de conexión a la BD."""
    return jsonify({"error": "Error de conexión a la BD", "mensaje": "Verifica las credenciales o el estado de PostgreSQL."}), 503

@app.errorhandler(DatabaseError)
def db_operation_error(e):
    """Manejador para errores de SQL (ej. violación de FK, dato nulo)."""
    return jsonify({"error": "Error de base de datos", "mensaje": str(e).split('\n')[0]}), 400

@app.errorhandler(Exception)
def internal_server_error(e):
    """Manejador genérico para errores internos."""
    app.logger.error(f"Error inesperado: {e}")
    return jsonify({"error": "Error interno del servidor", "mensaje": "Algo salió mal. Consulta los logs."}), 500


# Ruta de Bienvenida
@app.route('/')
def home():
    """Ruta de inicio para verificar que la API está funcionando."""
    return jsonify({"mensaje": "API del Sistema de Ventas en funcionamiento.", "version": "1.0"})

if __name__ == '__main__':
    # Ejecuta la aplicación en el puerto 5000 por defecto
    app.run(host='0.0.0.0', port=5000)
