from django.urls import path
from . import views

app_name = 'jogo'

urlpatterns = [
    # Home
    path('', views.HomeView.as_view(), name='home'),

    # Sorteio
    path('sorteios/', views.SorteioListView.as_view(), name='sorteio-list'),
    path('sorteios/<int:pk>/', views.SorteioDetailView.as_view(), name='sorteio-detail'),
    path('sorteios/<int:pk>/sortear', views.sortear, name='sortear'),

    path('sorteios/novo/', views.SorteioCreateView.as_view(), name='sorteio-create'),
    path('sorteios/<int:pk>/editar/', views.SorteioUpdateView.as_view(), name='sorteio-update'),
    path('sorteios/<int:pk>/excluir/', views.SorteioDeleteView.as_view(), name='sorteio-delete'),

    # InteresseJogo
    path('interesses/salvar/', views.interesse_salvar, name='interesse-save'),

    # Placar
    # path('placar/<int:partida_id>/edit/', views.PlacarCreateOrUpdateView.as_view(), name='placar-edit'),
    path('placar/get/<int:partida_id>/', views.get_placar, name='placar-get'),
    path('placar/save/<int:partida_id>/', views.save_placar, name='placar-save'),

    # Partida
    path('partida/get/<int:partida_id>/', views.get_partida, name='partida-get'),
    path('partida/save/<int:partida_id>/', views.save_partida, name='partida-save'),
    path('partida/cancelar/<int:partida_id>/', views.cancelar_partida, name='partida-cancelar'),
    path('partida/locais/', views.lista_locais, name='lista-locais'),

    # Temporada
    path('temporadas/', views.TemporadaListView.as_view(), name="temporada-list"),
    path('temporadas/<int:ano>/', views.TemporadaDetailView.as_view(), name="temporada-detail"),
]
