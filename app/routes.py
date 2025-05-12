from flask import request, render_template, redirect, url_for
import os
import pandas as pd
from app.logic.geocoder import geocode_addresses
from app.logic.route_optimizer import optimize_route

UPLOAD_FOLDER = "data"

def configure_routes(app):
    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/upload", methods=["POST"])
    def upload_file():
        file = request.files.get("file")
        if not file:
            return render_template("index.html", error="Nenhum arquivo enviado.")

        filename = os.path.join(UPLOAD_FOLDER, "lojas.xlsx")
        file.save(filename)

        # Ler o Excel
        df = pd.read_excel(filename)
        df = df.head(10)  # pega só as 10 primeiras lojas por enquanto

        # Gerar endereços completos
        df["endereco_completo"] = df["Endereço"] + ", " + df["CIDADE"] + ", " + df["ESTADO"]

        # Obter coordenadas (incluindo o ponto de partida no Butantã)
        locais = ["Butantã, São Paulo - SP"] + df["endereco_completo"].tolist()
        coordenadas = geocode_addresses(locais)

        # Calcular a rota otimizada
        rota_otimizada, distancia_total = optimize_route(coordenadas)

        # Montar resultado para exibir
        resultado = {
            "rota": [locais[i] for i in rota_otimizada],
            "distancia_total_km": round(distancia_total, 2)
        }

        return render_template("index.html", resultado=resultado)
