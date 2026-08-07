import random
import os

def limpar():
    os.system("cls")

lista_de_palavras = [ 'gabinete', 'cpu', 'gpu' ]

palavra = random.choice(lista_de_palavras)

palavra = list(palavra)

palavra_secreta = ['_'] * len(palavra)

print("Descubra a palavra.\nDica: A palavra esta ligada a computadores.")
print(palavra_secreta)

contador_de_erros = 0

while contador_de_erros < 10:

    print(f"Chances: {contador_de_erros}")
    letra = input("Digite uma letra: ")

    if letra not in palavra:
        contador_de_erros += 1

    else:

        for indice, caractere in enumerate(palavra):

            if caractere == letra:
               palavra_secreta[indice] = letra
            
        print(f"Progresso: {palavra_secreta}")

    if palavra == palavra_secreta:

       print("Você conseguiu descobrir a palavra.", "".join(palavra_secreta))
       break


