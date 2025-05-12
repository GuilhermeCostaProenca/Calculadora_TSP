import pandas as pd
from collections import defaultdict

def agrupar_por_estado(df):
    grupos = defaultdict(list)

    for _, row in df.iterrows():
        estado = row["ESTADO"].strip().upper()
        grupos[estado].append(row)

    # Converte os grupos em DataFrames individuais por estado
    grupos_df = {estado: pd.DataFrame(lojas) for estado, lojas in grupos.items()}
    return grupos_df
