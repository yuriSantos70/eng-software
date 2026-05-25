import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime
from getpass import getpass
from main import Usuario, Sistema
from data.mock_usuarios import credores, devedores
from utils import normalizar

sistema = Sistema(taxa=0.05, multa=0.02)

# Passo 1 - Credor clica em novo empréstimo
input("[ Novo Empréstimo ] Pressione Enter para continuar...")

# Passo 2 - Informações necessárias para o empréstimo
print("\nPreencha as informações necessárias:")

# Passo 3 - Credor preenche os dados
nome_credor = input("Nome do credor: ")
nome_devedor = input("Nome do devedor: ")
valor_str = input("Valor (R$): ")
data_atual = datetime.now()

# Fluxo alternativo 3a - campos obrigatórios faltando
campos_faltando = []
if not nome_credor.strip():
    campos_faltando.append("nomeCredor")
if not nome_devedor.strip():
    campos_faltando.append("nomeDevedor")
if not valor_str.strip():
    campos_faltando.append("valor")

if campos_faltando:
    print(f"\nErro: campos obrigatórios faltando: {', '.join(campos_faltando)}")
    exit()

valor = float(valor_str)

credor = next((u for u in credores if normalizar(u.nome) == normalizar(nome_credor)), Usuario(nome_credor, senha=""))
devedor = next((u for u in devedores if normalizar(u.nome) == normalizar(nome_devedor)), None)

if devedor is None:
    print(f"\nErro: devedor '{nome_devedor}' não encontrado.")
    exit()

# Passo 4 - Devedor coloca sua assinatura
assinatura = getpass(f"\nAssinatura do devedor ({devedor.nome}): ")

# Fluxo alternativo 4a - assinatura incorreta, com opção de tentar novamente
while devedor.senha != assinatura:
    print("Assinatura incorreta! Tente novamente.")
    assinatura = getpass(f"Assinatura do devedor ({devedor.nome}): ")

# Passo 5 - Empréstimo criado
emprestimo = sistema.criarEmprestimo(
    valorInicial=valor,
    dataAtual=data_atual,
    nomeCredor=credor,
    nomeDevedor=devedor,
    senha=assinatura
)

if emprestimo:
    print("Empréstimo criado com sucesso!")
    emprestimo.salvarEmprestimo()