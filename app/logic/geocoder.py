import os
import requests


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def geocode_address_google(address):
    """
    Converte um endereço em latitude/longitude usando a Google Geocoding API
    """
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if not data.get("results"):
        raise Exception(f"Endereço não encontrado: {address}")

    location = data["results"][0]["geometry"]["location"]
    return (location["lat"], location["lng"])

def geocode_addresses(addresses):
    """
    Recebe uma lista de endereços e retorna uma lista de tuplas (lat, lng)
    """
    coordenadas = []
    for address in addresses:
        try:
            latlng = geocode_address_google(address)
            coordenadas.append(latlng)
        except Exception as e:
            print(f"[ERRO GEOCODIFICAÇÃO] {address}: {e}")
            coordenadas.append((None, None))
    return coordenadas
