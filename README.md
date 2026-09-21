# Busca em Largura (BFS)

Demonstração da BFS no labirinto disponibilizado em sala, com visualização
gráfica e execução no terminal. Cada posição livre é um estado; os movimentos
permitidos são cima, baixo, esquerda e direita, sem atravessar paredes.

## Executar

Na pasta do projeto, instale o pygame se necessário e abra a visualização:

```bash
python -m pip install pygame
python maze.py
```

**Controles:** `R` reinicia; `+` / `-` ajustam a velocidade; `ESC` sai.

Para executar o mesmo labirinto no terminal, sem pygame:

```bash
python busca.py
```

## Arquivos

| Arquivo | Função |
|---|---|
| [`estrutura_labirinto.py`](estrutura_labirinto.py) | Mapa, início, objetivo e vizinhos permitidos. |
| [`busca.py`](busca.py) | BFS, registro dos pais e reconstrução do caminho. |
| [`maze.py`](maze.py) | Animação da busca, legenda e controles. |

## Como funciona

A BFS usa uma **fila FIFO**: o primeiro estado que entra é o primeiro a sair.
Assim, explora por camadas: início, posições a 1 movimento, a 2 e assim por
diante. Se existisse um caminho mais curto até a saída, ela seria alcançada
numa camada anterior. Por isso, a BFS encontra o menor número de movimentos.

Neste labirinto, cada movimento custa 1: menos movimentos também significa
menor custo. Com custos diferentes, a BFS não garante o menor custo total.

**Aplicação:** planejar a rota de um robô em uma grade com obstáculos e
movimentos de mesmo custo.

**Vantagem:** garante um caminho com o menor número de movimentos.
**Limitação:** pode consumir muita memória ao guardar as células descobertas.

## Resultado do mapa atual

A busca examina **161 células** e encontra um caminho de **32 movimentos**,
passando por **33 células**, incluindo o início. Células examinadas incluem
alternativas que não fazem parte da solução; movimentos são os deslocamentos
do caminho final, calculados por `len(caminho) - 1`.


