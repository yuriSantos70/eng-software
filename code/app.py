import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime

from main import Usuario
from data.mock_emprestimos import sistema
from utils import normalizar, valor_reajustado


def ler_senha(prompt: str) -> str:
    return input(prompt)


# ── helpers ────────────────────────────────────────────────────────────────────

def exibir_emprestimos(emprestimos: list, taxa: float) -> None:
    for i, e in enumerate(emprestimos, start=1):
        reajustado = valor_reajustado(e.valor_inicial, taxa, e.data_inicial)
        print(f"  {i}. Data: {e.data_inicial.strftime('%d/%m/%Y')}"
              f" | Valor original: R$ {e.valor_inicial:.2f}"
              f" | Valor reajustado: R$ {reajustado:.2f}"
              f" | Credor: {e.credor.nome}"
              f" | Devedor: {e.devedor.nome}")


# ── casos de uso ───────────────────────────────────────────────────────────────

def criar_emprestimo() -> None:
    print("\n=== Novo Empréstimo ===")

    nome_credor  = input("Nome do credor: ").strip()
    nome_devedor = input("Nome do devedor: ").strip()
    valor_str    = input("Valor (R$): ").strip()

    # Fluxo alternativo 3a — campos obrigatórios faltando
    campos_faltando = []
    if not nome_credor:
        campos_faltando.append("nomeCredor")
    if not nome_devedor:
        campos_faltando.append("nomeDevedor")
    if not valor_str:
        campos_faltando.append("valor")

    if campos_faltando:
        print(f"Erro: campos obrigatórios faltando: {', '.join(campos_faltando)}")
        return

    try:
        valor = float(valor_str)
    except ValueError:
        print("Erro: valor inválido.")
        return

    credor = next(
        (u for u in sistema.usuarios if normalizar(u.nome) == normalizar(nome_credor)),
        Usuario(nome_credor, senha="")
    )
    devedor = next(
        (u for u in sistema.usuarios if normalizar(u.nome) == normalizar(nome_devedor)),
        None
    )

    if devedor is None:
        print(f"Erro: devedor '{nome_devedor}' não encontrado.")
        return

    # Fluxo alternativo — admin não pode ser credor
    if credor.is_admin:
        print("Erro: administrador não pode ser credor.")
        return

    # Passo 4 — devedor assina
    assinatura = ler_senha(f"Assinatura do devedor ({devedor.nome}): ")

    # Fluxo alternativo 4a — assinatura incorreta
    while devedor.senha != assinatura:
        print("Assinatura incorreta! Tente novamente.")
        assinatura = ler_senha(f"Assinatura do devedor ({devedor.nome}): ")

    emprestimo = sistema.criarEmprestimo(
        valorInicial=valor,
        dataAtual=datetime.now(),
        nomeCredor=credor,
        nomeDevedor=devedor,
        senha=assinatura
    )

    if emprestimo:
        dados = emprestimo.salvarEmprestimo()
        print(f"Empréstimo criado com sucesso! "
              f"(credor: {dados['credor']} → devedor: {dados['devedor']}, R$ {dados['valor']:.2f})")
    else:
        print("Erro ao criar empréstimo.")


def consultar_usuario() -> None:
    print("\n=== Consultar Usuário ===")
    nome = input("Nome do usuário: ").strip()

    como_credor  = sistema.consultarCredor(nome)

    # Fluxo alternativo 2a — usuário não encontrado
    if como_credor is None:
        print(f"Usuário '{nome}' não encontrado no sistema.")
        return

    como_devedor = sistema.consultarDevedor(nome)

    # Fluxo alternativo 2b — nenhum empréstimo encontrado
    if not como_credor["emprestimos"] and not como_devedor["emprestimos"]:
        print(f"Nenhum empréstimo encontrado para '{nome}'.")
        return

    print(f"\n=== '{nome}' como Credor ===")
    if como_credor["emprestimos"]:
        exibir_emprestimos(como_credor["emprestimos"], sistema.taxa)
    else:
        print("  Nenhum empréstimo como credor.")
    print(f"  Total reajustado: R$ {como_credor['total_reajustado']:.2f}")

    print(f"\n=== '{nome}' como Devedor ===")
    if como_devedor["emprestimos"]:
        exibir_emprestimos(como_devedor["emprestimos"], sistema.taxa)
    else:
        print("  Nenhum empréstimo como devedor.")
    print(f"  Total reajustado: R$ {como_devedor['total_reajustado']:.2f}")


def quitar_emprestimo() -> None:
    print("\n=== Quitar Empréstimo ===")
    nome_devedor = input("Nome do devedor: ").strip()

    como_devedor = sistema.consultarDevedor(nome_devedor)
    if como_devedor is None:
        print(f"Usuário '{nome_devedor}' não encontrado no sistema.")
        return

    emprestimos = como_devedor["emprestimos"]
    if not emprestimos:
        print(f"Nenhum empréstimo em aberto para '{nome_devedor}'.")
        return

    print(f"\nEmpréstimos em aberto de '{nome_devedor}':")
    exibir_emprestimos(emprestimos, sistema.taxa)

    escolha_str = input("\nNúmero do empréstimo a quitar (0 para cancelar): ").strip()
    try:
        escolha = int(escolha_str)
    except ValueError:
        print("Opção inválida.")
        return

    if escolha == 0:
        return
    if escolha < 1 or escolha > len(emprestimos):
        print("Número inválido.")
        return

    emprestimo_escolhido = emprestimos[escolha - 1]
    devedor = emprestimo_escolhido.devedor

    assinatura = ler_senha(f"Assinatura do devedor ({devedor.nome}): ")

    resultado = sistema.quitarEmprestimo(emprestimo_escolhido, assinatura)
    if resultado:
        print(f"Empréstimo quitado com sucesso! "
              f"Valor: R$ {emprestimo_escolhido.valor_inicial:.2f}")
    else:
        print("Assinatura incorreta. Quitação cancelada.")


def alterar_senha_admin() -> None:
    print("\n=== Alterar Senha (Admin) ===")

    # Passo 2 — loop até as senhas coincidirem
    while True:
        nova_senha  = ler_senha("Nova senha: ")
        confirmacao = ler_senha("Confirme a nova senha: ")
        if sistema.validarSenha(nova_senha, confirmacao):
            break
        print("Erro: as senhas não coincidem. Tente novamente.")

    # Passo 3 — loop até a senha atual estar correta
    while True:
        senha_atual = ler_senha("Senha atual do admin: ")
        if sistema.alterarSenhaAdmin(nova_senha, senha_atual):
            print("Senha alterada com sucesso!")
            break
        print("Erro: senha atual incorreta. Tente novamente.")


# ── menu principal ─────────────────────────────────────────────────────────────

def main() -> None:
    sistema.carregarEmprestimos()

    opcoes = {
        "1": ("Criar empréstimo",   criar_emprestimo),
        "2": ("Consultar usuário",  consultar_usuario),
        "3": ("Quitar empréstimo",  quitar_emprestimo),
        "4": ("Alterar senha admin", alterar_senha_admin),
    }

    while True:
        print("\n=== Sistema de Empréstimos ===")
        for k, (label, _) in opcoes.items():
            print(f"  {k}. {label}")
        print("  0. Sair")

        opcao = input("Opção: ").strip()
        if opcao == "0":
            print("Saindo...")
            break
        elif opcao in opcoes:
            opcoes[opcao][1]()
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()

