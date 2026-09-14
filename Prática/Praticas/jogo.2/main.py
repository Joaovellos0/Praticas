import os
import random
import time

from gerador_de_mobs import gerar_inimigo


def limpar():
    os.system("cls")


class Entidade:
    def __init__(self, vida: int, nivel: int, forca: int):
        self.vida = vida
        self.nivel = nivel
        self.forca = forca
        self.dano = self.nivel * self.forca


class Heroi(Entidade):
    def __init__(self, vida, forca, classe: str, genero: str, nome: str):
        super().__init__(vida=100 + vida, nivel=1, forca=forca)
        self.experiencia = 0
        self.classe = classe
        self.genero = genero
        self.nome = nome

    def character_sheet(self):
        if genero == "Masculino":
            print(
                f"     SEU HEROI\n\nNome: {self.nome}\nClasse: {self.classe}\nGênero: {self.genero}\nNível: {self.nivel}\nVida: {self.vida}\nForça: {self.forca}\n\n"
            )
        elif genero == "Feminino":
            print(
                f"     SUA HEROÍNA\n\nNome: {self.nome}\nClasse: {self.classe}\nGênero: {self.genero}\nNível: {self.nivel}\nVida: {self.vida}\nForça: {self.forca}\n\n"
            )


class Inimigo(Entidade):
    def __init__(self, vida, nivel, forca, tipo: str):
        super().__init__(vida=vida, nivel=nivel, forca=forca)
        self.tipo = tipo
        self.xp = self.forca + self.nivel


class Chefe(Inimigo):
    def __init__(self, vida, nivel, forca, tipo, nome: str):
        super().__init__(vida=vida, nivel=nivel, forca=forca, tipo=tipo)
        self.nome = nome


while True:
    menu_inicial = input("Pressione (ENTER) para entrar ou (0) para sair. ")

    if menu_inicial == 0:
        break
    elif menu_inicial == "":
        limpar()
        classes = [
            {"Knight": {"Vida": 80, "Força": 25}},
            {"Warrior": {"Vida": 100, "Força": 32}},
        ]
        print("Criador de Personagem")

        while True:

            escolher_classe = int(
                input(
                    "Escolha a classe do seu herói:\n\n(1 - Knight) (2 - Warrior)\n\n"
                )
            )
            if escolher_classe not in range(1, 3):
                print("Opção inválida.")
                time.sleep(1)
                limpar()
                continue
            else:
                classe = classes[escolher_classe - 1]
                nome_classe = list(classe.keys())[0]
                vida = classe[nome_classe]["Vida"]
                forca = classe[nome_classe]["Força"]
                break

        while True:

            escolher_genero = input(
                "Escolha (M) para Masculino ou (F) para Feminino: "
            ).upper()

            if escolher_genero == "M":
                genero = "Masculino"
                time.sleep(0.5)
                limpar()
                break
            elif escolher_genero == "F":
                genero = "Feminino"
                time.sleep(0.5)
                limpar()
                break
            else:
                print("Opção inválida.")
                time.sleep(1)
                limpar()
                continue

        personagem = Heroi(
            vida, forca, nome_classe, genero, input("Escreva o Nome do personagem: ")
        )
        limpar()
        personagem.character_sheet()
        break

    else:
        print("Opção inválida.")
        time.sleep(1)
        limpar()
        continue

comecar = input("Ir para a arena? (s/n)").lower()
