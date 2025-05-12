import requests
import os
from dotenv import load_dotenv 
load_dotenv()

# Chave da API do Google
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def geocode_address(address):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception("Erro na requisição da API de Geocodificação.")

    data = response.json()
    if not data["results"]:
        raise Exception(f"Endereço não encontrado: {address}")

    location = data["results"][0]["geometry"]["location"]
    return (location["lat"], location["lng"])

def geocode_addresses(addresses):
    coordenadas = []
    for address in addresses:
        try:
            coordenadas.append(geocode_address(address))
        except Exception as e:
            print(f"Erro ao geocodificar '{address}': {e}")
            coordenadas.append((None, None))
    return coordenadas
