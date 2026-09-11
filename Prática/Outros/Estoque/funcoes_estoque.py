def adicionar_ao_estoque():
    produto_adicionado = {
        "Produto": input("Adicione seu produto: "),
        "Quantidade": int(input("Informe a quantidade sendo adicionada: ")),
        "Valor": float(input("Informe o valor do produto: ")),
    }
    estoque.append(produto_adicionado)
    print(estoque)
