import json
import os
from datetime import datetime

from utils import normalizar, valor_reajustado

_PASTA_EMPRESTIMOS = os.path.join(os.path.dirname(__file__), "data", "emprestimos")


class Usuario:
    def __init__(self, nome: str, senha: str):
        self.nome = nome
        self.senha = senha



class Emprestimo:
    def __init__(
        self,
        data_inicial: datetime,
        valor_inicial: float,
        credor: Usuario,
        devedor: Usuario
    ):
        self.data_inicial = data_inicial
        self.valor_inicial = valor_inicial
        self.credor = credor
        self.devedor = devedor

    # Contrato: salvarEmprestimo()
    # Responsabilidade: Salva as informações do empréstimo
    # Pós-condições: Nenhuma
    def salvarEmprestimo(self) -> dict:
        dados = {
            "data": self.data_inicial.strftime("%Y-%m-%d"),
            "valor": self.valor_inicial,
            "credor": self.credor.nome,
            "devedor": self.devedor.nome,
        }
        os.makedirs(_PASTA_EMPRESTIMOS, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
        caminho = os.path.join(_PASTA_EMPRESTIMOS, f"{timestamp}.json")
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        return dados


class Sistema:
    def __init__(self, taxa: float, multa: float, admin_senha: str = "admin123"):
        self.taxa = taxa
        self.multa = multa
        self.admin_senha = admin_senha
        self.usuarios = []
        self.emprestimos = []

    # Contrato: criarEmprestimo(valorInicial, dataAtual, nomeCredor, nomeDevedor, senha)
   
    def criarEmprestimo(
        self,
        valorInicial: float,
        dataAtual: datetime,
        nomeCredor: Usuario,
        nomeDevedor: Usuario,
        senha: str
    ):
        # Passo 3a: Validar campos obrigatórios
        campos_faltando = []
        if valorInicial is None:
            campos_faltando.append("valorInicial")
        if dataAtual is None:
            campos_faltando.append("dataAtual")
        if nomeCredor is None:
            campos_faltando.append("nomeCredor")
        if nomeDevedor is None:
            campos_faltando.append("nomeDevedor")
        if not senha:
            campos_faltando.append("assinatura")

        if campos_faltando:
            return None

        emprestimo = Emprestimo(
            data_inicial=dataAtual,
            valor_inicial=valorInicial,
            credor=nomeCredor,
            devedor=nomeDevedor
        )

        self.emprestimos.append(emprestimo)

        return emprestimo

    # Contrato: validarSenha(novaSenha, confirmacaoSenha)
    # Responsabilidade: Confirmar se as senhas inseridas nos dois campos são compatíveis
    # Pós-condições: Nenhuma
    def validarSenha(self, novaSenha: str, confirmacaoSenha: str) -> bool:
        return novaSenha == confirmacaoSenha

    # Contrato: alterarSenhaAdmin(novaSenha, senhaAtual)
    # Responsabilidade: Alterar a senha de administrador do sistema
    # Pós-condições: admin_senha atualizada
    def alterarSenhaAdmin(self, novaSenha: str, senhaAtual: str) -> bool:
        if self.admin_senha != senhaAtual:
            return False
        self.admin_senha = novaSenha
        return True

    # Contrato: carregarEmprestimos()
    # Responsabilidade: Lê todos os arquivos JSON de data/emprestimos/ e popula self.emprestimos
    # Pós-condições: self.emprestimos atualizado com os dados persistidos
    def carregarEmprestimos(self) -> None:
        if not os.path.isdir(_PASTA_EMPRESTIMOS):
            return
        for arquivo in sorted(os.listdir(_PASTA_EMPRESTIMOS)):
            if not arquivo.endswith(".json"):
                continue
            caminho = os.path.join(_PASTA_EMPRESTIMOS, arquivo)
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
            credor = next(
                (u for u in self.usuarios if normalizar(u.nome) == normalizar(dados["credor"])),
                None
            )
            devedor = next(
                (u for u in self.usuarios if normalizar(u.nome) == normalizar(dados["devedor"])),
                None
            )
            if credor is None or devedor is None:
                continue
            self.emprestimos.append(Emprestimo(
                data_inicial=datetime.strptime(dados["data"], "%Y-%m-%d"),
                valor_inicial=dados["valor"],
                credor=credor,
                devedor=devedor,
            ))

    # Contrato: consultarCredor(nomeUsuario)
    def consultarCredor(self, nomeUsuario: str):
        usuario_existe = any(
            normalizar(u.nome) == normalizar(nomeUsuario) for u in self.usuarios
        )
        if not usuario_existe:
            return None

        emprestimos = [
            e for e in self.emprestimos
            if normalizar(e.credor.nome) == normalizar(nomeUsuario)
        ]
        total = sum(valor_reajustado(e.valor_inicial, self.taxa, e.data_inicial) for e in emprestimos)
        return {"emprestimos": emprestimos, "total_reajustado": total}

    # Contrato: quitarEmprestimo(emprestimo, assinatura)
    # Responsabilidade: Quitar (remover) um empréstimo mediante assinatura do devedor
    # Pós-condições: Empréstimo removido da lista
    def quitarEmprestimo(self, emprestimo, assinatura: str) -> bool:
        if emprestimo.devedor.senha != assinatura:
            return False
        if emprestimo in self.emprestimos:
            self.emprestimos.remove(emprestimo)
            return True
        return False

    # Contrato: consultarDevedor(nomeUsuario)
    def consultarDevedor(self, nomeUsuario: str):
        usuario_existe = any(
            normalizar(u.nome) == normalizar(nomeUsuario) for u in self.usuarios
        )
        if not usuario_existe:
            return None

        emprestimos = [
            e for e in self.emprestimos
            if normalizar(e.devedor.nome) == normalizar(nomeUsuario)
        ]
        total = sum(valor_reajustado(e.valor_inicial, self.taxa, e.data_inicial) for e in emprestimos)
        return {"emprestimos": emprestimos, "total_reajustado": total}