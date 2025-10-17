from flask import Flask, jsonify, render_template
from flask_cors import CORS

# ===== Importar extensiones =====
from extensions import bcrypt

# ===== Crear app =====
app = Flask(__name__)
CORS(app)
bcrypt.init_app(app)

# ===== Rutas de frontend =====
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard_page():
    return render_template('dashboard.html')

# ===== Test API =====
@app.route('/api_test')
def api_test():
    return jsonify({"mensaje": "API del sistema de inventario funcionando"})

# ===== Importar y registrar Blueprints =====
from routes.usuario_routes import bp as usuario_bp
from routes.producto_routes import bp as producto_bp
from routes.persona_routes import bp as persona_bp
from routes.documento_routes import bp as documento_bp
from routes.movimiento_routes import bp as movimiento_bp
from routes.kardex_routes import bp as kardex_bp
from routes.distribuidor_routes import bp as distribuidores_bp

app.register_blueprint(usuario_bp)
app.register_blueprint(producto_bp)
app.register_blueprint(persona_bp)
app.register_blueprint(documento_bp)
app.register_blueprint(movimiento_bp)
app.register_blueprint(kardex_bp)
app.register_blueprint(distribuidores_bp)

# ===== Ejecutar servidor =====
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
