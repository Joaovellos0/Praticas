import random
import os

def limpar():
    os.system("cls")


while True:
    
    escolhas = ["pedra","papel","tesoura"]
   
    escolha_jogador = input("Digite: pedra, papel ou tesoura para jogar, 0 para acabar ou 1 para limpar o histórico de jogadas: ")
    escolha_maquina = random.choice(escolhas)

    while escolha_jogador not in escolhas:
        print("Erro")
        escolha_jogador = input("Digite: pedra, papel ou tesoura para jogar, 0 para acabar ou 1 para limpar o histórico de jogadas: ")
        

    if escolha_jogador == "1":
        limpar()

    elif escolha_jogador == "0":
        print("Obrigado por jogar :)")
        break
    
        
    else:
         print(f"Sua escolha: {escolha_jogador} | Escolha da máquina: {escolha_maquina}")

    
    if escolha_jogador == escolha_maquina:
         print("Empate.")
      
    
    elif escolha_jogador == "pedra" and escolha_maquina == "tesoura" or\
         escolha_jogador == "papel" and escolha_maquina == "pedra" or\
         escolha_jogador == "tesoura" and escolha_maquina == "papel":
        
        print("Você ganhou!")
      
   
    elif escolha_jogador == "tesoura" and escolha_maquina == "pedra" or\
         escolha_jogador == "pedra" and escolha_maquina == "papel" or\
         escolha_jogador == "papel" and escolha_maquina == "tesoura":

        print("Você perdeu.")