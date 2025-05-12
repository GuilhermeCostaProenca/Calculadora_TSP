from flask import request, render_template
import os
import pandas as pd
from app.logic.geocoder import geocode_addresses
from app.logic.route_optimizer import optimize_route
from app.logic.agrupador import agrupar_por_estado
from app.utils.batch_splitter import dividir_em_lotes

UPLOAD_FOLDER = "data"

def configure_routes(app):
    @app.route("/", methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route("/upload", methods=["POST"])
    def upload_file():
        file = request.files.get("file")
        quantidade = int(request.form.get("quantidade", 10))

        if not file:
            return render_template("index.html", error="Nenhum arquivo enviado.")

        filename = os.path.join(UPLOAD_FOLDER, "lojas.xlsx")
        file.save(filename)

        # Ler o Excel
        df = pd.read_excel(filename)

        # Agrupar por estado (exemplo: SP)
        from app.logic.agrupador import agrupar_por_estado
        grupos = agrupar_por_estado(df)
        df_sp = grupos.get("SP", pd.DataFrame())

        if df_sp.empty:
            return render_template("index.html", error="Nenhuma loja do estado de SP encontrada.")

        # Selecionar quantidade desejada
        df_lote = df_sp.head(quantidade)

        # Gerar endereços completos
        df_lote["endereco_completo"] = df_lote["Endereço"] + ", " + df_lote["CIDADE"] + ", " + df_lote["ESTADO"]

        # Obter coordenadas (incluindo o ponto de partida no Butantã)
        locais = ["Butantã, São Paulo - SP"] + df_lote["endereco_completo"].tolist()
        coordenadas = geocode_addresses(locais)

        # Calcular a rota otimizada
        rota_otimizada, distancia_total = optimize_route(coordenadas)

        # Montar resultado para exibir
        resultado = {
            "rota": [locais[i] for i in rota_otimizada],
            "distancia_total_km": round(distancia_total, 2)
        }

        return render_template("index.html", resultado=resultado)
