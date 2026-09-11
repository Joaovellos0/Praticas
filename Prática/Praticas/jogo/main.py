import os
import time
import random


def limpar():
    os.system("cls")


class Jogo:
    def __init__(self):
        self.nome = "DRAGONS AND DOGMAS"
        self.lista_de_monstros = []

    def mostrar_nome(self):
        print(self.nome)


class Heroi:
    def __init__(self, nome: str, classe: str, genero: str, vida: int, strength: int):
        self.nome = nome
        self.classe = classe
        self.genero = genero
        self.nivel = 1
        self.experiencia = 0
        self.vida = vida
        self.strength = strength
        self.dano = strength + self.nivel

    def character_sheet(self):
        print(
            f"Nome: {self.nome}\nGenero: {self.genero}\nClasse: {self.classe}\nNível: {self.nivel}\nVida: {self.vida}"
        )

    def causar_dano(self, monstro):
        monstro.vida -= self.dano
        monstro.vida_restante = monstro.vida
        print(f"{self.nome} atacou {monstro}")


class Monstro:
    def __init__(self, tipo: str, nivel: int):
        self.tipo = tipo
        self.nivel = nivel
        self.strength = nivel - 2
        self.vida = 100 + (nivel * nivel)
        self.dano = self.strength + nivel

    def monster_sheet(self):
        print(f"{self.tipo}\n{self.nivel}\n{self.strength}\n{self.vida}, {self.dano}")


lista_de_mobs = []
niveis_mob1 = [3, 5, 7, 9]
nivel_mob1 = random.choice(niveis_mob1)

mob1 = Monstro("Goblin", nivel_mob1)
lista_de_mobs.append(mob1)

niveis_mob2 = [12, 15, 18, 21]
nivel_mob2 = random.choice(niveis_mob2)

mob2 = Monstro("Hobgoblin", nivel_mob2)
lista_de_mobs.append(mob2)

niveis_mob3 = [25, 28, 33, 38]
nivel_mob3 = random.choice(niveis_mob3)

mob3 = Monstro("Grimgoblin", nivel_mob3)
lista_de_mobs.append(mob3)


jogo = Jogo()
jogo.mostrar_nome()

menu_inicial = input("Pressione (ENTER) para começar")

if menu_inicial == "":

    classes = [
        {"Knight": {"Vida": 160, "Força": 12}},
        {"Warrior": {"Vida": 220, "Força": 22}},
        {"Archer": {"Vida": 110, "Força": 8}},
        {"Thief": {"Vida": 115, "Força": 10}},
        {"Assassin": {"Vida": 120, "Força": 18}},
    ]


print("Criador de personagem")
escolher_classe = int(
    input(
        "Escolha a classe:\n\n(1-Knight)\n(2-Warrior)\n(3-Archer)\n(4-Thief)\n(5-Assassin)\n\n"
    )
)

if escolher_classe not in range(1, 6):
    print("Opção inválida.")
else:
    classe = classes[escolher_classe - 1]
    nome_classe = list(classe.keys())[0]
    vida = classe[nome_classe]["Vida"]
    forca = classe[nome_classe]["Força"]


escolher_genero = input("Escolha o gênero do personagem:\n(M) ou (F)\n\n").upper()

if escolher_genero == "M":
    genero = "Masculino"
elif escolher_genero == "F":
    genero = "Feminino"
else:
    print("Opção inválida.")

personagem = Heroi(
    input("Escolha o nome do Personagem: "), nome_classe, genero, vida, forca
)
personagem.character_sheet()

comecar = input("Deseja iniciar uma batalha? (s) ou (n)").lower()

if comecar == "s":
    print("Batalha iniciada.")

    sortear_oponente = random.choice(lista_de_mobs)
    oponente = sortear_oponente
    personagem.causar_dano(oponente)
