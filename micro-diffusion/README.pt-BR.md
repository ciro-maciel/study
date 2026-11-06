# Micro Diffusion: o texto que aparece todo de uma vez

[English](README.md)

Um GPT escreve uma letra depois da outra, da esquerda para a direita. Um modelo de difusão faz de outro jeito: começa de uma palavra com todas as letras apagadas e preenche as lacunas aos poucos, primeiro as de que tem mais certeza, até não sobrar nenhuma apagada. Os geradores de imagem funcionam assim; já existem modelos de texto que escrevem assim também. Este arquivo mostra a ideia inteira com nomes próprios, em cerca de 350 linhas de Python e NumPy, treinando em segundos.

- **Autor:** Siwoo4985
- **Original:** <https://github.com/Siwoo4985/Micro-Diffusion> (MIT)
- **Copiado do commit:** `00535e70f8328bfb445ecc88d96f738ece76961c`, em 6 de novembro de 2026, sem alterações: `train_pure.py` e `names.txt`
- **sha256:** `train_pure.py` `ea89c17b1f99199ad7b10047f77980b02a94c4883766ea43ddadce872c45cc04`

## Rodar

Precisa do NumPy (o microgpt não precisa de nada; este faz as contas em matrizes inteiras de uma vez):

```bash
python3 -m pip install numpy
python3 train_pure.py --seed 42
```

O que vimos num Mac (Apple M4 Pro, Python 3.15.2, NumPy 2.5.4) em 6 de novembro de 2026. Com `--seed 42` a saída se repetiu igual numa segunda rodada.

| | |
| --- | --- |
| Nomes | 31.979 (até 12 letras) |
| Parâmetros | 238.672 |
| Treino | 5.000 passos de 64 nomes, em 5 segundos |
| Alguns nomes inventados | `honcea`, `avilya`, `nokan`, `lymane`, `kaihan`, `jaholyn`, `salma`, `marce` |

## Apagar, depois preencher

Primeiro ele mostra o **processo de ida**, o lado fácil: pega um nome de verdade e apaga mais letras a cada passo `t`, seguindo um cronograma que termina com tudo apagado (`_` é uma letra apagada):

```
Forward Process: "matison"
  t=  0 (mask   0.0%): matison
  t=  5 (mask   4.2%): _atison
  t= 10 (mask  15.3%): matis_n
  t= 20 (mask  50.6%): _at_s_n
  t= 30 (mask  85.6%): _______
  t= 40 (mask 100.0%): _______
```

O **treino** é esse mesmo apagar, milhares de vezes: escolhe nomes, escolhe um `t` entre 1 e 40, apaga essa parte das letras e pede ao modelo que adivinhe cada letra original. O erro cai conforme ele aprende:

```
  step |     loss |   t |  mask%
     0 |   3.3550 |   8 |  10.1%
  2500 |   0.0697 |   4 |   2.8%
  4999 |   0.9560 |  24 |  65.9%
```

O erro pula porque o `t` muda a cada passo: com 3% apagado a resposta está quase dada, com 66% apagado é difícil. Compare linhas com `t` parecido, não vizinhas.

**Gerar** vai no sentido contrário. Começa com 12 letras apagadas, pede ao modelo um palpite para cada lacuna, fica com os palpites de que ele tem mais certeza e apaga o resto de novo; repete 40 vezes. Quatro nomes nascendo:

```
  t= 40 (  0.0%): ___________ | ___________ | ___________ | ___________
  t= 30 ( 25.0%): _y | _oncea | avi_ya | no_an
  t= 20 ( 50.0%): ty | honcea | avilya | nokan
```

`honcea` teve o meio antes da primeira letra. Essa é a diferença para um GPT, que nunca poderia decidir o fim de uma palavra antes do começo.

## O que tem dentro, na ordem do arquivo

| Parte | O que faz |
| --- | --- |
| **Configuração** | No máximo 12 letras, 256 neurônios por camada, 40 níveis de ruído (`T`), 5.000 passos, 64 nomes por passo |
| **Tokenizador** | Um número por letra, mais `PAD` (o nome acabou) e `MASK` (apagada) |
| **Cronograma de ruído** (`cosine_mask_rate`, `add_noise`) | Quanto apagar em cada `t`: pouco no começo, tudo no fim |
| **Removedor de ruído** (`forward`) | Uma MLP, três camadas com uma conexão de atalho, que vê o nome inteiro de uma vez (cada letra como 28 zeros e um um) mais o `t`, e adivinha as 12 letras |
| **Treino** (`train_step`) | Apaga, adivinha, mede o erro, e o caminho de volta escrito à mão: aqui não há autograd, cada derivada está escrita |
| **Geração** (`sample`) | De tudo apagado a um nome em 40 passos, revelando primeiro as letras mais certas |

## O microgpt e este, lado a lado

| | [microgpt](../microgpt/) | Micro Diffusion |
| --- | --- | --- |
| Escreve | uma letra depois da outra, da esquerda para a direita | todas as letras de uma vez, as mais certas primeiro |
| Modelo | um Transformer com atenção | uma MLP que vê o nome inteiro |
| Derivadas | autograd do `Value`, calculadas sozinhas | escritas à mão, camada por camada |
| Contas | um número de cada vez, Python puro | matrizes inteiras de uma vez, NumPy |
| Treino no mesmo Mac | 42 s, 1.000 nomes | 5 s, 320.000 nomes |

A última linha é o passo seguinte ao [quão rápido, e por quê](../microgpt/README.pt-BR.md#quão-rápido-e-por-quê): aqui a velocidade vem de fazer matrizes de uma vez, não de uma linguagem mais rápida.

## Para experimentar

- `--temperature 0.6` ou `1.0`: a rodada já imprime as duas; nomes mais seguros com 0,6, mais estranhos com 1,0.
- `--steps 500`: um décimo do treino. Os nossos saíram `jlmin`, `fnaicna`, `rdibnr`: a forma de um nome ainda não está lá.
- `T = 40` → `10` (numa cópia): quatro vezes menos passos para gerar, cada um revelando mais letras de uma vez. Esperávamos nomes piores e não vimos: os nossos saíram `karye`, `dorton`, `nona`, `narrah`. Quinze nomes são poucos para dizer; experimente e conte.

## Aprendemos com

- [Micro-Diffusion](https://github.com/Siwoo4985/Micro-Diffusion): o próprio código, e a ideia de explicar difusão de texto no mesmo estilo mínimo do microgpt.

## Para estudar em seguida

1. [microgpt](../microgpt/README.pt-BR.md), o jeito da esquerda para a direita, para comparar.
2. O [`train.py`](https://github.com/Siwoo4985/Micro-Diffusion/blob/main/train.py) do autor: a mesma difusão com um Transformer em PyTorch.
