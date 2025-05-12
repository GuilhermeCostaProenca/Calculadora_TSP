import os
import requests

AZURE_MAPS_KEY = os.getenv("AZURE_MAPS_KEY")

def get_distance_matrix_azure(locais):
    """
    locais: lista de endereços (já geocodificados em lat,lng)
    retorna: matriz de distâncias em km entre todos os pontos
    """

    if len(locais) > 50:
        raise Exception("Azure Maps só aceita 50 pontos no Distance Matrix por request.")

    coords_str = ":".join([f"{lat},{lng}" for lat, lng in locais])

    url = (
        f"https://atlas.microsoft.com/route/matrix/json"
        f"?api-version=1.0&subscription-key={AZURE_MAPS_KEY}"
        f"&routeType=fastest&travelMode=car&traffic=false"
    )

    payload = {
        "origins": [{"latitude": lat, "longitude": lng} for lat, lng in locais],
        "destinations": [{"latitude": lat, "longitude": lng} for lat, lng in locais]
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Erro na Distance Matrix da Azure: {response.text}")

    data = response.json()
    distances = data["matrix"]

    # Montar matriz NxN
    tamanho = len(locais)
    matriz = [[0.0] * tamanho for _ in range(tamanho)]

    i = 0
    for r in range(tamanho):
        for c in range(tamanho):
            km = distances[i]["response"]["routeSummary"]["lengthInMeters"] / 1000
            matriz[r][c] = km
            i += 1

    return matriz
