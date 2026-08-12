import os

def limpar():
    os.system("cls")

def converter_dolares():
    while True:

        try:
            valor_dolar = float(input("Digite o valor que deseja converter US$: "))

        except ValueError:
            limpar()
            print(f"<{ValueError}>: Digite apenas valores.")
            continue

        valor_real = valor_dolar * 5.13
        print(f"Valor convertido em R$: {valor_real:.2f}")
        break

def converter_euros():
    while True:

        try:
            valor_euro = float(input("Digite o valor que deseja converter €: "))

        except ValueError:
            limpar()
            print(f"<{ValueError}>: Digite apenas valores.")
            continue

        valor_real = valor_euro * 5.93
        print(f"Valor convertido em R$: {valor_real:.2f}")
        break

def converter_reais():
    while True:

        escolher_conversor = input("Deseja converter Real para (1)Dólar ou para (2)Euro?: ")

        if escolher_conversor not in ["1", "2"]:
            print("Comando inválido.")
            continue

        try:
            if escolher_conversor == "1":
                valor_real = float(input("Digite o valor que deseja converter R$: "))
                valor_dolar = valor_real / 5.13

                print(f"Valor convertido em US$: {valor_dolar:.2f}")

            elif escolher_conversor == "2":
                valor_real = float(input("Digite o valor que deseja converter R$: "))
                valor_euro = valor_real / 5.93

                print(f"Valor convertido em €: {valor_euro:.2f}")

        except ValueError:
            print(f"<{ValueError}>: Digite apenas valores.")

while True:

    print("                                             <CONVERSOR DE MOEDAS>\n")
    escolha = input("Escolha: (1)Coverter Dólares para Reais (2)Converter Euros para Reais (3)Converter Reais ou (0)Para encerrar.\n")
    limpar()

    if escolha == "1":
        converter_dolares()

    elif escolha == "2":
        converter_euros()

    elif escolha == "3":
        converter_reais()

    elif escolha == "0":
        break
    
    else:
        print("Comando inválido.")