from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
import random

from django.contrib.auth.models import User

from Jogo.models import Usuario, Sorteio, InteresseJogo, Partida
from Jogo.views import realizar_sorteio  # ajuste o import conforme sua estrutura

User = get_user_model()


class SorteioTestCase(TestCase):
    def setUp(self):
        # Criar 50 jogadoras
        self.jogadoras = []
        for i in range(1, 51):
            user = User.objects.create(
                username=f'tenis_user_{i}',
                first_name=f'Jogadora{i}',
                last_name='Teste'
            )
            self.jogadoras.append(user)

        self.sorteios = []
        # Criar 7 sorteios (meses 1 a 7 de 2025)
        for mes in range(1, 8):
            sorteio = Sorteio.objects.create(
                mes=mes,
                ano=2025,
                data_inicio_interesses=date(2025, mes, 1),
                status='I'
            )
            self.sorteios.append(sorteio)

            # Gerar interesses para cada jogadora entre 3 e 4
            interesses = []
            total = 0
            for jogadora in self.jogadoras:
                qtd = random.randint(3, 4)
                interesses.append((jogadora, qtd))
                total += qtd

            # Se total for ímpar, ajuste o último para garantir paridade
            if total % 2 != 0:
                jogadora, qtd = interesses[-1]
                if qtd == 3:
                    qtd = 4
                else:
                    qtd = 3
                interesses[-1] = (jogadora, qtd)

            # Criar os registros de interesse
            for jogadora, qtd in interesses:
                InteresseJogo.objects.create(
                    jogador=jogadora,
                    sorteio=sorteio,
                    quantidade=qtd
                )

    def test_realizar_sorteios(self):
        """
        Testa todos os 7 sorteios criados.
        """
        for sorteio in self.sorteios:
            print(f"\n🔹 Sorteio: {sorteio.mes}/{sorteio.ano}")
            resultado = realizar_sorteio(sorteio)
            print("Resultado:", resultado)

            partidas = Partida.objects.filter(sorteio=sorteio)
            total_partidas = partidas.count()
            print(f"Total de partidas criadas: {total_partidas}")

            # Verifica duplicidade de duplas no mesmo mês
            duplas_mes = set()
            for p in partidas:
                dupla = tuple(sorted([p.jogador1_id, p.jogador2_id]))
                self.assertNotIn(
                    dupla, duplas_mes,
                    f"❌ Dupla {dupla} repetida no mesmo mês!"
                )
                duplas_mes.add(dupla)

            # Verifica se total de partidas fecha com interesses
            total_interesses = sum(
                i.quantidade for i in InteresseJogo.objects.filter(sorteio=sorteio)
            )
            self.assertEqual(
                total_interesses % 2, 0,
                "❌ Total de interesses deveria ser par!"
            )
            self.assertEqual(
                total_partidas * 2, total_interesses,
                "❌ Número de partidas não fecha com interesses!"
            )
