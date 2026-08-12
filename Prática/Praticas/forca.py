import random
import os

def limpar():
    os.system("cls")

lista_de_palavras = ['placa-mae', 'gabinete', 'memoria-ram', 'cpu', 'gpu' ]

palavra = random.choice(lista_de_palavras)

palavra = list(palavra)

palavra_secreta = ['_'] * len(palavra)

print("Descubra a palavra.\nDica: A palavra esta ligada a computadores.")
print(palavra_secreta)

contador_de_erros = 0

while contador_de_erros < 10:

    chances = print(f"Chances: {contador_de_erros}")
    letra = input("Digite uma letra: ")

    if letra not in palavra:
        contador_de_erros += 1

    else:
        # 1- Achar a posição da letra dentro da palavra. A palavra é uma lista, a letra é um valor. Utilize o método para encontrar o indice de um item em uma lista pelo valor.
        # 2- Utilize um método de lista para substituir o valor em uma posição específica. Substitua pela letra.
