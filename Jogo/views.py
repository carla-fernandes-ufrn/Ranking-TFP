from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils.timezone import localtime
from django.utils.timezone import now
from django.views.generic import TemplateView
from django.db.models import Q, Count, F, Case, When, IntegerField, Value, CharField
from django.db.models.functions import Concat
from django.db.models.functions import ExtractYear

import io
import openpyxl
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

from django.contrib.auth.models import User

from django.contrib.auth.decorators import user_passes_test
        
import random
from itertools import combinations
from django.db import transaction

from django.db.models import Sum

from .models import Sorteio, InteresseJogo, Partida, Placar, Local
from .forms import SorteioForm, InteresseJogoForm, PlacarForm
from Usuario.models import Usuario

# ======================
# HOME
# ======================

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        today = now().date()
        mes_atual = today.month
        ano_atual = today.year

        # Usuário logado
        usuario = request.user

        # Sorteio do mês atual
        sorteio_atual = Sorteio.objects.filter(mes=mes_atual, ano=ano_atual).first()
        total_pedidos = 0
        interesse_atual = None

        if sorteio_atual:
            total_pedidos = sorteio_atual.interesses_jogo.aggregate(total=Sum('quantidade'))['total'] or 0
            interesse_atual = InteresseJogo.objects.filter(jogador=usuario, sorteio=sorteio_atual).first()
            total = sorteio_atual.partidas.count()
            concluido = sorteio_atual.partidas.filter(status__in=['R', 'N']).count()
            progresso = int((concluido / total) * 100) if total > 0 else 0

            sorteio_atual.total_pedidos = total_pedidos
            sorteio_atual.interesse_do_user = interesse_atual
            sorteio_atual.progresso = progresso

        # Buscar sorteio do mês seguinte
        proximo_mes = mes_atual + 1
        proximo_ano = ano_atual
        if proximo_mes > 12:
            proximo_mes = 1
            proximo_ano += 1

        sorteio_proximo = Sorteio.objects.filter(
            mes=proximo_mes, ano=proximo_ano,
            data_inicio_interesses__lt=today
        ).first()

        if sorteio_proximo:
            interesse_proximo = InteresseJogo.objects.filter(jogador=usuario, sorteio=sorteio_proximo).first()
            sorteio_proximo.interesse_do_user = interesse_proximo or None
            sorteio_proximo.total_pedidos = sorteio_proximo.interesses_jogo.aggregate(total=Sum('quantidade'))['total'] or 0
            total = sorteio_proximo.partidas.count()
            concluido = sorteio_proximo.partidas.filter(status__in=['R', 'N']).count()
            sorteio_proximo.progresso = int((concluido / total) * 100) if total > 0 else 0

        # Partidas do mês atual
        partidas = Partida.objects.filter(
            Q(jogador1=usuario) | Q(jogador2=usuario),
            sorteio__mes=mes_atual,
            sorteio__ano=ano_atual
        ).select_related('placar', 'local')

        partidas_proximas = []
        if sorteio_proximo and sorteio_proximo.status == 'S':
            partidas_proximas = Partida.objects.filter(
                Q(jogador1=usuario) | Q(jogador2=usuario),
                sorteio=sorteio_proximo
            ).select_related('placar', 'local')

        return render(request, 'home.html', {
            'sorteio': sorteio_atual,
            'sorteio_proximo': sorteio_proximo,
            'partidas': partidas,
            'partidas_proximas': partidas_proximas
        })

# ======================
# SORTEIO
# ======================

class SorteioListView(ListView, LoginRequiredMixin):
    model = Sorteio
    template_name = 'jogo/sorteio/listar.html'
    context_object_name = 'lista_sorteios'

    def get_queryset(self):
        qs = super().get_queryset().prefetch_related('partidas')
        for sorteio in qs:
            total = sorteio.partidas.count()

            # Total de pedidos de interesse
            total_pedidos = (
                sorteio.interesses_jogo.aggregate(total=Sum('quantidade'))['total'] or 0
            )

            concluido = sorteio.partidas.filter(status__in=['R', 'N']).count()
            progresso = int((concluido / total) * 100) if total > 0 else 0

            sorteio.progresso = progresso
            sorteio.total_partidas = total
            sorteio.total_pedidos = total_pedidos

            usuario = self.request.user

            interesse = InteresseJogo.objects.filter(
                jogador=self.request.user,
                sorteio=sorteio
            ).first()

            sorteio.interesse_do_user = interesse

        return qs

class SorteioDetailView(DetailView, LoginRequiredMixin):
    model = Sorteio
    template_name = 'jogo/sorteio/detalhe.html'
    context_object_name = 'sorteio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sorteio = self.object

        if sorteio.status == 'S':  # Se sorteado → partidas
            partidas = sorteio.partidas.all().select_related('jogador1', 'jogador2', 'local', 'placar')

            # Filtros
            nome = self.request.GET.get('nome')
            data = self.request.GET.get('data')
            local = self.request.GET.get('local')
            status = self.request.GET.get('status')

            if nome:
                partidas = partidas.annotate(
                    nome_jogador1=Concat('jogador1__first_name', Value(' '), 'jogador1__last_name', output_field=CharField()),
                    nome_jogador2=Concat('jogador2__first_name', Value(' '), 'jogador2__last_name', output_field=CharField())
                ).filter(
                    Q(nome_jogador1__icontains=nome) |
                    Q(nome_jogador2__icontains=nome)
                )
            if data:
                partidas = partidas.filter(data__date=data)
            if local:
                partidas = partidas.filter(local__nome__icontains=local)
            if status:
                partidas = partidas.filter(status=status)

            # ⚡️ Aqui: calcula o vencedor de cada partida
            for partida in partidas:
                vencedor = None

                if hasattr(partida, 'placar') and partida.placar:
                    # Se tiver supertie, decide por ele
                    sj1 = partida.placar.supertiejogador1 or 0
                    sj2 = partida.placar.supertiejogador2 or 0
                    if sj1 or sj2:
                        if sj1 > sj2:
                            vencedor = partida.jogador1
                        elif sj2 > sj1:
                            vencedor = partida.jogador2
                    else:
                        # Soma sets
                        s1j1 = partida.placar.set1jogador1 or 0
                        s1j2 = partida.placar.set1jogador2 or 0
                        s2j1 = partida.placar.set2jogador1 or 0
                        s2j2 = partida.placar.set2jogador2 or 0

                        sets_j1 = 0
                        sets_j2 = 0

                        if s1j1 > s1j2:
                            sets_j1 += 1
                        elif s1j2 > s1j1:
                            sets_j2 += 1

                        if s2j1 > s2j2:
                            sets_j1 += 1
                        elif s2j2 > s2j1:
                            sets_j2 += 1

                        if sets_j1 > sets_j2:
                            vencedor = partida.jogador1
                        elif sets_j2 > sets_j1:
                            vencedor = partida.jogador2

                # partida.vencedor = vencedor

            context['partidas'] = partidas

        elif sorteio.status == 'I':  # Se indicação → interesses
            usuarios = User.objects.order_by('first_name', 'last_name')
            lista = []

            for user in usuarios:
                interesse = InteresseJogo.objects.filter(jogador=user, sorteio=sorteio).first()
                lista.append({
                    'usuario': user,
                    'quantidade': interesse.quantidade if interesse else '-'
                })

            context['interesses'] = lista

        return context
    
@login_required
def exportar_sorteio_xlsx(request, pk):
    sorteio = get_object_or_404(Sorteio, pk=pk)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Sorteio {sorteio.mes}-{sorteio.ano}"

    if sorteio.status == 'I':
        ws.append(["Nome", "Quantidade de Jogos"])
        for interesse in sorteio.interesses_jogo.select_related("jogador"):
            nome = f"{interesse.jogador.first_name} {interesse.jogador.last_name}"
            ws.append([nome, interesse.quantidade])
    elif sorteio.status == 'S':
        ws.append([
            "Jogador 1", "Jogador 2", "Status", "Local", "Data", "Hora",
            "Set1 J1", "Set1 J2", "TB1 J1", "TB1 J2",
            "Set2 J1", "Set2 J2", "TB2 J1", "TB2 J2",
            "Supertie J1", "Supertie J2", "WO"
        ])
        for partida in sorteio.partidas.select_related("jogador1", "jogador2", "local", "placar"):
            placar = partida.placar
            ws.append([
                f"{partida.jogador1.first_name} {partida.jogador1.last_name}",
                f"{partida.jogador2.first_name} {partida.jogador2.last_name}",
                partida.get_status_display(),
                partida.local.nome if partida.local else "",
                partida.data.strftime("%d/%m/%Y") if partida.data else "",
                partida.data.strftime("%H:%M") if partida.data else "",
                placar.set1jogador1 if placar else "",
                placar.set1jogador2 if placar else "",
                placar.tiebreak1jogador1 if placar else "",
                placar.tiebreak1jogador2 if placar else "",
                placar.set2jogador1 if placar else "",
                placar.set2jogador2 if placar else "",
                placar.tiebreak2jogador1 if placar else "",
                placar.tiebreak2jogador2 if placar else "",
                placar.supertiejogador1 if placar else "",
                placar.supertiejogador2 if placar else "",
                f"{placar.vencedor_wo.first_name} {placar.vencedor_wo.last_name}" if placar and placar.vencedor_wo else ""
            ])

    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    filename = f"sorteio_{sorteio.mes}_{sorteio.ano}.xlsx"
    response = HttpResponse(buffer, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required
def exportar_sorteio_pdf(request, pk):
    sorteio = get_object_or_404(Sorteio, pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="sorteio_{sorteio.mes}_{sorteio.ano}.pdf"'

    buffer = []
    if sorteio.status == 'S':
        page_orientation = landscape(A4)
    else:
        page_orientation = A4

    doc = SimpleDocTemplate(response, pagesize=page_orientation)
    styles = getSampleStyleSheet()
    elements = []

    title = f"Sorteio {sorteio.mes}/{sorteio.ano}"
    elements.append(Paragraph(title, styles['Title']))
    elements.append(Spacer(1, 12))

    if sorteio.status == 'I':
        data = [["Nome", "Quantidade de Jogos"]]
        for interesse in sorteio.interesses_jogo.select_related("jogador"):
            nome = f"{interesse.jogador.first_name} {interesse.jogador.last_name}"
            data.append([nome, interesse.quantidade])

    elif sorteio.status == 'S':
        data = [[
            "Jogador 1", "Jogador 2", "Status", "Local", "Data", "Hora",
            "Set1 J1", "Set1 J2", "TB1 J1", "TB1 J2",
            "Set2 J1", "Set2 J2", "TB2 J1", "TB2 J2",
            "Super J1", "Super J2", "WO"
        ]]

        for partida in sorteio.partidas.select_related("jogador1", "jogador2", "local", "placar"):
            placar = partida.placar
            data.append([
                f"{partida.jogador1.first_name} {partida.jogador1.last_name}",
                f"{partida.jogador2.first_name} {partida.jogador2.last_name}",
                partida.get_status_display(),
                partida.local.nome if partida.local else "",
                partida.data.strftime("%d/%m/%Y") if partida.data else "",
                partida.data.strftime("%H:%M") if partida.data else "",
                placar.set1jogador1 if placar else "",
                placar.set1jogador2 if placar else "",
                placar.tiebreak1jogador1 if placar else "",
                placar.tiebreak1jogador2 if placar else "",
                placar.set2jogador1 if placar else "",
                placar.set2jogador2 if placar else "",
                placar.tiebreak2jogador1 if placar else "",
                placar.tiebreak2jogador2 if placar else "",
                placar.supertiejogador1 if placar else "",
                placar.supertiejogador2 if placar else "",
                f"{placar.vencedor_wo.first_name} {placar.vencedor_wo.last_name}" if placar and placar.vencedor_wo else ""
            ])

    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),    # Cabeçalho
        ('FONTSIZE', (0, 1), (-1, -1), 7),   # Corpo da tabela (reduzido para caber mais)
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.black),
    ]))


    elements.append(table)
    doc.build(elements)
    return response


class SorteioCreateView(CreateView, LoginRequiredMixin):
    model = Sorteio
    form_class = SorteioForm
    template_name = 'sorteio/form.html'
    success_url = reverse_lazy('jogo:sorteio-list')

class SorteioUpdateView(UpdateView, LoginRequiredMixin):
    model = Sorteio
    form_class = SorteioForm
    template_name = 'sorteio/form.html'
    success_url = reverse_lazy('jogo:sorteio-list')

class SorteioDeleteView(DeleteView, LoginRequiredMixin):
    model = Sorteio
    template_name = 'sorteio/confirm_delete.html'
    success_url = reverse_lazy('jogo:sorteio-list')

# ======================
# INTERESSE JOGO
# ======================

@login_required
@require_POST
def interesse_salvar(request):
    sorteio_id = request.POST.get('sorteio')
    sorteio = get_object_or_404(Sorteio, pk=sorteio_id)

    usuario = request.user

    interesse, created = InteresseJogo.objects.get_or_create(
        jogador=usuario,
        sorteio=sorteio
    )

    form = InteresseJogoForm(request.POST, instance=interesse)

    if form.is_valid():
        form.instance.jogador = usuario
        form.instance.sorteio = sorteio
        form.save()

        total_pedidos = sorteio.interesses_jogo.aggregate(total=Sum('quantidade'))['total'] or 0

        return JsonResponse({
            'success': True,
            'quantidade': form.instance.quantidade,
            'sorteio_id': sorteio.pk,
            'total_pedidos': total_pedidos
        })

    return JsonResponse({'success': False, 'errors': form.errors})

# ======================
# PARTIDA
# ======================

@login_required
def get_partida(request, partida_id):
    partida = get_object_or_404(Partida, pk=partida_id)
    data = {
        'data': localtime(partida.data).strftime('%Y-%m-%dT%H:%M') if partida.data else '',
        'local_id': partida.local.pk if partida.local else '',
        'local_nome': partida.local.nome if partida.local else ''
    }
    return JsonResponse(data)

@login_required
def save_partida(request, partida_id):
    partida = get_object_or_404(Partida, pk=partida_id)
    if request.method == 'POST':
        local_id = request.POST.get('local')
        data = request.POST.get('data')
        errors = {}

        if local_id:
            partida.local_id = local_id
        else:
            errors['local'] = ['Selecione o local']

        if data:
            partida.data = data
        else:
            errors['data'] = ['Informe a data/hora']

        if errors:
            return JsonResponse({'success': False, 'errors': errors})

        partida.status = 'M'  # Marcar como Marcado
        partida.save()
        return JsonResponse({'success': True})

@login_required
def cancelar_partida(request, partida_id):
    partida = get_object_or_404(Partida, pk=partida_id)
    partida.status = 'N'  # Não-realizado
    partida.data = None   # Zera data
    partida.local = None  # Zera local

    # Se tiver placar, deleta o objeto Placar
    if partida.placar:
        partida.placar.delete()
        partida.placar = None  # Remove o vínculo

    partida.save()
    return JsonResponse({'success': True})

@login_required
def lista_locais(request):
    locais = list(Local.objects.values('id', 'nome'))
    return JsonResponse(locais, safe=False)

# ======================
# PLACAR
# ======================

@login_required
def get_placar(request, partida_id):
    partida = get_object_or_404(Partida, pk=partida_id)
    if partida.placar:
        placar = partida.placar

        data = {
            'duracao_minutos': (int(partida.duracao.total_seconds() % 3600) // 60) if partida.duracao else None,
            'duracao_horas': int(partida.duracao.total_seconds() // 3600) if partida.duracao else None,
            'set1jogador1': placar.set1jogador1,
            'set1jogador2': placar.set1jogador2,
            'set2jogador1': placar.set2jogador1,
            'set2jogador2': placar.set2jogador2,
            'tiebreak1jogador1': placar.tiebreak1jogador1,
            'tiebreak1jogador2': placar.tiebreak1jogador2,
            'tiebreak2jogador1': placar.tiebreak2jogador1,
            'tiebreak2jogador2': placar.tiebreak2jogador2,
            'supertiejogador1': placar.supertiejogador1,
            'supertiejogador2': placar.supertiejogador2,
        }
    else:
        data = {}
    return JsonResponse(data)

@login_required
def save_placar(request, partida_id):
    partida = get_object_or_404(Partida, pk=partida_id)

    if request.method == 'POST':
        if partida.placar:
            placar = partida.placar
        else:
            placar = Placar()

        form = PlacarForm(request.POST, instance=placar)
        if form.is_valid():
            placar = form.save()
            if not partida.placar:
                partida.placar = placar
                partida.save()

            # Atualiza a duração da partida!
            partida.duracao = form.cleaned_data.get('duracao')
            partida.status = 'R'
            partida.save()

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

# ======================
# TEMPORADA
# ======================

class TemporadaListView(TemplateView):
    template_name = 'jogo/temporada/lista.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        anos = (
            Sorteio.objects
            .values_list('ano', flat=True)
            .distinct()
            .order_by('-ano')
        )

        context['anos'] = anos
        return context
    
class TemporadaDetailView(TemplateView):
    template_name = 'jogo/temporada/detalhe.html'

    def get_context_data(self, **kwargs):
        ano = kwargs['ano']
        context = super().get_context_data(**kwargs)

        # Todas partidas do ano
        partidas = Partida.objects.filter(
            sorteio__ano=ano
        ).select_related('jogador1', 'jogador2', 'placar')

        # Inicializa placar por jogadora
        placares = {}

        for partida in partidas:
            j1 = partida.jogador1
            j2 = partida.jogador2

            # Decide quem ganhou
            vencedor = partida.vencedor if hasattr(partida, 'vencedor') else None
            status = partida.status

            for jogador in [j1, j2]:
                if jogador not in placares:
                    placares[jogador] = {
                        'ganhos': 0,
                        'perdidos': 0,
                        'nao_jogados': 0,
                        'pontos': 0
                    }

            if status == 'N':
                # Não realizado
                placares[j1]['nao_jogados'] += 1
                placares[j2]['nao_jogados'] += 1
            elif vencedor == j1:
                placares[j1]['ganhos'] += 1
                placares[j2]['perdidos'] += 1
            elif vencedor == j2:
                placares[j2]['ganhos'] += 1
                placares[j1]['perdidos'] += 1
            else:
                # Partida sem placar ainda?
                placares[j1]['nao_jogados'] += 1
                placares[j2]['nao_jogados'] += 1

        # Calcula pontos
        ranking = []
        for jogador, stats in placares.items():
            pontos = stats['ganhos'] * 100 + stats['perdidos'] * 50
            stats['pontos'] = pontos
            ranking.append((jogador, stats))

        ranking = sorted(ranking, key=lambda x: x[1]['pontos'], reverse=True)

        context['ano'] = ano
        context['ranking'] = ranking

        return context

# ======================
# SORTEIO ALEATÓRIO
# ======================

@login_required
@require_POST
@user_passes_test(lambda u: u.is_superuser)
def sortear(request, pk):
    sorteio = get_object_or_404(Sorteio, pk=pk)
    realizar_sorteio(sorteio)
    print(sorteio)

    return redirect('jogo:sorteio-detail', pk=pk)

def realizar_sorteio(sorteio, max_tentativas=1000):
    """
    Função para realizar o sorteio de partidas de tênis respeitando:
    - Cada partida é dupla única no mesmo mês (ABSOLUTO)
    - Nunca pode repetir com a mesma jogadora nos 3 meses anteriores (ABSOLUTO)
    - Cada jogadora faz o número de jogos solicitado
    - Total de jogos precisa ser par
    - Verifica se há combinações suficientes
    """

    interesses = list(
        InteresseJogo.objects.filter(sorteio=sorteio).select_related('jogador')
    )

    # Filtrar jogadoras com interesse
    interesses_validos = [i for i in interesses if i.quantidade >= 1]
    num_jogadoras = len(interesses_validos)
    total_jogos = sum(i.quantidade for i in interesses_validos)

    if num_jogadoras < 2:
        raise Exception("Precisa de pelo menos 2 jogadoras com interesse >= 1.")

    if total_jogos % 2 != 0:
        raise Exception(
            f"A soma total de jogos ({total_jogos}) é ímpar. Ajuste para ser par."
        )

    # Máximo de partidas únicas possíveis no mês
    max_duplas_mes = (num_jogadoras * (num_jogadoras - 1)) // 2
    total_partidas_necessarias = total_jogos // 2

    if total_partidas_necessarias > max_duplas_mes:
        raise Exception(
            f"Não é possível atender {total_partidas_necessarias} partidas com apenas {num_jogadoras} jogadoras "
            f"sem repetir duplas no mesmo mês. Máximo possível: {max_duplas_mes} partidas únicas."
        )

    # Estrutura de jogadores
    jogadores = {
        i.jogador.id: {
            'usuario': i.jogador,
            'restantes': i.quantidade
        }
        for i in interesses_validos
    }
    ids_jogadores = list(jogadores.keys())

    # Histórico de partidas do mesmo mês
    partidas_mes = Partida.objects.filter(
        sorteio=sorteio
    ).values_list('jogador1_id', 'jogador2_id')

    duplas_mes = set(tuple(sorted(p)) for p in partidas_mes)

    # Histórico de partidas nos últimos 3 meses
    meses_previos = []
    mes = sorteio.mes
    ano = sorteio.ano

    for i in range(1, 4):  # 3 meses anteriores
        m = mes - i
        y = ano
        if m <= 0:
            m += 12
            y -= 1
        meses_previos.append((m, y))

    partidas_periodo = Partida.objects.filter(
        sorteio__ano__in=[y for m, y in meses_previos],
        sorteio__mes__in=[m for m, y in meses_previos]
    ).values_list('jogador1_id', 'jogador2_id')

    duplas_periodo = set(tuple(sorted(p)) for p in partidas_periodo)

    # Loop principal — restrição ABSOLUTA
    for tentativa in range(max_tentativas):
        if _tentar_sortear(
            ids_jogadores, jogadores, duplas_mes, duplas_periodo, sorteio
        ):
            sorteio.status='S'
            sorteio.save()
            return f"Sorteio concluído após {tentativa+1} tentativa(s) evitando repetição no mês e nos 3 meses anteriores."

    # NÃO há fallback: restrição absoluta!
    raise Exception(
        f"Não foi possível gerar todas as partidas sem repetir no mês ou nos 3 meses anteriores.\n"
        f"Verifique interesses ou ajuste restrições."
    )


def _tentar_sortear(ids_jogadores, jogadores, duplas_mes, duplas_bloqueadas, sorteio):
    """
    Função auxiliar que tenta gerar o sorteio com as restrições recebidas:
    - duplas_mes: NUNCA pode repetir (ABSOLUTO)
    - duplas_bloqueadas: NUNCA pode repetir nos últimos 3 meses (ABSOLUTO)
    """
    possiveis_duplas = list(combinations(ids_jogadores, 2))
    random.shuffle(possiveis_duplas)

    jogadores_tmp = {k: dict(v) for k, v in jogadores.items()}
    duplas_mes_tmp = set(duplas_mes)
    duplas_bloqueadas_tmp = set(duplas_bloqueadas)
    partidas_tentativa = []

    progresso = True

    while progresso:
        progresso = False

        for id1, id2 in possiveis_duplas:
            id1, id2 = sorted((id1, id2))
            j1 = jogadores_tmp[id1]
            j2 = jogadores_tmp[id2]

            if j1['restantes'] <= 0 or j2['restantes'] <= 0:
                continue

            if (id1, id2) in duplas_mes_tmp:
                continue

            if (id1, id2) in duplas_bloqueadas_tmp:
                continue

            partidas_tentativa.append((id1, id2))
            duplas_mes_tmp.add((id1, id2))
            duplas_bloqueadas_tmp.add((id1, id2))
            j1['restantes'] -= 1
            j2['restantes'] -= 1

            progresso = True

    ainda_faltam = [
        j['restantes'] for j in jogadores_tmp.values() if j['restantes'] > 0
    ]

    if sum(ainda_faltam) == 0:
        with transaction.atomic():
            for id1, id2 in partidas_tentativa:
                Partida.objects.create(
                    jogador1=jogadores[id1]['usuario'],
                    jogador2=jogadores[id2]['usuario'],
                    sorteio=sorteio
                )
        return True

    return False

