"""Application factory (MVC: ensambla controllers + views)."""

from pathlib import Path

from flask import Flask

from .controllers.comidas_controller import comidas_bp
from .controllers.progreso_controller import progreso_bp
from .controllers.rutinas_controller import rutinas_bp
from .controllers.suscripcion_controller import suscripcion_bp

_VIEWS_DIR = Path(__file__).resolve().parent / "views"


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(_VIEWS_DIR / "templates"),
        static_folder=str(_VIEWS_DIR / "static"),
    )
    app.register_blueprint(rutinas_bp)
    app.register_blueprint(progreso_bp)
    app.register_blueprint(comidas_bp)
    app.register_blueprint(suscripcion_bp)
    return app
