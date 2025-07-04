from django.contrib.auth.models import User, AbstractUser
from django.db import models

STATUS = [
    ('E', 'Esperando autorização'),
    ('A', 'Ativo'),
    ('I', 'Inativo'),
]

class Usuario(AbstractUser):
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    data_nascimento = models.DateField(blank=True, null=True, verbose_name="Data de Nascimento")
    endereco = models.TextField(blank=True, null=True, verbose_name="Endereço")
    status = models.CharField(max_length=1, choices=STATUS, default='E', verbose_name="Status")

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.first_name + " " + self.last_name
