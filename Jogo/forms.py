from django import forms
from datetime import timedelta

from .models import Sorteio, InteresseJogo, Placar

class SorteioForm(forms.ModelForm):
    class Meta:
        model = Sorteio
        # NÃO inclui o status!
        fields = ['mes', 'ano', 'data_inicio_interesses']

class InteresseJogoForm(forms.ModelForm):
    class Meta:
        model = InteresseJogo
        fields = ['quantidade']
        widgets = {
            'quantidade': forms.NumberInput(attrs={
                'min': 0,
                'max': 4,
                'class': 'form-control',
                'placeholder': 'Quantidade desejada (0 a 4)'
            }),
        }

class PlacarForm(forms.ModelForm):

    duracao_horas = forms.IntegerField(required=False, min_value=0, label="Horas")
    duracao_minutos = forms.IntegerField(required=False, min_value=0, max_value=59, label="Minutos")

    class Meta:
        model = Placar
        fields = [
            'set1jogador1',
            'set1jogador2',
            'tiebreak1jogador1',
            'tiebreak1jogador2',
            'set2jogador1',
            'set2jogador2',
            'tiebreak2jogador1',
            'tiebreak2jogador2',
            'supertiejogador1',
            'supertiejogador2',
        ]
        widgets = {
            field: forms.NumberInput(attrs={'min': 0, 'class': 'form-control'})
            for field in fields
        }

    def clean(self):
        cleaned_data = super().clean()

        horas = cleaned_data.get('duracao_horas') or 0
        minutos = cleaned_data.get('duracao_minutos') or 0
        if horas == 0 and minutos == 0:
            cleaned_data['duracao'] = None
        else:
            cleaned_data['duracao'] = timedelta(hours=horas, minutes=minutos)

        # SET 1
        s1j1 = cleaned_data.get('set1jogador1')
        s1j2 = cleaned_data.get('set1jogador2')

        if s1j1 is not None and s1j2 is not None:
            self._validar_set(s1j1, s1j2, "Set 1")

        # SET 2
        s2j1 = cleaned_data.get('set2jogador1')
        s2j2 = cleaned_data.get('set2jogador2')

        if s2j1 is not None and s2j2 is not None:
            self._validar_set(s2j1, s2j2, "Set 2")

        # Tiebreak 1
        tb1j1 = cleaned_data.get('tiebreak1jogador1')
        tb1j2 = cleaned_data.get('tiebreak1jogador2')

        if tb1j1 is not None and tb1j2 is not None:
            self._validar_tiebreak(tb1j1, tb1j2, "Tiebreak 1")

        # Tiebreak 2
        tb2j1 = cleaned_data.get('tiebreak2jogador1')
        tb2j2 = cleaned_data.get('tiebreak2jogador2')

        if tb2j1 is not None and tb2j2 is not None:
            self._validar_tiebreak(tb2j1, tb2j2, "Tiebreak 2")

        # Supertie
        superj1 = cleaned_data.get('supertiejogador1')
        superj2 = cleaned_data.get('supertiejogador2')

        if superj1 is not None and superj2 is not None:
            self._validar_supertie(superj1, superj2)
        
        if (s1j1, s1j2) in [(7,6), (6,7)]:
            if tb1j1 is None or tb1j2 is None:
                raise forms.ValidationError("Set 1 está 7x6 — Tiebreak 1 é obrigatório.")
        if (s2j1, s2j2) in [(7,6), (6,7)]:
            if tb2j1 is None or tb2j2 is None:
                raise forms.ValidationError("Set 2 está 7x6 — Tiebreak 2 é obrigatório.")
        
        s1_winner = 1 if s1j1 and s1j1 > s1j2 else 2 if s1j2 and s1j2 > s1j1 else 0
        s2_winner = 1 if s2j1 and s2j1 > s2j2 else 2 if s2j2 and s2j2 > s2j1 else 0

        if s1_winner and s2_winner and s1_winner != s2_winner:
            if superj1 is None or superj2 is None:
                raise forms.ValidationError("Cada jogador ganhou 1 set — Supertie é obrigatório.")

    def _validar_set(self, a, b, label):
        ganhador, perdedor = max(a, b), min(a, b)
        if (ganhador == 6 and perdedor in [0,1,2,3,4]) or (ganhador == 7 and perdedor in [5,6]):
            return
        raise forms.ValidationError(f"{label} inválido: {ganhador} x {perdedor}")

    def _validar_tiebreak(self, a, b, label):
        ganhador, perdedor = max(a, b), min(a, b)
        if ganhador == 7 and perdedor in [0,1,2,3,4,5]:
            return
        if ganhador > 7 and ganhador - perdedor == 2:
            return
        raise forms.ValidationError(f"{label} inválido: {ganhador} x {perdedor}")

    def _validar_supertie(self, a, b):
        ganhador, perdedor = max(a, b), min(a, b)
        if ganhador == 10 and perdedor in [0,1,2,3,4,5,6,7,8]:
            return
        if ganhador > 10 and ganhador - perdedor == 2:
            return
        raise forms.ValidationError(f"Supertie inválido: {ganhador} x {perdedor}")