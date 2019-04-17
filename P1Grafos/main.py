import numpy as np
import os
import matplotlib.pyplot as plt
import networkx as nx
from switchcase import switch
from operator import eq


def switch(value, comp=eq):
    return [lambda match: comp(match, value)]


def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)


def only_ini(intersec, tam, ini):
    i = 0
    while i < tam:
        if intersec[i] == 1 and i != ini:
            return False
        i += 1
    return True


def vec_ver(vect, tam):     # Verifica se todas as posições do vetor auxiliar estão marcadas(=1)
    i = 0
    while i < tam:
        if vect[i] == 0:
            return False
        i += 1
    return True


def ver_sub(vectDir, vectInv, tam, sub):    # Verifica se o subgrafo é fortemente conexo
    i = 0
    while i < tam:
        if sub[i] == 0 and (vectInv[i] != 0 or vectDir[i] != 0):
            return False
        i += 1
    return True


def ver_tran(vect, tam, itemp): # Verifica se vetor transitivo esta totalmente marcado
    i = 0
    while 1 < tam:
        if vect[i] == 0 and i != itemp:
            return False
        i += 1
    return True


def dfs(m, vert_ini, vect, s, tam):
    i = 0
    while i < tam:
        if m[vert_ini, i] == 1 and vect[i] == 0:
            s.append(vert_ini)
            print("[", s[-1], "]", "[", i, "]")
            print()
            vect[vert_ini] = 1
            vert_ini = i
            i = -1
        if i == (tam-1):
            if len(s) != 0:
                print("Voltando de ", vert_ini, " para ", s[-1])
                print()
                vect[vert_ini] = 1
                vert_ini = s.pop()
                i = -1
            elif not s and vec_ver(vect, tam) is False:
                j = 0
                while j < tam:
                    if vect[j] == 0:
                        vert_ini = j
                        print("Indo para: ", vert_ini)
                        print()
                        break
                    j += 1
                i = 0
        if not s and vec_ver(vect, tam):
            print("Todos os vertices foram encontrados!")
            print()
            break
        i += 1


def bfs(m, vert_ini, vect, q, tam):
    q.append(vert_ini)
    vect[vert_ini] = 1
    print("Marcou: ", vert_ini)
    print()
    i = 0
    while i < tam:
        if m[vert_ini, i] == 1 and vect[i] == 0:
            q.append(i)
            vect[i] = 1
            print("Marcou: ", i)
            print()
            i = -1
        if i == (tam-1):
            if len(q) != 0:
                vect[i] = 1
                vert_ini = q.pop(0)
                i = -1
            elif not q and vec_ver(vect, tam) is False:
                j = 0
                while j < tam:
                    if vect[j] == 0:
                        vert_ini = j
                        vect[j] = 1
                        q.append(j)
                        print("Marcou: ", j)
                        print()
                        break
                    j += 1
                i = 0
        if not q and vec_ver(vect, tam):
            print("Todos foram encontrados!")
            print()
            break
        i += 1


def tranDir(m, tam, vect, vert_ini, s, vectDir, write):
    itemp = vert_ini    # itemp salva vertice inicial
    vect[vert_ini] = 0
    i = 0
    nv = 1      # Nível
    s.append(itemp)
    if write == 1:
        print(itemp, " é nível: ", vect[itemp])
        print()
    while i < tam:
        if m[vert_ini, i] == 1 and (vect[i] == 0 and i != itemp):
            vect[i] = nv
            if write == 1:
                print(i, " é nível: ", vect[i])
                print()
            s.append(i);
            i = -1
        if i == 8:
            if len(s) != 0:
                nv = vect[vert_ini] + 1
                vert_ini = s.pop()
                i = -1
            elif not s and ver_tran(vect, tam, itemp) is False:
                j = 0
                while j < tam:
                    if vect[j] == 0 and j != itemp:
                        if write == 1:
                            print(itemp, " não consegue atingir o vértice: ", j)
                            print()
                    j += 1
                break
        if not s and ver_tran(vect, tam, itemp):
            if write == 1:
                print("Todos os níveis foram definidos!")
                print()
            break
        i += 1
    np.copyto(vectDir, vect)
    return vectDir


def tranInv(m, tam, vect, vert_ini, s, vectInv, write):
    itemp = vert_ini
    vect[vert_ini] = 0
    i = 0
    nv = 1
    s.append(itemp)
    if write == 1:
        print(itemp, " é nível: ", vect[itemp])
        print()
    while i < tam:
        if m[i, vert_ini] == 1 and (vect[i] == 0 and i != itemp):
            vect[i] = nv
            if write == 1:
                print(i, " é nível: ", vect[i])
                print()
            s.append(i);
            i = -1
        if i == 8:
            if len(s) != 0:
                nv = vect[vert_ini] + 1
                vert_ini = s.pop()
                i = -1
            elif not s and ver_tran(vect, tam, itemp) is False:
                j = 0
                while j < tam:
                    if vect[j] == 0 and j != itemp:
                        if write == 1:
                            print(j, " não consegue atingir o vertice: ", itemp)
                            print()
                    j += 1
                break
        if not s and ver_tran(vect, tam, itemp):
            if write == 1:
                print("Todos os níveis foram definidos!")
                print()
            break
        i += 1
    np.copyto(vectInv, vect)
    return vectInv


def swcs(op):   # Switch case do menu
    os.system('cls')
    print(m)
    print()
    for case in switch(op):
        if case(1):
            print("DFS: ")
            dfs(m, vert_ini, vect, s, tam)
            print()
            return 0
        if case(2):
            print("BFS: ")
            print()
            bfs(m, vert_ini, vect, q, tam)
            return 0
        if case(3):
            print("Fecho Transitivo Direto: ")
            print()
            direct = tranDir(m, tam, vect, vert_ini, s, vectDir, 1)
            return direct
        if case(4):
            print("Fecho Transitivo Inverso: ")
            print()
            inv = tranInv(m, tam, vect, vert_ini, s, vectInv, 1)
            return inv
        if case(5):
            while True:
                ini = int(input('Selecione o vértice inicial(0 a {}): '.format((tam - 1))))
                print()
                if ini > (tam - 1):
                    print("Valor inválido!")
                else:
                    break
            return ini
        if case(6):
            connect(tam, vectDir, vectInv, vert_ini, vect);
            return 0
        if case(7):
            print("FECHE A JANELA ANTES DE CONTINUAR!")
            print()
            drawGraph(tam, m)
            return 0
        if case(8):
            return 1
    else:
        print("O valor selecionado é INVÁLIDO. Por favor selecione um número presente na lista! ")
        print()
        return 0


def drawGraph(tam, m):      # Desenha conexões do grafo
    graph = nx.DiGraph()
    for i in range(tam):
        for j in range(tam):
            if m[i][j] == 1:
                graph.add_edge(i, j)

    plt.draw()

    nx.draw_networkx(graph, with_labels=True, font_weight='bold')
    plt.title('Grafo Orientado')

    # Config fullscreen para TkAgg manager
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())

    plt.show()
    plt.interactive(False)

    os.system('cls')


def connect(tam, vectDir, vectInv, vert_ini, vect):   # Verifica se o grafo é conexo e identifica os subgrafos
    intersec = np.zeros((tam, 1))       # Vetor de intersecção entre transitivo direto e inverso
    sub = np.zeros((tam, 1))        # Vetor de subgrafos

    intersec[vert_ini] = 1

    i = 0
    while i < tam:
        if vectDir[i] != 0 and i != vert_ini and vectInv[i] != 0:
            intersec[i] = 1
        i += 1
    if vec_ver(intersec, tam):
        print("O grafo é conexo!")
        print()
    else:
        print("O grafo não é conexo!")
        print()

        if only_ini(intersec, tam, vert_ini):
            print("Subgrafo:")
            print()
            print(vert_ini)
            print()

        j = 0
        while j < tam:
            if intersec[j] == 0 and sub[j] == 0:
                np.copyto(vectDir, tranDir(m, tam, vect, j, s, vectDir, 0))
                vect = np.zeros((tam, 1)).astype('int64')  # Zera vect
                np.copyto(vectInv, tranInv(m, tam, vect, j, s, vectInv, 0))
                vect = np.zeros((tam, 1)).astype('int64')  # Zera vect

                print("Subgrafo:")
                print()
                print(j)
                i = 0
                while i < tam:
                    if vectDir[i] != 0 and i != j and sub[i] != 1 and vectInv[i] != 0:
                        sub[i] = 1
                        print(i)
                    i += 1
                if ver_sub(vectDir, vectInv, tam, sub):
                    print("É fortemente conexo!")
                    print()
                print()
            j += 1
        print("Todos os subgrafos foram encontrados")
        print()


while True:
    tam = int(input("Insira o tamanho da matriz: "))
    print()
    if tam <= 0:
        print("Valor inválido! Deve ser maior que 0")
    else:
        break

m = np.zeros(shape=(tam, tam))  # Cria matriz quadrática de zeros com o tamanho especificado
os.system('cls')


'''print("ADICIONE OS VÉRTICES: ")
print()

end = 1
while end != 0:
    while True:
        x = int(input('Linha(0 a {}): '.format((tam-1)) ))
        print()
        if x > (tam-1) or x < 0:
            print("Valor inválido!")
        else:
            break
    while True:
        y = int(input('Coluna(0 a {}): '.format((tam-1)) ))
        print()
        if y > (tam-1) or y < 0:
            print("Valor inválido!")
        else:
            break
    
    m[x][y] = 1
    
    while True:
        end = int(input("Deseja adicionar mais algum vértice (Sim[1]/Não[0]): "))
        print()
        if end < 0 or end > 1:
            print("Valor inválido! Deve ser 0 ou 1")
        else:
            break
    os.system('cls')'''


os.system('cls')
'''m = np.array([[1,1,1],[0,0,0],[0,1,0]]).astype(int)'''
m = np.array([[0,1,1,0,0,0,0,0], [0,0,1,1,0,0,0,0], [0,0,0,0,0,1,1,1], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0]]).astype(int)
print(m)
print()

'''m = np.array([[0,0,0,0,1,1,1,0,1],[0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1,0],
              [1,0,0,0,0,1,0,0,1],[1,0,0,0,1,0,0,0,1], [1,1,0,0,0,0,0,0,0], [0,0,1,1,0,0,0,0,0], [1,0,0,0,1,1,0,0,0]]).astype(int)
m = np.array([[0,1,0,0,0,0], [1,0,0,0,0,0], [0,0,0,1,0,0], [0,0,1,0,0,0], [0,0,0,0,0,1], [0,0,0,0,1,0]]).astype(int)

print(m)
print()'''

vect = np.zeros((tam, 1)).astype('int64')   # Vetor auxiliar
vectInv = np.zeros((tam, 1)).astype('int64')    # Vetor transitivo inverso
vectDir = np.zeros((tam, 1)).astype('int64')    # Vetor transitivo direto
s = []      # Pilha
q = []      # Fila

while True:
    vert_ini = int(input('Selecione o vértice inicial(0 a {}): '.format((tam-1))))
    print()
    if vert_ini > (tam-1):
        print("Valor inválido!")
    else:
        break

os.system('cls')

end = 0

while end != 1:
    print("GRAFOS:")
    print()
    print("1 - DFS")
    print("2 - BFS")
    print("3 - TRANSITIVO DIRETO")
    print("4 - TRANSITIVO INVERSO")
    print("5 - Reselecionar o vértice inicial")
    print("6 - Conectividade e Subgrafos")
    print("7 - Visualizar conexões do Grafo")
    print("8 - EXIT")
    print()
    print()
    op = int(input("Selecione uma opção: "))

    if op == 3:
        np.copyto(vectDir, swcs(op))        # Copia vetor resultante do transitivo direto para vectDir
    elif op == 4:
        np.copyto(vectInv, swcs(op))        # Copia vetor resultante do transitivo inverso para vectInv
    elif op == 5:
        vert_ini = swcs(op)
    else:
        end = swcs(op)

    print()
    input("Press <ENTER> to continue...")
    flush_input()

    vect = np.zeros((tam, 1)).astype('int64')  # Zera vetor auxiliar

    os.system('cls')
