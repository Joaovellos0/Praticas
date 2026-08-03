import os

def limpar():
    os.system("cls")
    
num_usuario = int(input("Digite um número para saber sua tabuada:\n"))
limpar()

print(f"Seu número ({num_usuario})\n")

for i in range(1, 11):

     print(f"| {num_usuario} X {i} = {num_usuario * i} |\n")