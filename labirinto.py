# Importa bibliotecas necessárias
import random                         # Usada para geração de números aleatórios
from collections import deque         # Estrutura de dados eficiente para filas (usada no BFS)

# --- Constantes ---
TAMANHO = 10                          # Tamanho da matriz do labirinto (10x10)
NUM_OBSTACULOS = random.randint(15, 35)  # Quantidade aleatória de obstáculos
NUM_RECARGA_5 = 5                     # Número de pontos de recarga de +5 de energia
NUM_RECARGA_10 = 3                    # Número de pontos de recarga de +10 de energia
ENERGIA_INICIAL = 50                 # Energia inicial do robô

# Movimentos permitidos: cima, baixo, esquerda e direita
MOVIMENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# --- Função para gerar o labirinto ---
def gerar_labirinto():
    # Cria matriz 10x10 preenchida com espaços vazios
    labirinto = [[' ' for _ in range(TAMANHO)] for _ in range(TAMANHO)]

    # Posiciona os obstáculos aleatoriamente
    contador = 0
    while contador < NUM_OBSTACULOS:
        i = random.randint(0, TAMANHO - 1)
        j = random.randint(0, TAMANHO - 1)
        # Garante que início (0,0) e fim (9,9) estejam livres
        if (i, j) not in [(0, 0), (TAMANHO - 1, TAMANHO - 1)] and labirinto[i][j] == ' ':
            labirinto[i][j] = 'O'  # Marca como obstáculo
            contador += 1

    # Posiciona os pontos de energia +5
    contador = 0
    while contador < NUM_RECARGA_5:
        i = random.randint(0, TAMANHO - 1)
        j = random.randint(0, TAMANHO - 1)
        if labirinto[i][j] == ' ':
            labirinto[i][j] = 'E5'
            contador += 1

    # Posiciona os pontos de energia +10
    contador = 0
    while contador < NUM_RECARGA_10:
        i = random.randint(0, TAMANHO - 1)
        j = random.randint(0, TAMANHO - 1)
        if labirinto[i][j] == ' ':
            labirinto[i][j] = 'E10'
            contador += 1

    # Define ponto de partida (S) e ponto de chegada (F)
    labirinto[0][0] = 'S'
    labirinto[TAMANHO - 1][TAMANHO - 1] = 'F'

    return labirinto

# --- Função para imprimir o labirinto no terminal ---
def imprimir_labirinto(labirinto):
    print("Labirinto:")
    for linha in labirinto:
        print(' '.join([f"{celula:^4}" for celula in linha]))  # Formatação com 4 caracteres centralizados

# --- Função que executa o algoritmo BFS com energia ---
def bfs_com_energia(labirinto):
    inicio = (0, 0)  # Posição inicial
    fila = deque()   # Fila que guarda os estados a explorar
    fila.append((inicio, [inicio], ENERGIA_INICIAL))  # Estado inicial: posição, caminho percorrido, energia

    visitados = set()  # Guarda combinações de (posição, energia)
    visitados.add((inicio, ENERGIA_INICIAL))

    # Loop da busca
    while fila:
        pos, caminho, energia = fila.popleft()  # Extrai o primeiro elemento da fila
        i, j = pos

        # Verifica se chegou ao destino
        if labirinto[i][j] == 'F':
            return caminho, energia  # Retorna o caminho e energia restante

        # Explora os vizinhos
        for move in MOVIMENTOS:
            ni, nj = i + move[0], j + move[1]

            # Verifica se a posição é válida
            if 0 <= ni < TAMANHO and 0 <= nj < TAMANHO:
                tipo = labirinto[ni][nj]

                if tipo == 'O':
                    continue  # Se for obstáculo, ignora

                nova_energia = energia - 1  # Consome 1 de energia

                # Se encontrar ponto de energia, adiciona
                if tipo == 'E5':
                    nova_energia += 5
                elif tipo == 'E10':
                    nova_energia += 10

                if nova_energia <= 0:
                    continue  # Energia insuficiente, não prossegue

                nova_pos = (ni, nj)

                # Evita revisitar o mesmo estado com energia igual
                if (nova_pos, nova_energia) not in visitados:
                    visitados.add((nova_pos, nova_energia))
                    fila.append((nova_pos, caminho + [nova_pos], nova_energia))

    return None, 0  # Se nenhum caminho for encontrado

# --- Execução do programa principal ---
labirinto = gerar_labirinto()         # Gera o labirinto
imprimir_labirinto(labirinto)         # Mostra o labirinto

caminho, energia_final = bfs_com_energia(labirinto)  # Executa o algoritmo

# --- Função para marcar o caminho no labirinto com '*' ---
def marcar_caminho(labirinto, caminho):
    labirinto_visual = [linha[:] for linha in labirinto]  # Cria uma cópia do labirinto
    for (i, j) in caminho:
        if labirinto_visual[i][j] not in ('S', 'F'):
            labirinto_visual[i][j] = '*'  # Marca o caminho com '*'
    return labirinto_visual

# --- Impressão do resultado ---
if caminho:
    print(f"\n✅ Caminho encontrado com {len(caminho)} passos e energia final = {energia_final}")
    print("Caminho:", caminho)
    labirinto_com_caminho = marcar_caminho(labirinto, caminho)
    print("\nLabirinto com o caminho percorrido:")
    imprimir_labirinto(labirinto_com_caminho)
else:
    print("\n❌ Nenhum caminho encontrado com a energia disponível.")
