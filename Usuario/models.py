from django.contrib.auth.models import User
from django.db import models

STATUS = [
    ('E', 'Esperando autorização'),
    ('A', 'Ativo'),
    ('I', 'Inativo'),
]

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    telefone = models.CharField(null=True, blank=True, max_length=20, verbose_name="Telefone")
    data_nascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço")
    status = models.CharField(max_length=1, choices=STATUS, default='E', verbose_name="Status")

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name