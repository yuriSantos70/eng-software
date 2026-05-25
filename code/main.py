from datetime import datetime

from utils import normalizar, valor_reajustado


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
    def salvarEmprestimo(self):
        print("=== Empréstimo Salvo ===")
        print(f"Data: {self.data_inicial.strftime('%Y-%m-%d')}")
        print(f"Valor: R$ {self.valor_inicial:.2f}")
        print(f"Credor: {self.credor.nome}")
        print(f"Devedor: {self.devedor.nome}")


class Sistema:
    def __init__(self, taxa: float, multa: float):
        self.taxa = taxa
        self.multa = multa
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