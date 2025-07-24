# Jogo/script_jogos_anteriores.py

import pandas as pd
from django.contrib.auth.models import User
from Jogo.models import Partida, Sorteio

def importar_jogos(caminho_arquivo, mes, ano):
    try:
        sorteio = Sorteio.objects.get(mes=mes, ano=ano)
    except Sorteio.DoesNotExist:
        raise ValueError(f"Nenhum sorteio encontrado para {mes}/{ano}")

    try:
        df = pd.read_excel(caminho_arquivo)
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo Excel: {e}")

    erros = []
    partidas_validadas = []

    for idx, row in df.iterrows():
        nome1 = str(row['Jogadora A']).strip()
        nome2 = str(row['Jogadora B']).strip()

        try:
            first1, last1 = nome1.split(' ', 1)
            jogador1 = User.objects.get(first_name__iexact=first1, last_name__iexact=last1)
        except Exception as e:
            erros.append(f"Linha {idx+2}: Jogadora A '{nome1}' inválida ({e})")
            continue

        try:
            first2, last2 = nome2.split(' ', 1)
            jogador2 = User.objects.get(first_name__iexact=first2, last_name__iexact=last2)
        except Exception as e:
            erros.append(f"Linha {idx+2}: Jogadora B '{nome2}' inválida ({e})")
            continue

        partidas_validadas.append((jogador1, jogador2))

    if erros:
        raise ValueError("Erros encontrados:\n" + "\n".join(erros))

    for j1, j2 in partidas_validadas:
        Partida.objects.create(jogador1=j1, jogador2=j2, sorteio=sorteio)

    return len(partidas_validadas)
