from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpResponseBadRequest
import os
from Usuario import script_criar_usuarios
from Jogo import script_jogos_anteriores

@staff_member_required
def executar_criar_usuarios(request):
    script_criar_usuarios.executar_criacao()
    return HttpResponse("Usuários criados com sucesso.")

@staff_member_required
def executar_importar_jogos(request):
    arquivo = request.GET.get("arquivo")
    mes = request.GET.get("mes")
    ano = request.GET.get("ano")

    if not (arquivo and mes and ano):
        return HttpResponseBadRequest("Parâmetros 'arquivo', 'mes' e 'ano' são obrigatórios.")

    caminho = os.path.join("importacoes", arquivo)
    try:
        script_jogos_anteriores.importar_jogos(caminho, mes, ano)
    except Exception as e:
        return HttpResponse(f"Erro ao importar: {e}", status=500)

    return HttpResponse("Jogos importados com sucesso.")
