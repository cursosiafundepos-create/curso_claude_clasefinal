"""Controller: rutas web para consultar y cambiar el plan de suscripción de la app."""

from flask import Blueprint, redirect, render_template, request, url_for

from ..models.suscripcion_repository import SuscripcionRepository

suscripcion_bp = Blueprint("suscripcion", __name__)
repo = SuscripcionRepository()


@suscripcion_bp.route("/suscripcion")
def ver_suscripcion():
    return render_template("suscripcion.html", suscripcion=repo.obtener())


@suscripcion_bp.route("/suscripcion/cambiar", methods=["POST"])
def cambiar_plan():
    repo.cambiar_plan(request.form["plan"])
    return redirect(url_for("suscripcion.ver_suscripcion"))
