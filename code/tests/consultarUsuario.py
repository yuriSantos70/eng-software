import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils import normalizar, valor_reajustado
from data.mock_emprestimos import sistema


def exibir_emprestimos(emprestimos: list, taxa: float) -> None:
    for i, e in enumerate(emprestimos, start=1):
        reajustado = valor_reajustado(e.valor_inicial, taxa, e.data_inicial)
        print(f"  {i}. Data: {e.data_inicial.strftime('%d/%m/%Y')}"
              f" | Valor original: R$ {e.valor_inicial:.2f}"
              f" | Valor reajustado: R$ {reajustado:.2f}"
              f" | Credor: {e.credor.nome}"
              f" | Devedor: {e.devedor.nome}")


# Passo 1 - Usuário insere o nome para pesquisa
nome = input("Nome do usuário: ")

# Passo 2 - Consulta como credor e como devedor
como_credor = sistema.consultarCredor(nome)
como_devedor = sistema.consultarDevedor(nome)

# Fluxo alternativo 2a - Usuário não encontrado no sistema
if como_credor is None:
    print(f"Erro: usuário '{nome}' não encontrado no sistema.")
    exit()

# Fluxo alternativo 2b - Nenhum empréstimo encontrado em nenhuma das categorias
if not como_credor["emprestimos"] and not como_devedor["emprestimos"]:
    print(f"Nenhum empréstimo encontrado para '{nome}'.")
    exit()

# Passo 3 - Exibir empréstimos encontrados
print(f"\n=== Empréstimos de '{nome}' como Credor ===")
if como_credor["emprestimos"]:
    exibir_emprestimos(como_credor["emprestimos"], sistema.taxa)
else:
    print("  Nenhum empréstimo como credor.")
print(f"\nTotal como Credor  (taxa={sistema.taxa*100:.0f}%/mês): R$ {como_credor['total_reajustado']:.2f}\n\n")

print(f"\n=== Empréstimos de '{nome}' como Devedor ===")
if como_devedor["emprestimos"]:
    exibir_emprestimos(como_devedor["emprestimos"], sistema.taxa)
else:
    print("  Nenhum empréstimo como devedor.")

# Passo 4 - Total do valor reajustado

print(f"\nTotal como Devedor (taxa={sistema.taxa*100:.0f}%/mês): R$ {como_devedor['total_reajustado']:.2f}")
