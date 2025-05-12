from flask import request, render_template
import os
import pandas as pd
from app.logic.geocoder import geocode_addresses
from app.logic.distance_matrix_google import get_distance_matrix_google
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

        # Salvar arquivo
        filename = os.path.join(UPLOAD_FOLDER, "lojas.xlsx")
        file.save(filename)

        # Ler Excel
        df = pd.read_excel(filename)

        # Agrupar por estado e selecionar SP
        grupos = agrupar_por_estado(df)
        df_sp = grupos.get("SP", pd.DataFrame())

        if df_sp.empty:
            return render_template("index.html", error="Nenhuma loja do estado de SP encontrada.")

        # Selecionar o lote desejado
        df_lote = df_sp.head(quantidade).copy()

        # Gerar endereços completos
        df_lote["endereco_completo"] = df_lote["Endereço"] + ", " + df_lote["CIDADE"] + ", " + df_lote["ESTADO"]

        # Criar lista de endereços com o ponto de partida (Butantã)
        locais = ["Butantã, São Paulo - SP"] + df_lote["endereco_completo"].tolist()

        # Geocodificar os endereços
        try:
            coordenadas = geocode_addresses(locais)
        except Exception as e:
            return render_template("index.html", error=f"Erro na geocodificação: {e}")

        # Obter matriz de distâncias reais com Google
        try:
            matriz_distancias = get_distance_matrix_google(locais)
        except Exception as e:
            return render_template("index.html", error=f"Erro ao calcular matriz de distância: {e}")

        # Calcular rota otimizada
        rota_otimizada, distancia_total = optimize_route(matriz_distancias)

        # Montar relatório A → B → C
        rota_detalhada = []
        for i in range(len(rota_otimizada) - 1):
            origem = locais[rota_otimizada[i]]
            destino = locais[rota_otimizada[i + 1]]
            rota_detalhada.append(f"{origem} → {destino}")

        # Enviar resultado para a tela
        resultado = {
            "rota": [locais[i] for i in rota_otimizada],
            "relatorio": rota_detalhada,
            "distancia_total_km": round(distancia_total, 2)
        }

        return render_template("index.html", resultado=resultado)
