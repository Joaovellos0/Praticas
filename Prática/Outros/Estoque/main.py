import funcoes_estoque

estoque = [{"Produto": "arroz", "Quantidade": 280, "Valor": 15.50}]

menu_estoque = input(
    "Digite 1 para acessar o estoque ou 2 para adicionar um novo produto ao estoque:\n"
)

if menu_estoque == "2":
    funcoes_estoque.adicionar_ao_estoque()

else:
    input("Digite uma opção válida.")
