import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime
from main import Usuario, Emprestimo, Sistema


def test_quitar_emprestimo_fluxo_principal():
    """Fluxo principal: devedor quita empréstimo com assinatura correta."""
    sistema = Sistema(taxa=0.05, multa=0.02)
    credor = Usuario(nome="Carlos", senha="cred123")
    devedor = Usuario(nome="Ana", senha="senha123")
    sistema.usuarios = [credor, devedor]

    emprestimo = sistema.criarEmprestimo(
        valorInicial=1000.00,
        dataAtual=datetime(2024, 1, 10),
        nomeCredor=credor,
        nomeDevedor=devedor,
        senha="senha123"
    )
    assert emprestimo is not None, "Empréstimo deveria ter sido criado"

    resultado = sistema.quitarEmprestimo(emprestimo, "senha123")
    assert resultado is True, "Empréstimo deveria ter sido quitado"
    assert emprestimo not in sistema.emprestimos, "Empréstimo deveria ter sido removido"

    print("test_quitar_emprestimo_fluxo_principal: PASSOU")


def test_quitar_emprestimo_assinatura_incorreta():
    """Fluxo alternativo: assinatura incorreta impede quitação."""
    sistema = Sistema(taxa=0.05, multa=0.02)
    credor = Usuario(nome="Carlos", senha="cred123")
    devedor = Usuario(nome="Ana", senha="senha123")
    sistema.usuarios = [credor, devedor]

    emprestimo = sistema.criarEmprestimo(
        valorInicial=500.00,
        dataAtual=datetime(2024, 6, 1),
        nomeCredor=credor,
        nomeDevedor=devedor,
        senha="senha123"
    )
    assert emprestimo is not None

    resultado = sistema.quitarEmprestimo(emprestimo, "senhaErrada")
    assert resultado is False, "Quitação não deveria ser permitida com assinatura errada"
    assert emprestimo in sistema.emprestimos, "Empréstimo não deveria ter sido removido"

    print("test_quitar_emprestimo_assinatura_incorreta: PASSOU")


def test_admin_nao_pode_criar_emprestimo():
    """Validação: administrador não pode ser credor em um empréstimo."""
    sistema = Sistema(taxa=0.05, multa=0.02)
    admin = Usuario(nome="Admin", senha="admin123", is_admin=True)
    devedor = Usuario(nome="Ana", senha="senha123")
    sistema.usuarios = [admin, devedor]

    emprestimo = sistema.criarEmprestimo(
        valorInicial=200.00,
        dataAtual=datetime.now(),
        nomeCredor=admin,
        nomeDevedor=devedor,
        senha="senha123"
    )
    assert emprestimo is None, "Admin não deveria poder criar empréstimos"

    print("test_admin_nao_pode_criar_emprestimo: PASSOU")


if __name__ == "__main__":
    test_quitar_emprestimo_fluxo_principal()
    test_quitar_emprestimo_assinatura_incorreta()
    test_admin_nao_pode_criar_emprestimo()
    print("\nTodos os testes passaram.")
