"""
URL configuration for Ranking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Jogo.urls', namespace='jogo')),
    path('usuario/', include('Usuario.urls', namespace='usuario')),
    path('tfp/', include('Jogo.urls', namespace='jogo')),
    # https://ranking-tfp.onrender.com/executar/criar-usuarios/
    path("executar/criar-usuarios/", executar_criar_usuarios),
    # https://ranking-tfp.onrender.com/executar/importar-jogos/?arquivo=sorteio_rodada_maio.xlsx&mes=5&ano=2025
    # https://ranking-tfp.onrender.com/executar/importar-jogos/?arquivo=Confrontos_Junho.xlsx&mes=6&ano=2025
    # https://ranking-tfp.onrender.com/executar/importar-jogos/?arquivo=Sorteio_Rodada_Julho_Tenis.xlsx&mes=7&ano=2025
    path("executar/importar-jogos/", executar_importar_jogos),
]
