import math

hora_entrada = int(input("Digite a hora que o carro entrou no estacionamento:\n"))
minutos_entrada = int(input("Digite os minutos da hora de entrada:\n"))

hora_saida = int(input("Digite a hora que o carro saiu do estacionamento:\n"))
minutos_saida = int(input("Digite os minutos da hora da saida:\n"))

#Transformando horas em minutos
hora_da_entrada = hora_entrada * 60 + minutos_entrada
hora_da_saida = hora_saida * 60 + minutos_saida

tempo_estacionado = hora_da_saida - hora_da_entrada

cada_meia_hora = math.ceil(tempo_estacionado / 30)

valor = cada_meia_hora * 3

print(valor)