import os
import requests
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def get_distance_matrix_google(locais):
    if len(locais) > 10:
        raise Exception("Erro: Google permite no máximo 10 locais por requisição.")

    url = "https://maps.googleapis.com/maps/api/distancematrix/json"
    params = {
        "origins": "|".join(locais),
        "destinations": "|".join(locais),
        "key": GOOGLE_API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data.get("status") != "OK":
        raise Exception("Erro na Distance Matrix API: " + str(data))

    matriz = []
    for row in data["rows"]:
        linha = []
        for element in row["elements"]:
            if element["status"] == "OK":
                km = element["distance"]["value"] / 1000
            else:
                km = float("inf")
            linha.append(km)
        matriz.append(linha)

    return matriz
