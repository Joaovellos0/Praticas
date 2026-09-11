while True:

    usuario = input("Digite seu nome de usuário: ")

    if len(usuario) > 12:
        print("Nome de usuário possui no máximo 12 caracteres.")
        continue
    elif not usuario.find(" ") == -1:
        print("Nome de usuário não aceita espaços")
    elif usuario.isalpha(False):
        print("Nome de usuario não aceita números.")

    else:

        print(f"Olá {usuario}")
