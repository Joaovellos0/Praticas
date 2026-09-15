import os
import random
import time


def limpar():
    os.system("cls")



class Entidade:
    def __init__(self, vida: int, nivel: int, forca: int):
        self.vida = vida
        self.nivel = nivel
        self.forca = forca
        self.dano = self.nivel * self.forca

    def atacar(self, alvo):
        alvo.vida -= self.dano

class Heroi(Entidade):
    def __init__(self, vida, forca, classe: str, genero: str, nome: str):
        super().__init__(vida=100 + vida, nivel=1, forca=forca)
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


class Chefe(Inimigo):
    def __init__(self, vida, nivel, forca, tipo, nome: str):
        super().__init__(vida=vida, nivel=nivel, forca=forca, tipo=tipo)
        self.nome = nome


def gerar_inimigo():

    tipos_inimigos = [
    {"Goblin": {"Vida": 10, "Força": 2}},
    {"Hobgoblin": {"Vida": 10, "Força": 5}},
    {"Grimgoblin": {"Vida": 10, "Força": 8}},
    {"Greater Goblin": {"Vida": 10, "Força": 10}},
    {"Cyclops": {"Vida": 10, "Força": 15}},
    {"Chimera": {"Vida": 10, "Força": 17}},
    {"Wyvern": {"Vida": 10, "Força": 20}},
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
            vida *= nivel_gerado
            forca += nivel_gerado

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

lista_oponentes = []
for i in range(10):
    mob = gerar_inimigo()
    lista_oponentes.append(mob) 

oponentes = lista_oponentes

while True:

    comecar = input("Ir para a arena? (s/n)\n").lower()
    limpar()

    if comecar == "n":
        break
    elif comecar == "s":
        
        while True:
            oponente = random.choice(oponentes)
            oponentes.remove(oponente)
            print(f"O oponente de {personagem.nome} é {oponente.tipo}")
            time.sleep(1.5)
            print(f"Vida {personagem.nome}: {personagem.vida}         Vida {oponente.tipo}: {oponente.vida}")

            opcoes = ["H", "E"]
            quem_ataca = random.choice(opcoes)

            if quem_ataca == "H":
                personagem.atacar(oponente)
                print(f"{personagem.nome} atacou {oponente.tipo}")

            elif quem_ataca == "E":
                oponente.atacar(personagem)
                print(f"{oponente.tipo} atacou {personagem.nome}")

            if personagem.vida <= 0:
                print(f"{oponente.tipo} derrotou {personagem.nome}")
                break
            elif oponente.vida <= 0:
                print(f"{personagem.nome} derrotou {oponente.tipo}")
                continue
            
                
    else:
        print("Opção inválida.")
        time.sleep(1)
        limpar()
        continue
