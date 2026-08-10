palavra = random.choice(lista_de_palavras)
lista_de_palavras.remove(palavra)
palavras_escolhidas.append(palavra)
palavra = list(palavra)
palavra_secreta = ["_"] * len(palavra)

print(palavras_escolhidas)