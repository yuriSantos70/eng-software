import unicodedata
from datetime import datetime


def normalizar(texto: str) -> str:
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(c for c in texto if unicodedata.category(c) != "Mn")


def calcular_meses(data_inicial: datetime) -> int:
    hoje = datetime.now()
    return (hoje.year - data_inicial.year) * 12 + (hoje.month - data_inicial.month)


def valor_reajustado(valor_inicial: float, taxa: float, data_inicial: datetime) -> float:
    meses = calcular_meses(data_inicial)
    return valor_inicial * ((1 + taxa) ** meses)
