"""Controller: rutas web para el registro nutricional de comidas."""

from datetime import date

from flask import Blueprint, redirect, render_template, request, url_for

from ..models.comida import TIPOS_LABEL, Comida
from ..models.comida_repository import ComidaRepository

comidas_bp = Blueprint("comidas", __name__)
repo = ComidaRepository()


def _totales(comidas: list[Comida]) -> dict:
    return {
        "calorias": sum(c.calorias for c in comidas),
        "proteinas_g": sum(c.proteinas_g for c in comidas),
        "carbohidratos_g": sum(c.carbohidratos_g for c in comidas),
        "grasas_g": sum(c.grasas_g for c in comidas),
    }


@comidas_bp.route("/comidas")
def ver_comidas():
    fecha = request.args.get("fecha") or date.today().isoformat()
    comidas = repo.obtener_por_fecha(fecha)
    return render_template(
        "comidas.html",
        fecha=fecha,
        comidas=comidas,
        totales=_totales(comidas),
        tipos_label=TIPOS_LABEL,
    )


@comidas_bp.route("/comidas", methods=["POST"])
def agregar_comida():
    fecha = request.form["fecha"]
    comida = Comida(
        fecha=fecha,
        tipo=request.form["tipo"],
        nombre=request.form["nombre"].strip(),
        calorias=int(request.form["calorias"]),
        proteinas_g=float(request.form.get("proteinas_g") or 0),
        carbohidratos_g=float(request.form.get("carbohidratos_g") or 0),
        grasas_g=float(request.form.get("grasas_g") or 0),
    )
    repo.agregar(comida)
    return redirect(url_for("comidas.ver_comidas", fecha=fecha))


@comidas_bp.route("/comidas/<comida_id>/editar", methods=["POST"])
def editar_comida(comida_id):
    fecha = request.form["fecha"]
    repo.editar(
        comida_id,
        {
            "nombre": request.form["nombre"].strip(),
            "tipo": request.form["tipo"],
            "calorias": request.form["calorias"],
            "proteinas_g": request.form.get("proteinas_g") or 0,
            "carbohidratos_g": request.form.get("carbohidratos_g") or 0,
            "grasas_g": request.form.get("grasas_g") or 0,
        },
    )
    return redirect(url_for("comidas.ver_comidas", fecha=fecha))


@comidas_bp.route("/comidas/<comida_id>/eliminar", methods=["POST"])
def eliminar_comida(comida_id):
    fecha = request.form["fecha"]
    repo.eliminar(comida_id)
    return redirect(url_for("comidas.ver_comidas", fecha=fecha))
