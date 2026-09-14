import random

tipos_inimigos = [
    {"Goblin": {"Vida": 10, "Força": 2}},
    {"Hobgoblin": {"Vida": 10, "Força": 5}},
    {"Grimgoblin": {"Vida": 10, "Força": 8}},
    {"Greater Goblin": {"Vida": 10, "Força": 10}},
    {"Cyclops": {"Vida": 10, "Força": 15}},
    {"Chimera": {"Vida": 10, "Força": 17}},
    {"Wyvern": {"Vida": 10, "Força": 20}},
]


def gerar_inimigo():

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
