import requests
import os

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_distance_matrix(locais):
    """
    locais: lista de endereços
    retorna: matriz NxN com distâncias em km entre todos os pontos
    """
    base_url = "https://maps.googleapis.com/maps/api/distancematrix/json"

    params = {
        "origins": "|".join(locais),
        "destinations": "|".join(locais),
        "key": GOOGLE_API_KEY,
        "units": "metric"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if data.get("status") != "OK":
        raise Exception("Erro na Distance Matrix API: " + str(data))

    matriz = []
    for row in data["rows"]:
        linha = []
        for element in row["elements"]:
            if element["status"] == "OK":
                km = element["distance"]["value"] / 1000  # metros → km
            else:
                km = float("inf")  # se não conseguir calcular
            linha.append(km)
        matriz.append(linha)

    return matriz
