print("Digite aqui os comandos para manipular a memória")
while True:
    entrada = input("").split()
    if not entrada:
        break # Se o usuário mandar uma linha vazia, o programa para de ler as entradas
    if(str(entrada[0]) == "init"):
        print(int(entrada[1]))
    elif(str(entrada[0]) == "alloc"):
        print(int(entrada[1]), str(entrada[2]))
    elif(str(entrada[0]) == "freeid"):
        print(int(entrada[1]))
    elif(str(entrada[0]) == "show"):
        print(str(entrada[0]))
    elif(str(entrada[0]) == "stats"):
        print(str(entrada[0]))
    else:
        print("Comando inválido.")
