#recibe la búsqueda del usuario,manda esa búsqueda al servicio,obtiene los resultados
from flask import Blueprint, render_template, request
from app.services.series_service import SeriesService

series_bp = Blueprint("series", __name__)
series_service = SeriesService()

@series_bp.route("/", methods=["GET"])
def home():
    query = request.args.get("query", "").strip()
    data = None

    if query:
        data = series_service.search_series_data(query)

    return render_template("index.html", data=data, query=query)