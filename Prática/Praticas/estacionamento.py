import os
import math


def limpar():
    os.system("cls")


hora_entrada = int(input("Digite a hora que o carro entrou no estacionamento:\n"))
limpar()
minutos_entrada = int(input("Digite os minutos da hora de entrada:\n"))
limpar()

hora_saida = int(input("Digite a hora que o carro saiu do estacionamento:\n"))
limpar()
minutos_saida = int(input("Digite os minutos da hora da saida:\n"))
limpar()

# Transformando horas em minutos
hora_da_entrada = hora_entrada * 60 + minutos_entrada
hora_da_saida = hora_saida * 60 + minutos_saida

tempo_estacionado = hora_da_saida - hora_da_entrada

# Passando o resultado acima pra HH : MM
horas = tempo_estacionado // 60
minutos = tempo_estacionado % 60

cada_meia_hora = math.ceil(tempo_estacionado / 30)

valor = cada_meia_hora * 3

print(
    f"Horário de entrada: {hora_entrada} : {minutos_entrada}\nHorário da saída: {hora_saida} : {minutos_saida}\n"
)
print(f"Tempo no estacionamento: {horas} : {minutos}\n")
print(f"R$: {valor},00")
