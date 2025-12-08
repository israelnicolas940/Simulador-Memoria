def Init(tam_vetor):
    Comandos = [tam_vetor]
    return Comandos

def Choose_block():
    pass

def Alloc(tam_aloc, tipo_alg, vetor_memo):

    if(tipo_alg == "best"):
        # Implementar best
        pass
    elif(tipo_alg == "worst"):
        # Implementar worst
        pass
    elif(tipo_alg == "first"):
        # Implementar fist
        pass
    else:
        print("algoritmo não reconhecido")

def Freeid(Id_bloco, vetor_memo):
    pass

def Show():
    # Integrar com frontend
    pass

def Stats(vetor_memo):
    ocp, liv, brcs = 0
    for i in range(vetor_memo):
        if(vetor_memo[i] == 0):
            liv =+ 1
        else:
            ocp =+ 1
    uso = (ocp * 100)/liv
    print("Tamanho total: ", len(vetor_memo), "bytes")
    print("Ocupado: ", ocp, " bytes | Livre", liv, "bytes")
    # Calcular fragmentação externa
    # Calcular fragmentação interna ( é possível? )
    print("Uso efetivo: {uso:.2f}%")
