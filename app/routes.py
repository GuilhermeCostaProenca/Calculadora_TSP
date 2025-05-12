from flask import request, render_template
import os
import pandas as pd
from app.logic.geocoder import geocode_addresses
from app.logic.distance_matrix_google import get_distance_matrix_google
from app.logic.route_optimizer import optimize_route
from app.logic.agrupador import agrupar_por_estado
from os import getenv

UPLOAD_FOLDER = "data"
U1_ENDERECO = "Rua Gerivatiba, 207, São Paulo - SP"

def configure_routes(app):
    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html", resultado=None, api_key=getenv("GOOGLE_API_KEY"))

    @app.route("/upload", methods=["POST"])
    def upload_file():
        file = request.files.get("file")
        if not file:
            return render_template("index.html", error="Nenhum arquivo enviado.", resultado=None)

        filename = os.path.join(UPLOAD_FOLDER, "lojas.xlsx")
        file.save(filename)

        df = pd.read_excel(filename)
        grupos = agrupar_por_estado(df)
        df_sp = grupos.get("SP", pd.DataFrame())
        if df_sp.empty:
            return render_template("index.html", error="Nenhuma loja do estado de SP encontrada.", resultado=None)

        df_lote = df_sp.head(10).copy()
        df_lote["endereco_completo"] = df_lote["Endereço"] + ", " + df_lote["CIDADE"] + ", " + df_lote["ESTADO"]

        locais = [U1_ENDERECO] + df_lote["endereco_completo"].tolist()

        try:
            coordenadas = geocode_addresses(locais)
        except Exception as e:
            return render_template("index.html", error=f"Erro na geocodificação: {e}", resultado=None)

        try:
            matriz_distancias = get_distance_matrix_google(locais)
        except Exception as e:
            return render_template("index.html", error=f"Erro ao calcular matriz de distância: {e}", resultado=None)

        rota_otimizada, distancia_total = optimize_route(matriz_distancias)

        rota_formatada = []
        for i, idx in enumerate(rota_otimizada):
            if i == 0:
                rota_formatada.append(f"U1: {locais[idx]}")
            else:
                letra = chr(64 + i)  # A, B, C...
                rota_formatada.append(f"{letra}: {locais[idx]}")

        url_google_maps = "https://www.google.com/maps/dir/" + "/".join([locais[i].replace(" ", "+") for i in rota_otimizada])

        resultado = {
            "rota": [locais[i] for i in rota_otimizada],
            "rota_formatada": rota_formatada,
            "distancia_total_km": round(distancia_total, 2),
            "google_maps_url": url_google_maps
        }

        return render_template("index.html", resultado=resultado, api_key=getenv("GOOGLE_API_KEY"))
