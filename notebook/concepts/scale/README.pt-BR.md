# Escala

[English](README.md) · [Caderno](../../README.pt-BR.md) · Anterior: [treino](../training/README.pt-BR.md) · Próximo: [ajuste fino](../fine-tuning/README.pt-BR.md)

**Em uma frase:** um modelo maior erra menos de um jeito previsível, mas só se os dados e a computação crescerem junto; com os dados parados, crescer o modelo para de ajudar e só fica mais caro.

## Como funciona

O tamanho de um modelo é o número de parâmetros. No [microgpt](../../../microgpt/microgpt.py), o botão principal é a largura, `n_embd = 16` (linha 76): quantos números cada token carrega. Dobrar a largura quase quadruplica os parâmetros, porque as matrizes têm largura nas duas dimensões.

Três coisas podem crescer:

- **o modelo** (parâmetros);
- **os dados** (quantos exemplos diferentes ele vê);
- **a computação** (quantos passos, quanto cálculo).

A descoberta do artigo das leis de escala é que o erro cai numa curva previsível, uma **lei de potência**, quando se cresce qualquer uma delas, desde que as outras não estejam segurando. É como uma receita: dobrar a farinha não adianta se a água continua a mesma.

## O que o artigo diz

No [artigo das leis de escala](../../../papers/2020-scaling-laws-for-neural-language-models.pdf):

> "The loss scales as a power-law with model size, dataset size, and the amount of compute used for training, with some trends spanning more than seven orders of magnitude."
> (resumo, página 1)

E a fórmula para o tamanho do modelo:

> "For models with a limited number of parameters, trained to convergence on sufficiently large datasets: L(N) = (N_c/N)^α_N ; α_N ∼ 0.076"
> (seção 1.2, equação 1.1, página 4)

Na prática: **multiplicar os parâmetros por 10 multiplica o erro por cerca de 0,84**, ou seja, tira uns 16%. Cada multiplicação por 10 ganha a mesma fração, nunca um salto. A frase importante é a condição: "treinados até convergir, em dados suficientemente grandes".

## O experimento

```bash
cd notebook/concepts/scale
python3 scale.py
```

O [`scale.py`](scale.py) treina o mesmo microgpt em três larguras, com os mesmos 1.000 passos e os mesmos nomes, e mede todos nos mesmos 200 nomes que nenhum viu. Num Mac com Python 3.15, em 31/10/2026, levou 67 segundos. A largura 32 foi rodada à parte, trocando a lista de larguras.

| Largura | Parâmetros | Perda em nomes nunca vistos | Tempo de treino |
| --- | --- | --- | --- |
| 4 | 472 | 2,425 | 5 s |
| 8 | 1.328 (2,8×) | 2,386 (-0,039) | 13 s |
| 16 | 4.192 (3,2×) | 2,343 (-0,043) | 49 s |
| 32 | 14.528 (3,5×) | **2,336 (-0,007)** | **332 s** |

O que a tabela mostra:

- **Até a largura 16, a lei aparece.** Cada vez que os parâmetros quase triplicam, o erro cai uma fração parecida, cerca de 0,04. Ganhos pequenos e regulares, o formato que o artigo mede.
- **Depois, para.** De 16 para 32, o modelo ficou 3,5 vezes maior e o erro quase não se mexeu (-0,007). Os 1.000 nomes de treino viraram o gargalo: o modelo maior não tem mais o que aprender com tão poucos exemplos.
- **O custo não para.** O tempo de treino subiu quase 7 vezes, de 49 para 332 segundos, para um ganho que mal aparece.

Os números absolutos não são os do artigo: os nomes têm muita aleatoriedade que nenhum modelo elimina (ninguém adivinha a próxima letra de um nome com certeza), e o microgpt não treina até convergir. O que se repete é o formato: ganho regular enquanto os dados aguentam, e a parede quando eles acabam.

**Para experimentar:** troque `for width in [4, 8, 16]` por `[32]` para ver a largura 32 sozinha (cerca de 5 minutos), ou aumente os passos de `lab.train(ns, ns['docs'], 1000)` para dar mais dados aos modelos maiores.

## Por que isso importa

- **Explica a corrida por tamanho.** Como o ganho é previsível, dá para planejar quanto investir num modelo antes de treiná-lo. Foi essa previsibilidade que justificou treinar modelos cada vez maiores.
- **Explica por que dados viraram o recurso mais disputado.** O experimento mostra a parede: sem mais dados, mais modelo não resolve.
- **Ajuda a escolher modelo no dia a dia.** O modelo maior é mais caro e mais lento, e nem sempre erra menos na sua tarefa. Vale medir no seu caso antes de pagar pelo maior.

## O que dá para construir

- **Medir antes de trocar por um modelo maior.** Para um agente ou uma tarefa, rodar os mesmos casos de teste no modelo menor e no maior, e ver se a diferença paga o custo. Muitas vezes o gargalo é o exemplo ou a instrução, não o tamanho, como a largura 32 mostrou.
- **Uma calculadora de "vale a pena?".** Dado o custo de cada modelo e o erro medido em casos reais, mostrar o custo por acerto. É a tabela acima, em dinheiro.

## Perguntas em aberto

- Um modelo grande e bem treinado sabe muito, mas ainda só continua texto. Como ele vira um assistente que responde do jeito certo? → **ajuste fino**, a próxima página.
- Com 3.000 passos em vez de 1.000, a largura 32 volta a ganhar da 16?
