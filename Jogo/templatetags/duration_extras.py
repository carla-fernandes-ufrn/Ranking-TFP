from django import template

register = template.Library()

@register.filter
def duracao_horas_minutos(value):
    if not value:
        return ""
    total_seconds = int(value.total_seconds())
    horas = total_seconds // 3600
    minutos = (total_seconds % 3600) // 60
    if horas > 0:
        return f"{horas}h {minutos}min"
    return f"{minutos}min"
