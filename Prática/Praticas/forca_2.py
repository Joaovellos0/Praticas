import os
import random

def limpar():
    os.system("cls")

lista_de_palavras = [
    "gabinete", "memoria ram", "fonte",
    "armazenamento", "ventoinha",
    "processador", "placa-mae",
    "placa de video", "chipset"
]   

while True:

    palavra = random.choice(lista_de_palavras)
    palavra = list(palavra)
    palavra_secreta = ["_"] * len(palavra)

    for indice_palavra_maquina, letra_palavra_maquina in enumerate(palavra):

        if letra_palavra_maquina == " " or letra_palavra_maquina == "-":
           palavra_secreta[indice_palavra_maquina] = letra_palavra_maquina

    print("\n          (JOGO DA FORCA SEM FORCA)\n")
    print("Descubra qual é a palavra:", "".join(palavra_secreta))
    print("Dica: A palavra esta ligada a hardware.\n")

    opcao = input("Digite (1) para tentar descobrir ou (0) para encerrar.\n")

    if opcao == "0":
       break
            
    elif opcao == "1":
         
         contador = 6

         while contador >= 0:
            
            print(f"Chances: {contador}")
            letra = input("Digite uma letra:\n")
            limpar()

            if letra not in palavra:

               contador -= 1

            elif contador == 0:
                 print(f"Você não conseguiu. Tente outra vez.")
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

        limpar()
        print("Esta opção não existe.")
                
