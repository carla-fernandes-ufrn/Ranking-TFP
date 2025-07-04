from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.db import transaction

from .forms import CriarUsuarioForm
from .models import Usuario

class Cadastrar(CreateView):
    model = Usuario
    template_name = 'usuario/cadastrar.html'
    success_url = reverse_lazy('usuario:login')
    form_class = CriarUsuarioForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))