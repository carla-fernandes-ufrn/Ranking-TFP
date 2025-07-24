from django import template

register = template.Library()

@register.filter
def nome_completo(user):
    if not user:
        return ""
    return f"{user.first_name} {user.last_name}"