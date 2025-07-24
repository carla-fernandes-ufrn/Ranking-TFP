from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django.contrib.auth.models import User
from Usuario.models import Usuario

SORTEIO = [
    ('I', 'Indicação'),
    ('S', 'Sorteado'),
]

class Sorteio(models.Model):
    mes = models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(12)],verbose_name="Mês")
    ano = models.PositiveIntegerField(validators=[MinValueValidator(2020),MaxValueValidator(2100)],verbose_name="Ano")
    data_inicio_interesses = models.DateField(null=False, blank=False, verbose_name="Data de abertura da indicação de jogos")
    status = models.CharField(max_length=1, default='I', choices=SORTEIO, verbose_name="Status")

    def __str__(self):
        return str(self.mes) + "/" + str(self.ano)

    class Meta:
        ordering = ['-ano', '-mes']
        verbose_name = "Sorteio"
        verbose_name_plural = "Sorteios"

class Local(models.Model):
    nome = models.CharField(max_length=200, null=False, blank=False, verbose_name="Nome")

    def __str__(self):
        return self.nome
    
    class Meta:
        ordering = ['nome']
        verbose_name = "Local"
        verbose_name_plural = "Locais"

class Placar(models.Model):
    set1jogador1 = models.PositiveBigIntegerField(null=False, blank=False, validators=[MinValueValidator(0),MaxValueValidator(7)],verbose_name="Set 1 Jogador 1")
    set1jogador2 = models.PositiveBigIntegerField(null=False, blank=False, validators=[MinValueValidator(0),MaxValueValidator(7)],verbose_name="Set 1 Jogador 2")
    set2jogador1 = models.PositiveBigIntegerField(null=False, blank=False, validators=[MinValueValidator(0),MaxValueValidator(7)],verbose_name="Set 2 Jogador 1")
    set2jogador2 = models.PositiveBigIntegerField(null=False, blank=False, validators=[MinValueValidator(0),MaxValueValidator(7)],verbose_name="Set 2 Jogador 2")
    tiebreak1jogador1 = models.PositiveBigIntegerField(null=True, blank=True, validators=[MinValueValidator(0)],verbose_name="Tie Break 1 Jogador 1")
    tiebreak1jogador2 = models.PositiveBigIntegerField(null=True, blank=True, validators=[MinValueValidator(0)],verbose_name="Tie Break 1 Jogador 2")
    tiebreak2jogador1 = models.PositiveBigIntegerField(null=True, blank=True, validators=[MinValueValidator(0)],verbose_name="Tie Break 2 Jogador 1")
    tiebreak2jogador2 = models.PositiveBigIntegerField(null=True, blank=True, validators=[MinValueValidator(0)],verbose_name="Tie Break 2 Jogador 2")
    supertiejogador1 = models.PositiveBigIntegerField(null=True, blank=True, validators=[MinValueValidator(0)],verbose_name="Supertie Jogador 1")
    supertiejogador2 = models.PositiveBigIntegerField(null=True, blank=True, validators=[MinValueValidator(0)],verbose_name="Supertie Jogador 2")
    vencedor_wo = models.ForeignKey(
        User,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Vencedor por WO"
    )
    
    class Meta:
        verbose_name = "Placar"
        verbose_name_plural = "Placares"
    
STATUS = [
    ('S', 'Sorteado'),
    ('M', 'Marcado'),
    ('R', 'Realizado'),
    ('N', 'Não-realizado'),
]

class Partida(models.Model):
    jogador1 = models.ForeignKey(User, on_delete=models.RESTRICT,verbose_name="Jogador 1", related_name="partidas_j1")
    jogador2 = models.ForeignKey(User, on_delete=models.RESTRICT,verbose_name="Jogador 2", related_name="partidas_j2")
    sorteio = models.ForeignKey(Sorteio, null=True, blank=True, on_delete=models.RESTRICT,verbose_name="Sorteio", related_name="partidas")
    data = models.DateTimeField(null=True, blank=True, verbose_name="Data e hora")
    local = models.ForeignKey(Local, null=True, blank=True, on_delete=models.RESTRICT,verbose_name="Local", related_name="partidas")
    duracao = models.DurationField(blank=True, null=True, verbose_name="Duração")
    status = models.CharField(max_length=1, default='S', choices=STATUS, verbose_name="Status")
    placar = models.OneToOneField(Placar, null=True, blank=True, on_delete=models.RESTRICT,verbose_name="Placar", related_name="partida")
    status_order = models.IntegerField(editable=False, default=0)
    
    @property
    def cor_status(self):
        return {
            'S': 'warning',
            'M': 'primary',
            'R': 'success',
            'N': 'danger'
        }.get(self.status, 'secondary')
    
    @property
    def vencedor(self):
        if not self.placar:
            return None

        sets_j1 = 0
        sets_j2 = 0

        if self.placar.set1jogador1 is not None and self.placar.set1jogador2 is not None:
            sets_j1 += self.placar.set1jogador1 > self.placar.set1jogador2
            sets_j2 += self.placar.set1jogador2 > self.placar.set1jogador1

        if self.placar.set2jogador1 is not None and self.placar.set2jogador2 is not None:
            sets_j1 += self.placar.set2jogador1 > self.placar.set2jogador2
            sets_j2 += self.placar.set2jogador2 > self.placar.set2jogador1

        if self.placar.supertiejogador1 is not None and self.placar.supertiejogador2 is not None:
            sets_j1 += self.placar.supertiejogador1 > self.placar.supertiejogador2
            sets_j2 += self.placar.supertiejogador2 > self.placar.supertiejogador1

        if sets_j1 > sets_j2:
            return self.jogador1
        elif sets_j2 > sets_j1:
            return self.jogador2
        else:
            return None

    def save(self, *args, **kwargs):
        status_map = {'R': 1, 'M': 2, 'S': 3, 'N': 4}
        self.status_order = status_map.get(self.status, 5)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['status_order', 'sorteio__ano', 'sorteio__mes', 'data']
        verbose_name = "Partida"
        verbose_name_plural = "Partidas"

class InteresseJogo(models.Model):
    jogador = models.ForeignKey(User, on_delete=models.RESTRICT,verbose_name="Jogador", related_name="interesses_jogo")
    sorteio = models.ForeignKey(Sorteio, null=True, blank=True, on_delete=models.RESTRICT,verbose_name="Sorteio", related_name="interesses_jogo")
    quantidade = models.PositiveBigIntegerField(null=True, blank=True, validators=[MinValueValidator(0),MaxValueValidator(4)],verbose_name="Quantidade de jogos")

    class Meta:
        ordering = ['sorteio__ano', 'sorteio__mes', 'jogador']
        verbose_name = "Interesse de jogo"
        verbose_name_plural = "Interesses de jogo"
