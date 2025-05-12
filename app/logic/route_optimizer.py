import itertools

def calcular_distancia_total(rota, matriz):
    return sum(matriz[rota[i]][rota[i+1]] for i in range(len(rota) - 1))

def optimize_route(matriz):
    """
    matriz: matriz NxN com distâncias reais entre os pontos
    retorna: melhor rota (lista de índices), distância total
    """
    indices = list(range(1, len(matriz)))  # sem o ponto inicial (0 = Butantã)
    melhor_rota = None
    menor_distancia = float("inf")

    for perm in itertools.permutations(indices):
        rota = [0] + list(perm)
        distancia = calcular_distancia_total(rota, matriz)
        if distancia < menor_distancia:
            menor_distancia = distancia
            melhor_rota = rota

    return melhor_rota, menor_distancia
