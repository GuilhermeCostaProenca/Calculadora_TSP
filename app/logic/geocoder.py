import os
import requests

AZURE_MAPS_KEY = os.getenv("AZURE_MAPS_KEY")

def geocode_address_azure(endereco):
    """
    Converte um endereço para (latitude, longitude) usando Azure Maps
    """
    url = f"https://atlas.microsoft.com/search/address/json"
    params = {
        "api-version": "1.0",
        "subscription-key": AZURE_MAPS_KEY,
        "query": endereco
    }

    response = requests.get(url, params=params)
    data = response.json()

    if not data["results"]:
        raise Exception(f"Endereço não encontrado: {endereco}")

    pos = data["results"][0]["position"]
    return (pos["lat"], pos["lon"])

def geocode_addresses(enderecos):
    coordenadas = []
    for endereco in enderecos:
        try:
            coordenadas.append(geocode_address_azure(endereco))
        except Exception as e:
            print(f"[ERRO] {endereco}: {e}")
            coordenadas.append((None, None))
    return coordenadas
