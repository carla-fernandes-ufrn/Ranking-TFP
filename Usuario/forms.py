from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.models import User
from .models import Usuario

class CriarUsuarioForm(auth_forms.UserCreationForm):
    class Meta:
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'data_nascimento', 'telefone', 'endereco')
        model = Usuario

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nome de usuário'
        self.fields['email'].label = 'E-mail'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Confirmar senha'