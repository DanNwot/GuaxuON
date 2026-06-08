from django import template

register = template.Library()

@register.filter(name='mascara_documento')
def mascara_documento(value):
    """Aplica máscara de CPF ou CNPJ dinamicamente removendo caracteres extras primeiro"""
    if not value:
        return ""
    
    # Remove qualquer formatação residual que venha do banco
    documento = "".join(digit for digit in str(value) if digit.isdigit())
    
    # Se for CPF
    if len(documento) == 11:
        return f"{documento[:3]}.{documento[3:6]}.{documento[6:9]}-{documento[9:]}"
    
    # Se for CNPJ
    elif len(documento) == 14:
        return f"{documento[:2]}.{documento[2:5]}.{documento[5:8]}/{documento[8:12]}-{documento[12:]}"
    
    # Caso seja uma inscrição estadual ou formato desconhecido, retorna o valor original
    return value