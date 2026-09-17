import os
import random
import time


def limpar():
    os.system("cls")


class Entidade:
    def __init__(self, vida: int, nivel: int, forca: int):
        self.vida = vida * nivel
        self.nivel = nivel
        self.forca = (forca + nivel) // 2
        self.dano = self.nivel * self.forca
        self.tipo_nome = "Entidade"

    def causar_dano(self, alvo):
        print(f"{self.tipo_nome} atacou {alvo.tipo_nome}")
        time.sleep(1)
        alvo.levar_dano(self)

    def levar_dano(self, alvo):
        dano = alvo.dano
        self.vida -= alvo.dano
        if self.vida <= 0:
            self.vida = 0
        print(f"{self.tipo_nome} recebeu {dano} de dano de {alvo.tipo_nome}\n")
        time.sleep(1)


class Heroi(Entidade):
    def __init__(self, vida: int, forca: int, classe: str, genero: str, nome: str):
        super().__init__(vida, nivel=50, forca=forca)
        self.experiencia = 0
        self.classe = classe
        self.genero = genero
        self.nome = nome
        self.tipo_nome = self.nome

    def __str__(self):
        if self.genero == "Masculino":
            return(
                f"     SEU HEROI\n\nNome: {self.nome}\nClasse: {self.classe}\nGênero: {self.genero}\nNível: {self.nivel}\nVida: {self.vida}\nForça: {self.forca}\n\n"
            )
        elif self.genero == "Feminino":
            return(
                f"     SUA HEROÍNA\n\nNome: {self.nome}\nClasse: {self.classe}\nGênero: {self.genero}\nNível: {self.nivel}\nVida: {self.vida}\nForça: {self.forca}\n\n"
            )


class Inimigo(Entidade):
    def __init__(self, vida, nivel, forca, tipo: str):
        super().__init__(vida=vida, nivel=nivel, forca=forca)
        self.tipo = tipo
        self.xp = self.forca + self.nivel
        self.tipo_nome = self.tipo

    def __str__(self):
        return(
            f"Tipo: {self.tipo}\nNível: {self.nivel}\nVida: {self.vida}\nForça: {self.forca}"
        )


class Chefe(Inimigo):
    def __init__(self, vida, nivel, forca, tipo, nome: str):
        super().__init__(vida=vida, nivel=nivel, forca=forca, tipo=tipo)
        self.nome = nome


def gerar_inimigo():

    tipos_inimigos = [
        {"Goblin": {"Vida": 19, "Força": 9}},
        {"Hobgoblin": {"Vida": 25, "Força": 15}},
        {"Grimgoblin": {"Vida": 34, "Força": 21}},
        {"Greater Goblin": {"Vida": 48, "Força": 30}},
        {"Cyclops": {"Vida": 83, "Força": 51}},
        {"Chimera": {"Vida": 120, "Força": 36}},
        {"Wyvern": {"Vida": 142, "Força": 67}},
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
        print(personagem)
        break

    else:
        print("Opção inválida.")
        time.sleep(1)
        limpar()
        continue

lista_oponentes = []
for i in range(3):
    mob = gerar_inimigo()
    lista_oponentes.append(mob)

oponentes = lista_oponentes
vida_inicial = personagem.vida

while len(oponentes) > 0:

    comecar = input("Ir para a arena? (s/n)\n").lower()
    limpar()

    if comecar == "n":
        break
    elif comecar == "s":

        oponente = random.choice(oponentes)
        vida_inicial_oponente = oponente.vida
        print(f"O oponente de {personagem.nome} é {oponente.tipo}")
        print(oponente)
        time.sleep(3)
        limpar()

        while True:

            print(
                f"Vida {personagem.nome}: {personagem.vida}         Vida {oponente.tipo}: {oponente.vida}\n"
            )

            opcoes = ["H", "E"]
            quem_ataca = random.choice(opcoes)

            if quem_ataca == "H":
                personagem.causar_dano(oponente)

            elif quem_ataca == "E":
                oponente.causar_dano(personagem)

            if personagem.vida <= 0:

                print(
                    f"Vida {personagem.nome}: {personagem.vida}         Vida {oponente.tipo}: {oponente.vida}\n{oponente.tipo} derrotou {personagem.nome}\n"
                )

                oponente.vida = vida_inicial_oponente
                personagem.vida = vida_inicial
                break

            elif oponente.vida <= 0:

                print(
                    f"Vida {personagem.nome}: {personagem.vida}         Vida {oponente.tipo}: {oponente.vida}\n{personagem.nome} derrotou {oponente.tipo}\n"
                )

                personagem.vida = vida_inicial
                oponentes.remove(oponente)
                if not oponentes:
                    print(f"{personagem.nome} derrotou todos os inimigos!\n")
                    break
                else:
                    oponente = random.choice(oponentes)
                    vida_inicial_oponente = oponente.vida
                    input()
                    limpar()

                    print(f"Próximo oponente: {oponente.tipo}")
                    print(oponente)
                    time.sleep(3)
                    limpar()
                    continue

    else:
        print("Opção inválida.")
        time.sleep(1)
        limpar()
        continue

