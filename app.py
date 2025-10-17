from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from routes import (
    login_bp, distribuidor_bp, producto_bp,
    documento_bp, movimiento_bp, kardex_bp,
    persona_bp, usuario_bp
)

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)

# Registrar los Blueprints
app.register_blueprint(login_bp)
app.register_blueprint(distribuidor_bp)
app.register_blueprint(producto_bp)
app.register_blueprint(documento_bp)
app.register_blueprint(movimiento_bp)
app.register_blueprint(kardex_bp)
app.register_blueprint(persona_bp)
app.register_blueprint(usuario_bp)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
