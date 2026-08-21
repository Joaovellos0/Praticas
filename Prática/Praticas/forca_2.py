import os
import random


def limpar():
    os.system("cls")


lista_de_palavras = [
    "gabinete",
    "memoria ram",
    "fonte",
    "armazenamento",
    "ventoinha",
    "processador",
    "placa-mae",
    "placa de video",
    "chipset",
]

palavras_escolhidas = []

while lista_de_palavras:

    palavra = random.choice(lista_de_palavras)
    lista_de_palavras.remove(palavra)
    palavras_escolhidas.append(palavra)
    palavra = list(palavra)
    palavra_secreta = ["_"] * len(palavra)

    for indice_maquina, letra_maquina in enumerate(palavra):

        if letra_maquina == " " or letra_maquina == "-":
            palavra_secreta[indice_maquina] = letra_maquina

    print("\n          (JOGO DA FORCA SEM FORCA)\n")
    print("Descubra qual é a palavra:", "".join(palavra_secreta))
    print("Dica: A palavra esta ligada a hardware.\n")

    opcao = input("Digite (1) para tentar descobrir ou (0) para encerrar.\n")

    if opcao == "0":
        break

    elif opcao == "1":

        contador = 6

        while contador > 0:

            print(f"\nChances: {contador}\n")
            letra = input("Digite uma letra ou (2) para chutar:\n")
            limpar()

            if letra == "2":

                print("".join(palavra_secreta))
                chute = input("\nChute:\n")
                chute = list(chute)

                if chute == palavra:

                    print("\nParabens, você acertou!")
                    break

                elif chute != palavra:

                    lista_de_palavras.append(palavra)
                    print("Não foi dessa vez.")
                    break

            elif letra not in palavra:

                contador -= 1

                if contador == 0:

                    print(f"Você não conseguiu. Tente outra vez.")
                    lista_de_palavras.append(palavra)
                    break

            else:

                for indice, caractere in enumerate(palavra):

                    if caractere == letra:

                        palavra_secreta[indice] = letra

            print("Progresso:\n ", "".join(palavra_secreta))

            if palavra_secreta == palavra:

                print("Você conseguiu!")
                break

        print(opcao)

    else:

        lista_de_palavras.append(palavra)
        limpar()
        print("Esta opção não existe.")

print("Não há mais palavras para descobrir. Obrigado por jogar :)")
