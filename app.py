from flask import Flask, redirect, url_for
from config import Config

def create_app(config_class=Config):
    print("Iniciando create_app...")  # Para debug
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Registrar blueprints
    try:
        from auth.routes import auth_bp
        from dashboard.routes import dashboard_bp
        from tools.routes import tools_bp
        from tools.item_bag_editor import editor_bp  # Novo blueprint
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(dashboard_bp)
        app.register_blueprint(tools_bp)
        app.register_blueprint(editor_bp)  # Registrar o editor
    except ImportError as e:
        print(f"Erro ao importar blueprints: {e}")
        raise

    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)