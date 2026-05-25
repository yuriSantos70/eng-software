from datetime import datetime
from main import Usuario, Emprestimo, Sistema

# Módulo de empréstimos mockados — apenas para testes

carlos   = Usuario(nome="Carlos",   senha="cred123")
fernanda = Usuario(nome="Fernanda", senha="cred456")
ana      = Usuario(nome="Ana",      senha="senha123")
bruno    = Usuario(nome="Bruno",    senha="dev456")
lucas    = Usuario(nome="Lucas",    senha="luc789")

sistema = Sistema(taxa=0.05, multa=0.02)

sistema.usuarios = [carlos, fernanda, ana, bruno, lucas]

sistema.emprestimos = [
    Emprestimo(
        data_inicial=datetime(2024, 1, 10),
        valor_inicial=1000.00,
        credor=carlos,
        devedor=ana,
    ),
    Emprestimo(
        data_inicial=datetime(2024, 6, 15),
        valor_inicial=2500.00,
        credor=carlos,
        devedor=bruno,
    ),
    Emprestimo(
        data_inicial=datetime(2024, 9, 1),
        valor_inicial=800.00,
        credor=fernanda,
        devedor=carlos,
    ),
    Emprestimo(
        data_inicial=datetime(2025, 3, 20),
        valor_inicial=1500.00,
        credor=ana,
        devedor=fernanda,
    ),
    Emprestimo(
        data_inicial=datetime(2025, 8, 5),
        valor_inicial=3200.00,
        credor=bruno,
        devedor=lucas,
    ),
    Emprestimo(
        data_inicial=datetime(2026, 2, 28),
        valor_inicial=600.00,
        credor=fernanda,
        devedor=ana,
    ),
]
