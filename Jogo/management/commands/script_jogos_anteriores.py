from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Jogo.models import Partida, Sorteio
import pandas as pd

class Command(BaseCommand):
    help = 'Importa partidas de um arquivo Excel com colunas Jogadora A e Jogadora B'

    def add_arguments(self, parser):
        parser.add_argument('arquivo', type=str, help='Caminho para o arquivo Excel')
        parser.add_argument('mes', type=int, help='Mês do sorteio')
        parser.add_argument('ano', type=int, help='Ano do sorteio')

    def handle(self, *args, **kwargs):
        arquivo = kwargs['arquivo']
        mes = kwargs['mes']
        ano = kwargs['ano']

        try:
            sorteio = Sorteio.objects.get(mes=mes, ano=ano)
        except Sorteio.DoesNotExist:
            self.stderr.write(self.style.ERROR(f"Nenhum sorteio encontrado para {mes}/{ano}"))
            return

        try:
            df = pd.read_excel(arquivo)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Erro ao ler o arquivo Excel: {e}"))
            return

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
            self.stderr.write(self.style.ERROR("❌ Erros encontrados, importação cancelada:"))
            for erro in erros:
                self.stderr.write(f"- {erro}")
            return

        # ✅ Nenhum erro, podemos criar as partidas
        for j1, j2 in partidas_validadas:
            Partida.objects.create(jogador1=j1, jogador2=j2, sorteio=sorteio)
            self.stdout.write(f"✓ {j1.first_name} {j1.last_name} x {j2.first_name} {j2.last_name}")

        self.stdout.write(self.style.SUCCESS(f"{len(partidas_validadas)} partidas importadas com sucesso."))
