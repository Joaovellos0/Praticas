import os

def limpar():
    os.system("cls")

print("-" *15 , end="")
print(" Sequência Fibonacci ", end="")
print("-" * 15)

termos = int(input("\nDigite o número de termos da sequência: "))

a, b = 0, 1
print(f"{a} → {b}", end="")

contador = 3
while contador <= termos:

    c = a + b
    a, b = b, c
    contador += 1

    print(f" → {c}", end="")