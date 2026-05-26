import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import Usuario


def test_alterar_senha_fluxo_principal():
    """Fluxo principal: administrador altera senha com sucesso."""
    admin = Usuario(nome="Admin", senha="senha123")

    nova_senha = "novaSenha456"
    confirmacao_senha = "novaSenha456"
    senha_atual = "senha123"

    # Passo 1-2: validar se nova senha e confirmação são iguais
    assert admin.validarSenha(nova_senha, confirmacao_senha), \
        "As senhas deveriam ser iguais"

    # Passo 3-4: alterar senha informando a senha atual correta
    resultado = admin.alterarSenha(nova_senha, senha_atual)
    assert resultado is True, "A senha deveria ter sido alterada com sucesso"
    assert admin.senha == nova_senha, "A senha do administrador deveria ser a nova senha"

    print("test_alterar_senha_fluxo_principal: PASSOU")


def test_alterar_senha_fluxo_alternativo_2a():
    """Fluxo alternativo 2a: confirmação de senha diferente da nova senha."""
    admin = Usuario(nome="Admin", senha="senha123")

    nova_senha = "novaSenha456"
    confirmacao_senha = "senhaErrada999"  # senha diferente

    # Passo 2a: senhas não coincidem
    resultado = admin.validarSenha(nova_senha, confirmacao_senha)
    assert resultado is False, "As senhas não deveriam ser iguais"

    print("test_alterar_senha_fluxo_alternativo_2a: PASSOU")
    print("Aviso: as senhas não são iguais.")


def test_alterar_senha_fluxo_alternativo_3a():
    """Fluxo alternativo 3a: senha atual informada incorretamente."""
    admin = Usuario(nome="Admin", senha="senha123")

    nova_senha = "novaSenha456"
    confirmacao_senha = "novaSenha456"
    senha_atual_errada = "senhaErrada000"

    # Passo 1-2: senhas novas coincidem
    assert admin.validarSenha(nova_senha, confirmacao_senha), \
        "As senhas deveriam ser iguais"

    # Passo 3a: senha atual incorreta
    resultado = admin.alterarSenha(nova_senha, senha_atual_errada)
    assert resultado is False, "A alteração não deveria ter sido permitida"
    assert admin.senha == "senha123", "A senha não deveria ter sido alterada"

    print("test_alterar_senha_fluxo_alternativo_3a: PASSOU")
    print("Aviso: a senha atual está incorreta.")


if __name__ == "__main__":
    test_alterar_senha_fluxo_principal()
    test_alterar_senha_fluxo_alternativo_2a()
    test_alterar_senha_fluxo_alternativo_3a()
    print("\nTodos os testes passaram.")
