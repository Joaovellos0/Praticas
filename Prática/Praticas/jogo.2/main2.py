import os
import random
import time


def limpar():
    os.system("cls")


class Entidade:
    def __init__(self, vida: int, nivel: int, forca: int):
        self.vida = vida * nivel
        self.nivel = nivel
        self.forca = forca + nivel
        self.dano = self.nivel * self.forca

    def atacar(self, alvo):
        alvo.vida -= self.dano
        if alvo.vida <= 0:
            alvo.vida = 0


class Heroi(Entidade):
    def __init__(self, vida, forca, classe: str, genero: str, nome: str):
        super().__init__(vida, nivel=20, forca=forca)
        self.experiencia = 0
        self.classe = classe
        self.genero = genero
        self.nome = nome

    def character_sheet(self):
        if self.genero == "Masculino":
            print(
                f"     SEU HEROI\n\nNome: {self.nome}\nClasse: {self.classe}\nGênero: {self.genero}\nNível: {self.nivel}\nVida: {self.vida}\nForça: {self.forca}\n\n"
            )
        elif self.genero == "Feminino":
            print(
                f"     SUA HEROÍNA\n\nNome: {self.nome}\nClasse: {self.classe}\nGênero: {self.genero}\nNível: {self.nivel}\nVida: {self.vida}\nForça: {self.forca}\n\n"
            )


class Inimigo(Entidade):
    def __init__(self, vida, nivel, forca, tipo: str):
        super().__init__(vida=vida, nivel=nivel, forca=forca)
        self.tipo = tipo
        self.xp = self.forca + self.nivel

    def enemy_sheet(self):
        print(
            f"Tipo: {self.tipo}\nNível: {self.nivel}\nVida: {self.vida}\nForça: {self.forca}"
        )


class Chefe(Inimigo):
    def __init__(self, vida, nivel, forca, tipo, nome: str):
        super().__init__(vida=vida, nivel=nivel, forca=forca, tipo=tipo)
        self.nome = nome


def gerar_inimigo():

    tipos_inimigos = [
        {"Goblin": {"Vida": 11, "Força": 7}},
        {"Hobgoblin": {"Vida": 14, "Força": 11}},
        {"Grimgoblin": {"Vida": 20, "Força": 15}},
        {"Greater Goblin": {"Vida": 27, "Força": 22}},
        {"Cyclops": {"Vida": 58, "Força": 41}},
        {"Chimera": {"Vida": 68, "Força": 30}},
        {"Wyvern": {"Vida": 120, "Força": 58}},
    ]

    nivel_gerado = random.choice(range(3, 51))

    if nivel_gerado in range(3, 10):
        inimigo = "Goblin"
    elif nivel_gerado in range(10, 17):
        inimigo = "Hobgoblin"
    elif nivel_gerado in range(17, 25):
        inimigo = "Grimgoblin"
    elif nivel_gerado in range(25, 32):
        inimigo = "Greater Goblin"
    elif nivel_gerado in range(32, 41):
        inimigo = "Cyclops"
    elif nivel_gerado in range(41, 47):
        inimigo = "Chimera"
    elif nivel_gerado in range(47, 51):
        inimigo = "Wyvern"

    for tipo in tipos_inimigos:

        if inimigo in tipo.keys():

            atributo = tipo[inimigo]
            vida = atributo["Vida"]
            forca = atributo["Força"]

            mob = Inimigo(vida, nivel_gerado, forca, inimigo)
            print(mob.enemy_sheet())

            return mob


def limpar():
    os.system("cls")


while True:
    menu_inicial = input("Pressione (ENTER) para entrar ou (0) para sair. ")

    if menu_inicial == 0:
        break
    elif menu_inicial == "":
        limpar()
        classes = [
            {"Knight": {"Vida": 110, "Força": 27}},
            {"Warrior": {"Vida": 80, "Força": 35}},
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

lista_oponentes = []
for i in range(10):
    mob = gerar_inimigo()
    lista_oponentes.append(mob)
    time.sleep(2)
    limpar()

oponentes = lista_oponentes
vida_inicial = personagem.vida

while True:

    comecar = input("Ir para a arena? (s/n)\n").lower()
    limpar()

    if comecar == "n":
        break
    elif comecar == "s":

        oponente = random.choice(oponentes)
        vida_inicial_oponente = oponente.vida
        print(f"O oponente de {personagem.nome} é {oponente.tipo}")
        time.sleep(1.5)

        while True:

            print(
                f"Vida {personagem.nome}: {personagem.vida}         Vida {oponente.tipo}: {oponente.vida}"
            )

            opcoes = ["H", "E"]
            quem_ataca = random.choice(opcoes)

            if quem_ataca == "H":
                personagem.atacar(oponente)
                print(f"{personagem.nome} atacou {oponente.tipo}")
                time.sleep(1)

            elif quem_ataca == "E":
                oponente.atacar(personagem)
                print(f"{oponente.tipo} atacou {personagem.nome}")
                time.sleep(1)

            if personagem.vida <= 0:

                print(
                    f"Vida {personagem.nome}: {personagem.vida}         Vida {oponente.tipo}: {oponente.vida}\n{oponente.tipo} derrotou {personagem.nome}\n"
                )

                personagem.vida = vida_inicial
                oponente.vida = vida_inicial_oponente
                break

            elif oponente.vida <= 0:

                print(
                    f"Vida {personagem.nome}: {personagem.vida}         Vida {oponente.tipo}: {oponente.vida}\n{personagem.nome} derrotou {oponente.tipo}"
                )

                personagem.vida = vida_inicial
                oponentes.remove(oponente)
                oponente = random.choice(oponentes)
                time.sleep(1.2)
                limpar()

                print(f"Próximo oponente: {oponente.tipo}")
                time.sleep(3)
                limpar()
                continue

    else:
        print("Opção inválida.")
        time.sleep(1)
        limpar()
        continue
