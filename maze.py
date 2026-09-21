# -*- coding: utf-8 -*-
"""
Visualização da BFS com pygame. Legenda e controles aparecem na janela.

adaptado de https://www.pygame.org/project-Rect+Collision+Response-1061-.html
"""

import sys
import pygame

from estrutura_labirinto import CELL, LARGURA, ALTURA, INICIO, OBJETIVO, PAREDES, vizinhos
from busca import busca

# Configuração visual

SCALE = 2  # ampliação do desenho
DCELL = CELL * SCALE
PANEL_H = 115  # faixa inferior com status, legenda em até duas linhas e controles

COR_FUNDO      = (18, 18, 18)
COR_GRADE      = (55, 55, 55)
COR_PAREDE     = (230, 230, 230)
COR_VISITADO   = (55, 90, 170)
COR_FRONTEIRA  = (240, 200, 40)
COR_ATUAL      = (255, 120, 0)
COR_CAMINHO    = (60, 200, 100)
COR_INICIO     = (0, 170, 255)
COR_FIM        = (230, 50, 60)
COR_PAINEL     = (10, 10, 10)
COR_TEXTO      = (230, 230, 230)


historico = []  # lista de dicionários devolvida por busca.py: um item por etapa
indice = 0      # em qual item do histórico estamos agora


def reset():
    """Roda a BFS de novo do zero e volta ao primeiro quadro da animação."""
    global historico, indice
    # A BFS calcula a busca; o pygame anima o histórico.
    # Mostre a legenda e diferencie células examinadas de movimentos do caminho.
    historico = busca(INICIO, OBJETIVO, vizinhos)
    indice = 0


def avancar():
    """Avança um passo na animação, mostrando o próximo item do histórico."""
    global indice
    if indice < len(historico) - 1:
        indice += 1


# Desenho na tela

def cell_rect(coord):
    cx, cy = coord
    return pygame.Rect(cx * SCALE, cy * SCALE, DCELL, DCELL)


def desenhar_legenda(screen, fonte, x0, y0):
    itens = [
        (COR_INICIO, "Início"),
        (COR_FIM, "Objetivo"),
        (COR_PAREDE, "Parede"),
        (COR_VISITADO, "Visitado"),
        (COR_FRONTEIRA, "Fronteira"),
        (COR_ATUAL, "Atual"),
        (COR_CAMINHO, "Caminho"),
    ]
    x = x0
    for cor, nome in itens:
        img = fonte.render(nome, True, COR_TEXTO)
        if x + 18 + img.get_width() > screen.get_width() - 8:
            x = x0
            y0 += 22
        pygame.draw.rect(screen, cor, (x, y0, 14, 14))
        pygame.draw.rect(screen, (0, 0, 0), (x, y0, 14, 14), 1)
        screen.blit(img, (x + 18, y0 - 2))
        x += 18 + img.get_width() + 18


def desenhar(screen, fonte, fps):
    screen.fill(COR_FUNDO)

    estado = historico[indice]
    visitados = estado["visitados"]
    fronteira = estado["fronteira"]
    atual = estado["atual"]
    caminho = estado["caminho"]
    encontrado = estado["encontrado"]
    falhou = estado["falhou"]
    passos = estado["passos"]

    for c in visitados:
        pygame.draw.rect(screen, COR_VISITADO, cell_rect(c))
    for c in fronteira:
        pygame.draw.rect(screen, COR_FRONTEIRA, cell_rect(c))
    if encontrado:
        for c in caminho:
            pygame.draw.rect(screen, COR_CAMINHO, cell_rect(c))
    if atual is not None and not encontrado:
        pygame.draw.rect(screen, COR_ATUAL, cell_rect(atual))
    pygame.draw.rect(screen, COR_INICIO, cell_rect(INICIO))
    pygame.draw.rect(screen, COR_FIM, cell_rect(OBJETIVO))

    for w in PAREDES:
        pygame.draw.rect(screen, COR_PAREDE, cell_rect(w))

    # Grade sobre as células coloridas.
    for gx in range(LARGURA + 1):
        pygame.draw.line(screen, COR_GRADE, (gx * DCELL, 0), (gx * DCELL, ALTURA * DCELL))
    for gy in range(ALTURA + 1):
        pygame.draw.line(screen, COR_GRADE, (0, gy * DCELL), (LARGURA * DCELL, gy * DCELL))

    # painel inferior: status, legenda e controles
    py = ALTURA * DCELL
    pygame.draw.rect(screen, COR_PAINEL, (0, py, LARGURA * DCELL, PANEL_H))

    if falhou:
        status = "Sem caminho até o objetivo!"
    elif encontrado:
        status = f"Caminho mínimo: {len(caminho) - 1} movimentos ({len(caminho)} células)."
    else:
        status = "Buscando..."

    linha1 = f"BFS | {status}"
    linha2 = f"Examinadas: {passos}   Fronteira: {len(fronteira)}   Velocidade: {fps}/s"
    linha3 = "R reinicia   |   +/- velocidade   |   ESC sai"

    screen.blit(fonte.render(linha1, True, COR_TEXTO), (8, py + 4))
    screen.blit(fonte.render(linha2, True, COR_TEXTO), (8, py + 22))
    desenhar_legenda(screen, fonte, 8, py + 44)
    screen.blit(fonte.render(linha3, True, (150, 150, 150)), (8, py + 90))

    pygame.display.flip()


# Loop principal

def main():
    pygame.init()
    pygame.display.set_caption("Busca em Largura (BFS) no labirinto")
    screen = pygame.display.set_mode((LARGURA * DCELL, ALTURA * DCELL + PANEL_H))
    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont("couriernew,dejavusansmono,consolas,monospace", 16)

    fps = 12
    reset()

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    running = False
                elif e.key == pygame.K_r:
                    reset()
                elif e.key in (pygame.K_EQUALS, pygame.K_KP_PLUS):
                    fps = min(fps + 4, 120)
                elif e.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                    fps = max(fps - 4, 1)

        desenhar(screen, fonte, fps)
        clock.tick(fps)
        avancar()

    pygame.quit()
    sys.exit()


# CONCLUSÃO:
# Pergunta: Por que a BFS encontra o caminho com menos passos neste labirinto?
# Resposta: A fila FIFO explora por camadas. Um caminho mais curto teria sido
# encontrado antes. Com custo 1 por movimento, menos passos também é menor custo.

if __name__ == "__main__":
    main()
