"""Application factory (MVC: ensambla controllers + views)."""

from pathlib import Path

from flask import Flask

from .controllers.rutinas_controller import rutinas_bp

_VIEWS_DIR = Path(__file__).resolve().parent / "views"


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder=str(_VIEWS_DIR / "templates"),
        static_folder=str(_VIEWS_DIR / "static"),
    )
    app.register_blueprint(rutinas_bp)
    return app
