# coding: utf-8

import math, pygame, random, pprint
from math import *
from pygame import *


# declaração da classe

class Nodo(object):
    def __init__(self, coord, pai):
        self.coord = coord
        self.pai = pai


# definição dos parâmetros

tamPlano = [800, 600]
distMax = 15.0      # entre um ponto e outro da árvore
raio = 17           # região para qual é considerado atingido o ponto de chegada
maxNodos = 5000     # número máximo de vértices da árvore


# declaração de variáveis globais

obstac = []
nodos = [Nodo(None, None)]
x = 0
y = 1 # índices dos vetores

pontoChegada = Nodo((30, 230), None)
pontoSaida = Nodo((375, 375), None)


# casos de teste

testaParede = False
funcaoIntersec = True


def dist(Nodo, P):
    '''
    Recebe dois pontos e retorna a distância entre eles
    '''
    global x, y
    distancia = sqrt((Nodo[x]-P[x])**2 + (Nodo[y]-P[y])**2)
    return distancia


def intersecciona_obstaculo(Nodo, P):
    '''
    Verifica se a aresta que liga o nodo da árvore e um novo ponto aleatório
    não faz intersecção com algum obstáculo
    '''
    global obstac
    global x, y

    teta = atan((Nodo[y]-P[y])/(Nodo[x]-P[x]))  # tangente do ângulo
    
    for k in obstac:
        
        if ((Nodo[x] <= k.right) and (P[x] >= k.left)):  # se o objeto estiver entre as coordenadas x dos dois pontos
            alt1 = tan(teta)*(k.left-Nodo[x])   # define as alturas das retas nas coordenadas x do obstáculo
            alt2 = tan(teta)*(k.right-Nodo[x])
            alt1 = Nodo[y]-alt1
            alt2 = Nodo[y]-alt2
            if (alt1 >= k.top and alt1 <= k.bottom) or (alt2 >= k.top and alt2 <= k.bottom):    # se estiver no intervalo de intersecção, o ponto é inválido
                return True

        elif ((Nodo[x] >= k.left) and (P[x] <= k.right)): # mesma coisa, mas pro caso do nodo estar mais à direita
            alt1 = tan(teta)*(k.left-P[x])
            alt2 = tan(teta)*(k.right-P[x])
            alt1 = P[y]-alt1
            alt2 = P[y]-alt2
            if (alt1 >= k.top and alt1 <= k.bottom) or (alt2 >= k.top and alt2 <= k.bottom):
                return True
    
    return False


def posiciona_novo_P(Nodo, P):
    '''
    Se o ponto P estiver numa distância maior que distMax do nó mais próximo,
    retorna projeção de um novo ponto na reta Nodo-P a uma distância distMax de Nodo
    '''
    global x, y
    global distMax
    
    if dist (Nodo, P) < distMax:
        return P
    
    else:
        teta = atan2((P[y]-Nodo[y]), (P[x]-Nodo[x]))     # atan2 recebe y e x e retorna o ângulo de inclinação da reta que os liga
        P = Nodo[x] + distMax*cos(teta), Nodo[y] + distMax*sin(teta) # novo ponto projetado sobre a mesma reta
        return P


def posicao_valida(P):
    '''
    Confere se o ponto foi gerado numa posição válida (não está sobre
    a região de um obstáculo)
    '''
    for k in obstac:
        if k.collidepoint(P) == True:
            return False

    return True


def posiciona_obstaculos(parede):
    '''
    Define os obstáculos e os desenha na tela.
    Sobre o objeto Rect: recebe duas tuplas (A,B),(C,D) onde representam:
    A,B - posição do retângulo em X,Y
    C,D - dimensões X e Y do retângulo
    '''
    global obstac
    global x, y

    if (parede == True):    # coloca um obstáculo que divide a tela no meio
        obstac.append(pygame.Rect((tamPlano[x]/2.0, 0),(3*distMax/4.0, tamPlano[y])))

    else:                   # vetor de obstáculos a serem desenhados na tela
        '''
        obstac.append(pygame.Rect((100,100),(30,330)))
        obstac.append(pygame.Rect((500,500),(150, 50)))
        '''
        obstac.append(pygame.Rect((300,100),(20,400)))
        obstac.append(pygame.Rect((300,100),(300,20)))
        obstac.append(pygame.Rect((300,500),(300,20)))
        obstac.append(pygame.Rect((600,100),(20,300)))
        obstac.append(pygame.Rect((600,500),(150,20)))
        obstac.append(pygame.Rect((450,300),(20,200)))
    
    for k in obstac:
        pygame.draw.rect(plano, [50,50,50], k)
        


def gera_RRT():
    '''
    Gera uma árvore aleatória de no máximo maxNodos vértices.
    Interrompe execução quando encontra o ponto de destino.
    '''

    global nodos, maxNodos
    global raio, pontoChegada
    global x, y
                      
    i = 0

    while i < maxNodos:
    
        i = i + 1
        ok = False
                      
        while ok == False:
            novoP = random.random()*tamPlano[x], random.random()*tamPlano[y]
            # random() retorna um valor entre 0.0 e 1.0, multiplicados pelas dimensões do plano geram um novo ponto

            pai = nodos[0]
       
            for k in nodos:     # percorre todos pontos da árvore para encontrar o mais próximo e define como pai
                if dist(k.coord, novoP) < dist(pai.coord, novoP):
                    pai = k                    

            P = posiciona_novo_P(pai.coord, novoP)      # define o ponto numa distâncima máxima distMax do pai

            if (funcaoIntersec == True):
                ok = (posicao_valida(P) and not(intersecciona_obstaculo(pai.coord, P)))   # confere se o novo nodo ou aresta não ficou em cima de um obstáculo
            else:
                ok = posicao_valida(P)


        nodos.append(Nodo(P, pai))      # adiciona na lista de nodos da árvore
        pygame.draw.line(plano, [255, 0, 0], pai.coord, P, 1)       # desenha aresta que conecta os dois
              
        pygame.display.update()
        clock.tick(10000)

        if dist(pontoChegada.coord, P) <= raio:     # se estiver dentro do raio de "aceitação", interrompe execução
            return True

    return False




# main():

pygame.init()
clock = pygame.time.Clock()
pygame.event.set_allowed(None)

plano = pygame.display.set_mode(tamPlano)
plano.fill((235, 230, 220))

posiciona_obstaculos(testaParede)

print("Ponto de saida:")
print(pontoSaida.coord)
print("Ponto de destino:")
print(pontoChegada.coord)


pygame.draw.circle(plano, (254, 121, 209), pontoSaida.coord, raio, 0)       # coloca o ponto da saída na tela, em rosa
pygame.draw.circle(plano, (0, 255, 0), pontoChegada.coord, raio, 0)         # ponto de chegada em azul

pygame.display.update()
clock.tick(10000)
    
nodos[0] = pontoSaida    # "raiz" da árvore

print("Gerando RRT...")
encontrou = gera_RRT()   # encontrou indica se a árvore chegou a pontoSaida

ponto = nodos[len(nodos)-1] # ultimo ponto do vetor é aquele que chegou a pontoSaida
percorridos = []

print("Verificando existencia de caminho...")

if encontrou == True:
    print("Caminho encontrado. :)")
    print("Construindo caminho. Pontos percorridos:")

    while ponto.pai != None:    # enquanto não chegar à raiz
        pygame.draw.line(plano, [51, 153, 255], ponto.pai.coord, ponto.coord, 3) # desenha linha do ponto até seu pai
        percorridos.append(ponto.coord)
        ponto = ponto.pai
        
        pygame.display.update()
        clock.tick(30000)

    percorridos.reverse()
    pprint.pprint(percorridos)  # lista os pontos percorridos para montar o caminho

else:
    print("Caminho nao encontrado :(")

print("Fim de execucao")

pygame.time.wait(10000)        
pygame.display.quit()
pygame.quit()
