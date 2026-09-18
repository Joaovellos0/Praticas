import os
import random
import time


def limpar():
    os.system("cls")


def gerar_numero():
    numeros = []

    for i in range(8):
        numero = random.choice(range(1, 10))
        numeros.append(numero)

    numero = "".join(map(str, numeros))
    return numero


def criar_conta():
    escolha = input("1  (Conta Corrente)         2  (Conta Poupança)\n")
    limpar()

    if escolha == "1":
        user = ContaCorrente(
            input("Escreva seu nome de usuário: "),
            gerar_numero(),
            input("Digite sua senha: "),
        )
        return user

    elif escolha == "2":
        user = ContaPoupanca(
            input("Escreva seu nome de usuário: "),
            gerar_numero(),
            input("Digite sua senha: "),
        )
        return user

    else:
        print("Opção inválida.")


def logar(contas):
    nome = input("Usuário: ")
    limpar()
    senha = input("Digite sua senha: ")
    limpar()

    for conta in contas:
        if nome == conta._titular and senha == conta._senha:
            return conta

    print("Acesso Negado.")


class Conta:
    def __init__(self, titular: str, numero: str, senha: str):
        self._titular = titular
        self._numero = numero
        self._senha = senha
        self._saldo = 0

    def __str__(self):
        return (
            f"Titular: {self._titular}\nNúmero: {self. _numero}\nSenha: {self._senha}"
        )

    def depositar(self):
        saldo_atual = self._saldo
        print(f"Carteira: R$: {saldo_atual:.2f}")
        deposito = float(input("Quanto deseja depositar?:\n"))
        limpar()
        self._saldo += deposito
        print(f"Você depositou R$: {deposito:.2f}\nCarteira: R$: {self._saldo:.2f}\n")

    def sacar(self):
        saque = float(
            input(f"Carteira: R$: {self._saldo:.2f}\nQuanto deseja sacar?:\n")
        )
        if saque < self._saldo:
            print("Saque Negado.")
        else:
            self._saldo -= saque
            print(f"Você sacou R$: {saque:.2f}\nCarteira: R$: {self._saldo:.2f}")


class ContaCorrente(Conta):
    def __init__(self, titular: str, numero: str, senha: str):
        super().__init__(titular, numero, senha)
        self.limite_especial = 2000.00

    def sacar(self):
        saque = float(
            input(f"Carteira: R$: {self._saldo:.2f}\nQuanto deseja sacar?:\n")
        )
        if self._saldo - saque >= -self.limite_especial:
            self._saldo -= saque
            print(f"Você sacou R$: {saque:.2f}\nCarteira: R$: {self._saldo:.2f}\n")
        else:
            print("Saque Negado.")


class ContaPoupanca(Conta):
    def __init__(self, titular: str, numero: str, senha: str):
        super().__init__(titular, numero, senha)
        self.taxa_de_rendimento = 0.05


contas = []

while True:
    escolher = input("1  Login     2  Crie sua conta.     OU digite (SAIR)\n").upper()
    limpar()

    if escolher == "SAIR":
        break

    elif escolher == "1":

        if not contas:
            print("Não há contas registradas.")
            continue

        else:
            usuario = logar(contas)

            if usuario == None:
                continue

            if usuario._saldo == 0:
                print(
                    f"Seja bem vindo(a) {usuario._titular}\nFaça o primeiro depósito na sua conta para acessar as funcionalidades.\n"
                )
                usuario.depositar()

            while True:

                escolher = input(
                    f"Carteira: R$: {usuario._saldo:.2f}\n1  (DEPOSITAR)     2 (SACAR)     3 (SAIR)\n"
                )

                if escolher == "":
                    usuario.depositar()
                elif escolher == "2":
                    usuario.sacar()
                elif escolher == "3":
                    break

    elif escolher == "2":
        usuario = criar_conta()
        if usuario == None:
            continue
        else:
            contas.append(usuario)
            print(usuario)
            time.sleep(2)
            limpar()

    else:
        print("Opção inválida.")
        continue
