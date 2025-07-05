from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.db import transaction

from .forms import CriarUserForm
from .models import Usuario

class Cadastrar(CreateView):
    model = User
    template_name = 'usuario/cadastrar.html'
    success_url = reverse_lazy('usuario:login')
    form_class = CriarUserForm

    def form_valid(self, form):
        user = form.save()
        Usuario.objects.create(
            user=user
        )
        
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))