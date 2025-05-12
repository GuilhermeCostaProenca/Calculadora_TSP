def dividir_em_lotes(df, tamanho_lote=10):
    """
    Divide o DataFrame em vários lotes com 'tamanho_lote' lojas cada.
    Retorna uma lista de DataFrames (cada um representando uma entrega).
    """
    lotes = []
    total = len(df)
    for i in range(0, total, tamanho_lote):
        lote = df.iloc[i:i + tamanho_lote]
        lotes.append(lote)
    return lotes
