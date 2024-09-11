class ContaBancaria:
    def __init__(self, numero_conta, titular, senha):
        self.numero_conta = numero_conta
        self.titular = titular
        self.senha = senha
        self.saldo = 0.0
        self.extrato = []
        self.limite_saque_diario = 500.0
        self.saques_diarios = 0
        self.limite_saques_por_dia = 3

    def autenticar(self, senha):
        return self.senha == senha

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato.append(f"Depósito: R$ {valor:.2f}")
            print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        else:
            print("Valor de depósito inválido.")

    def sacar(self, valor, senha):
        if not self.autenticar(senha):
            print("Senha incorreta!")
            return
        if valor > self.saldo:
            print("Saldo insuficiente.")
        elif valor > self.limite_saque_diario:
            print("Valor do saque excede o limite diário.")
        elif self.saques_diarios >= self.limite_saques_por_dia:
            print("Número de saques diários excedido.")
        else:
            self.saldo -= valor
            self.extrato.append(f"Saque: R$ {valor:.2f}")
            self.saques_diarios += 1
            print(f"Saque de R$ {valor:.2f} realizado com sucesso.")

    def transferir(self, valor, conta_destino, senha):
        if not self.autenticar(senha):
            print("Senha incorreta!")
            return
        if valor > self.saldo:
            print("Saldo insuficiente para transferência.")
        else:
            self.saldo -= valor
            conta_destino.saldo += valor
            self.extrato.append(f"Transferência de R$ {valor:.2f} para conta {conta_destino.numero_conta}")
            conta_destino.extrato.append(f"Transferência recebida de R$ {valor:.2f} da conta {self.numero_conta}")
            print(f"Transferência de R$ {valor:.2f} para {conta_destino.titular} realizada com sucesso.")

    def mostrar_extrato(self):
        print(f"\nExtrato da conta {self.numero_conta} - Titular: {self.titular}")
        if not self.extrato:
            print("Nenhuma transação realizada.")
        else:
            for operacao in self.extrato:
                print(operacao)
        print(f"Saldo atual: R$ {self.saldo:.2f}\n")

class Banco:
    def __init__(self):
        self.contas = {}

    def criar_conta(self, numero_conta, titular, senha):
        if numero_conta in self.contas:
            print("Número de conta já existe!")
        else:
            nova_conta = ContaBancaria(numero_conta, titular, senha)
            self.contas[numero_conta] = nova_conta
            print(f"Conta criada com sucesso para {titular}.")

    def obter_conta(self, numero_conta):
        return self.contas.get(numero_conta, None)

    def autenticar_conta(self, numero_conta, senha):
        conta = self.obter_conta(numero_conta)
        if conta and conta.autenticar(senha):
            return conta
        else:
            print("Conta ou senha incorreta!")
            return None

# Exemplo de uso
banco = Banco()

# Criando contas
banco.criar_conta(123, "José", "senha123")
banco.criar_conta(456, "Marie", "senha456")


conta_jose = banco.obter_conta(123)
conta_marie = banco.obter_conta(456)

conta_jose.depositar(1000)
conta_jose.sacar(300, "senha123")
conta_jose.mostrar_extrato()

# Transferência entre contas
conta_jose.transferir(200, conta_marie, "senha123")
conta_jose.mostrar_extrato()
conta_marie.mostrar_extrato()
