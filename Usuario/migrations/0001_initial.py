# Generated by Django 5.2.3 on 2025-07-05 17:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefone', models.CharField(max_length=20, verbose_name='Telefone')),
                ('data_nascimento', models.DateField(verbose_name='Data de Nascimento')),
                ('endereco', models.TextField(blank=True, null=True, verbose_name='Endereço')),
                ('status', models.CharField(choices=[('E', 'Esperando autorização'), ('A', 'Ativo'), ('I', 'Inativo')], default='E', max_length=1, verbose_name='Status')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
                'ordering': ['user__first_name', 'user__last_name'],
            },
        ),
    ]
