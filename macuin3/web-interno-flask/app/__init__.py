import os
from flask import Flask
from dotenv import load_dotenv
load_dotenv()

def create_app():
    app = Flask(__name__,
        template_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates"),
        static_folder=os.path.join(os.path.dirname(os.path.dirname(__file__)), "static"))
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret")
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.autopartes import autopartes_bp
    from app.routes.pedidos import pedidos_bp
    from app.routes.inventario import inventario_bp
    from app.routes.reportes import reportes_bp
    from app.routes.empleados import empleados_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(autopartes_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(inventario_bp)
    app.register_blueprint(reportes_bp)
    app.register_blueprint(empleados_bp)
    return app
