# coding: utf-8
from random import randint, random
from collections import Counter

alpha = 3
beta = 3
rho = 0.8
Q = 100

#função objetivo
def func_obj(formiga, mat_dist):
    
    return sum(mat_dist[formiga[i]][formiga[i+1]] for i in range(len(formiga)-1)) + mat_dist[formiga[0]][formiga[-1]]

#função que avalia um caminho para uma cidade de acordo com a distância e a quantidade de feromônio
def fitnessCidade(cidade1, cidade2, mat_dist, mat_fero):

    return mat_fero[cidade1][cidade2]**alpha + (1/(mat_dist[cidade1][cidade2]))**beta

#função que decide qual cidade a formiga irá caminhar e move a formiga
def caminhar(formiga, mat_dist, mat_fero):

    cidades_nao_visitadas = [i for i in range(len(mat_dist)) if i not in formiga]
    total_fero = sum(fitnessCidade(formiga[-1], i, mat_dist, mat_fero) for i in cidades_nao_visitadas)
    probabilidades = {i: fitnessCidade(formiga[-1], i, mat_dist, mat_fero)/total_fero for i in cidades_nao_visitadas}
    
    prob = random()
    acumulado = 0
    
    for cidade, fit in probabilidades.items():
        acumulado += fit
        if acumulado >= prob:
            formiga.append(cidade)
            return

def main():

    #matriz de distâncias
    mat_dist = [
                [0,29,82,46,68,52,72,42,51,55,29,74,23,72,46],
                [29,0,55,46,42,43,43,23,23,31,41,51,11,52,21],
                [82,55,0,68,46,55,23,43,41,29,79,21,64,31,51],
                [46,46,68,0,82,15,72,31,62,42,21,51,51,43,64],
                [68,42,46,82,0,74,23,52,21,46,82,58,46,65,23],
                [52,43,55,15,74,0,61,23,55,31,33,37,51,29,59],
                [72,43,23,72,23,61,0,42,23,31,77,37,51,46,33],
                [42,23,43,31,52,23,42,0,33,15,37,33,33,31,37],
                [51,23,41,62,21,55,23,33,0,29,62,46,29,51,11],
                [55,31,29,42,46,31,31,15,29,0,51,21,41,23,37],
                [29,41,79,21,82,33,77,37,62,51,0,65,42,59,61],
                [74,51,21,51,58,37,37,33,46,21,65,0,61,11,55],
                [23,11,64,51,46,51,51,33,29,41,42,61,0,62,23],
                [72,52,31,43,65,29,46,31,51,23,59,11,62,0,59],
                [46,21,51,64,23,59,33,37,11,37,61,55,23,59,0]
    ]

    #matriz de feromônio
    mat_fero = [[1e-16 for i in mat_dist] for j in mat_dist]

    #população de formigas
    pop = [[i] for i in range(len(mat_dist))]

    contador = Counter()
    distancias = [float("inf") for i in pop]
    
    while True:
        for i in range(len(pop)):
            caminhar(pop[i], mat_dist, mat_fero)
            distancias[i] = func_obj(pop[i], mat_dist)
        melhor = min(distancias)
        contador[melhor] += 1
        print(f'Melhor caminho: {melhor}\tMédia de caminhos: {sum(distancias)/len(pop)}')
        if contador[melhor] >= 10: break

        #Atualização de feromônio
        for i in range(len(mat_dist)):
            for j in range(i, len(mat_dist)):
                soma = 0
                for ind, formiga in enumerate(pop):
                    if i in formiga:
                        if j in formiga:
                            if (s := formiga.index(i)) > 0:
                                if formiga[s-1] == j:
                                    soma += Q/distancias[ind]
                            if s < len(formiga)-1:
                                if formiga[s+1] == j:
                                    soma += Q/distancias[ind]
                mat_fero[i][j] = (1 - rho) * mat_fero[i][j] + soma

if __name__ == "__main__":
    main()
