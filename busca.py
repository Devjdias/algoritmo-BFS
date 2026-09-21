# -*- coding: utf-8 -*-
"""Busca em Largura (BFS), com histórico para visualização e execução no terminal."""

from collections import deque


def novo_estado():
    """Inicializa os registros da busca."""
    return {
        "visitados": set(),   # células já examinadas
        "fronteira": set(),   # células que aguardam na fila
        "pai": {},            # célula anterior no caminho
        "atual": None,        # célula examinada nesta etapa
        "passos": 0,          # células examinadas, não movimentos da solução
        "encontrado": False,
        "falhou": False,
        "caminho": [],        # solução do início ao objetivo
    }


def _copia_do_estado(estado):
    """Copia os dados para a animação, preservando as etapas anteriores."""
    return {
        "visitados": set(estado["visitados"]),
        "fronteira": set(estado["fronteira"]),
        "atual": estado["atual"],
        "passos": estado["passos"],
        "encontrado": estado["encontrado"],
        "falhou": estado["falhou"],
        "caminho": list(estado["caminho"]),
    }


def _reconstruir_caminho(pai, objetivo):
    # Seguimos os pais da saída até o início e invertemos a lista.
    # Movimentos = len(caminho) - 1, pois a lista também inclui o início.
    caminho = []
    celula = objetivo
    while celula is not None:
        caminho.append(celula)
        celula = pai.get(celula)
    caminho.reverse()
    return caminho


def _expandir(estado, celula, objetivo, vizinhos, fronteira):
    """Testa o objetivo e, se ainda não chegou, enfileira os vizinhos novos."""
    estado["fronteira"].discard(celula)
    estado["visitados"].add(celula)
    estado["atual"] = celula
    estado["passos"] += 1

    if celula == objetivo:
        estado["encontrado"] = True
        estado["caminho"] = _reconstruir_caminho(estado["pai"], objetivo)
        return

    for viz in vizinhos(celula):
        # Não repetimos células já examinadas ou que estão na fila.
        # Isso evita repetições e ciclos.
        if viz in estado["visitados"] or viz in estado["fronteira"]:
            continue
        # O pai registra de onde viemos; append põe o vizinho no fim.
        estado["pai"][viz] = celula
        estado["fronteira"].add(viz)
        fronteira.append(viz)


def busca(inicio, objetivo, vizinhos):
    """Executa a BFS e devolve o histórico de estados na ordem da busca."""
    estado = novo_estado()
    # Começamos pelo início, que não tem pai.
    estado["fronteira"].add(inicio)
    estado["pai"][inicio] = None
    historico = []

    # A fila FIFO explora por camadas: 0, 1, 2... movimentos.
    # popleft retira do começo; append adiciona ao fim.
    # A deque define a ordem; o conjunto estado["fronteira"] evita repetições.
    fronteira = deque([inicio])
    while fronteira:
        celula = fronteira.popleft()
        _expandir(estado, celula, objetivo, vizinhos, fronteira)
        historico.append(_copia_do_estado(estado))
        if estado["encontrado"]:
            return historico

    estado["falhou"] = True
    # Fila vazia sem encontrar o objetivo: não existe caminho até ele.
    historico.append(_copia_do_estado(estado))
    return historico


if __name__ == "__main__":
    from estrutura_labirinto import MAPA, INICIO, OBJETIVO, vizinhos

    print("Labirinto da apresentação (W=parede, E=objetivo):")
    for linha in MAPA:
        print(" ", linha)
    print(f"Início: {INICIO} | Objetivo: {OBJETIVO}")
    print()

    historico = busca(INICIO, OBJETIVO, vizinhos)
    for estado in historico:
        print(f"Examinadas: {estado['passos']:3d}  atual={estado['atual']}  "
              f"fronteira={len(estado['fronteira']):2d}")

    print()
    estado_final = historico[-1]
    if estado_final["encontrado"]:
        movimentos = len(estado_final["caminho"]) - 1
        print(f"Objetivo encontrado após examinar {estado_final['passos']} células.")
        print(f"Caminho mínimo: {movimentos} movimentos "
              f"({len(estado_final['caminho'])} células, incluindo o início).")
    else:
        print("Não achou o objetivo.")
