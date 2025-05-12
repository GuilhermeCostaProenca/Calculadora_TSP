import itertools
import math

def calcular_distancia(coord1, coord2):
    # Fórmula da distância Euclidiana simples
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2) * 111  # ~111km por grau

def calcular_distancia_total(rota, coordenadas):
    distancia = 0.0
    for i in range(len(rota) - 1):
        origem = coordenadas[rota[i]]
        destino = coordenadas[rota[i + 1]]
        distancia += calcular_distancia(origem, destino)
    return distancia

def optimize_route(coordenadas):
    # Rota começa no ponto 0 (Butantã), visitando todos os outros e voltando
    indices = list(range(1, len(coordenadas)))  # sem o ponto de partida
    melhor_rota = None
    menor_distancia = float("inf")

    for perm in itertools.permutations(indices):
        rota_atual = [0] + list(perm)
        distancia = calcular_distancia_total(rota_atual, coordenadas)
        if distancia < menor_distancia:
            menor_distancia = distancia
            melhor_rota = rota_atual

    return melhor_rota, menor_distancia
