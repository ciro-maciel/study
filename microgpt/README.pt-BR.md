# microgpt: um GPT inteiro em 199 linhas

[English](README.md)

Um GPT completo, do texto à geração, em **199 linhas de Python puro**. Usa só `os`, `math` e `random`: sem PyTorch, sem NumPy, sem placa de vídeo. O arquivo abre assim: "este arquivo é o algoritmo completo; todo o resto é só eficiência".

- **Autor:** Andrej Karpathy
- **Original:** <https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95>
- **Copiado da versão:** `14fb038816c7aae0bb9342c2dbf1a51dd134a5ff`, em 31 de outubro de 2026, sem alteração
- **sha256:** `d47d88c2fd432c8ebdc1048beab7f7eb64ea7e0e664e11b812d72a6d95ebccee`

## Rodar

```bash
python3 microgpt.py
```

Na primeira vez ele baixa o `input.txt`: 32.033 nomes de pessoas, do repositório `makemore` do mesmo autor. Depois treina por 1.000 passos, mostrando o erro a cada um, e no fim inventa 20 nomes que não estavam na lista.

O que vimos num Mac com Python 3.15, em 31 de outubro de 2026:

| | |
| --- | --- |
| Parâmetros | 4.192 |
| Tempo de treino | 42 segundos |
| Erro (loss), primeiro passo | 3,37 |
| Erro (loss), últimos passos | cerca de 2,2 |
| Alguns nomes inventados | `kamon`, `karai`, `vialan`, `yeran`, `keylen`, `alerin` |

O erro oscila de um passo para o outro porque cada passo olha um nome só; acompanhe a tendência, não cada linha. O arquivo fixa a semente aleatória (`random.seed(42)`), então com o mesmo Python você deve ver os mesmos nomes que nós.

## Aprendeu ou decorou?

Os 1.000 passos de treino veem só os primeiros 1.000 nomes da lista embaralhada (`docs[step % len(docs)]`), então os outros 31.033 são nomes que o modelo nunca viu. O [`evaluate.py`](evaluate.py) roda o `microgpt.py` sem mudar nada e depois mede o erro médio por letra, o mesmo que o treino imprime:

```bash
python3 evaluate.py
```

O que medimos num Mac (Apple M4 Pro, Python 3.15.2) em 5 de novembro de 2026, em 64 segundos:

| Erro médio por letra (menor é melhor) | |
| --- | --- |
| Chutar cada letra ao acaso (27 opções) | 3,30 |
| Bigrama: cada letra pela anterior, contado nos mesmos 1.000 nomes, em 500 nomes novos | 2,52 |
| microgpt, em 500 nomes em que treinou | 2,35 |
| microgpt, em 500 nomes que nunca viu | 2,39 |

O erro nos nomes novos é quase o mesmo dos nomes do treino: ele aprendeu como um nome é feito, não decorou a lista. E ganha do bigrama, que só conhece a letra anterior. Essa diferença é o que a atenção compra.

## Um nome, passo a passo

O [`trace.py`](trace.py) roda o `microgpt.py` sem mudar nada e depois acompanha um único nome pelo modelo treinado: o token que entra em cada posição, as três letras que o modelo acha mais prováveis em seguida e a probabilidade que ele deu à certa. No mesmo Mac, em 5 de novembro de 2026, em 43 segundos:

```
--- "emma" as tokens: [26, 4, 12, 12, 0, 26] ---
after <BOS>  model guesses: a 14%, k 9%, j 8%             right answer e: 5%
after     e  model guesses: l 28%, r 12%, n 12%           right answer m: 6%
after     m  model guesses: i 22%, a 22%, e 18%           right answer m: 1%
after     m  model guesses: i 25%, a 23%, e 17%           right answer a: 23%
after     a  model guesses: n 30%, <BOS> 17%, r 10%       right answer <BOS>: 17%
```

Leia linha a linha. O `<BOS>` (token 26) marca onde um nome começa e termina. No começo o modelo aposta nas letras com que os nomes costumam começar. Depois de `em` ele espera uma vogal, então um segundo `m` leva 1%. Depois de `emm` o `a` certo está entre os três favoritos. Depois do `a` final ele dá 17% para o nome terminar ali. Cada um dos 1.000 passos de treino é esse mesmo caminho, com o erro de cada resposta certa empurrado um pouco para baixo. Teste o seu: `python3 trace.py anna`.

## O que tem dentro, na ordem do arquivo

| Parte | O que faz |
| --- | --- |
| **Dataset** | Lê a lista de nomes, um por linha, e embaralha |
| **Tokenizador** | Cada letra vira um número; um número a mais (`BOS`) marca onde um nome começa e termina |
| **Autograd** (`class Value`) | Cada conta guarda de onde veio, para depois o programa andar de trás para frente e descobrir quanto cada número contribuiu para o erro. É o `micrograd` do mesmo autor, embutido |
| **Parâmetros** | Os números que o modelo aprende: 1 camada, largura 16, contexto de 16 letras, 4 cabeças de atenção |
| **Modelo** | O GPT-2 com pequenas trocas: `rmsnorm` no lugar de `layernorm`, sem viés, `ReLU` no lugar de `GeLU` |
| **Adam** | O otimizador que ajusta cada parâmetro depois de cada passo |
| **Treino** | 1.000 passos: pega um nome, prevê cada próxima letra, mede o erro, ajusta |
| **Geração** | Gera nomes letra por letra; a `temperature` (0,5) controla o quanto ele arrisca |

## Quão rápido, e por quê

O mesmo algoritmo roda de jeitos muito diferentes, dependendo de quem o executa. [`microgpt.mjs`](microgpt.mjs) é o `microgpt.py` traduzido linha a linha para JavaScript: o mesmo `Value`, o mesmo modelo, o mesmo Adam, os mesmos 1.000 passos. Só o gerador aleatório muda, então os nomes vêm em outra ordem; por isso a tabela compara o tempo por letra lida.

```bash
python3 speed.py      # roda o microgpt.py sem alterar e mede o tempo
node microgpt.mjs
bun microgpt.mjs
```

O que medimos num Mac (Apple M4 Pro) em 6 de novembro de 2026, a mediana de três rodadas de cada:

| Quem roda | Treino | Letras lidas | Por letra | Contra o Python |
| --- | --- | --- | --- | --- |
| Python 3.15.2 (CPython) | 43,3 s | 7.170 | 6.042 µs | 1× |
| Node 26.13 (V8) | 5,9 s | 7.116 | 834 µs | 7,2× mais rápido |
| Bun 1.4 (JavaScriptCore) | 3,3 s | 7.116 | 457 µs | 13,2× mais rápido |

O tempo do Python é a execução inteira (o `speed.py` não alcança o interior do arquivo, que fica intocado); medindo só o laço de treino numa cópia, deu 42,0 s de 42,1 s, então a diferença é pequena. As rodadas se repetem: toda rodada de cada um terminou no mesmo erro (2,6497 no Python, 2,2999 no JavaScript).

De onde vem a diferença: a conta é a mesma, número por número, então a distância está em como cada máquina a executa. O CPython lê o programa e o executa instrução por instrução, toda vez; o V8 e o JavaScriptCore percebem o código que se repete (aqui, os milhões de operações de `Value`) e o compilam nas instruções do próprio processador enquanto ele roda. Isso é um compilador just-in-time, e neste programa ele vale de 7 a 13 vezes.

Nenhum dos três faz o que os modelos de verdade fazem: aqui cada número ainda é um objeto, um de cada vez. O próximo degrau de velocidade, fazer matrizes inteiras de uma vez, numa GPU, é para o que existe o PyTorch; ele não está medido aqui.

## Para experimentar

Mude uma linha, rode de novo, compare. Edite uma cópia (`cp microgpt.py experimento.py`), para o original ficar intacto.

- `temperature = 0.5` → `1.0`: nomes mais estranhos. → `0.1`: nomes seguros e repetidos.
- `num_steps = 1000` → `3000`: erro menor, nomes mais convincentes, três vezes a espera.
- `n_embd = 16` → `32`: um modelo mais largo; veja quanto crescem os parâmetros e o tempo.
- Troque o `input.txt` por uma lista sua, um item por linha (cidades, nomes de produto, palavras em português) e não mude mais nada.

## Aprendemos com

- [microGPT-C](https://github.com/vixhal-baraiya/microgpt-c): medir em nomes que o modelo nunca viu, contra uma base simples (`evaluate.py`).
- [NamiGPT](https://github.com/aa1143/NamiGPT): seguir um exemplo mínimo do primeiro token ao último palpite (`trace.py`).
- [microgpt-efficiency](https://github.com/chanjoongx/microgpt-efficiency): medir o mesmo algoritmo em mais de uma implementação para mostrar de onde vem a velocidade (`speed.py`, `microgpt.mjs`).

## Para estudar em seguida

1. [`micrograd`](https://github.com/karpathy/micrograd): só o autograd, explicado.
2. [`nn-zero-to-hero`](https://github.com/karpathy/nn-zero-to-hero): o curso em vídeo, do zero ao GPT.
3. [`nanoGPT`](https://github.com/karpathy/nanoGPT): o mesmo GPT em PyTorch, em escala de verdade.
4. [`nanochat`](https://github.com/karpathy/nanochat): um ChatGPT inteiro, de ponta a ponta.

E o livro: [*IA por dentro*](https://ciromaciel.click/books/ia-por-dentro?ref=oss-study), sobre por que a resposta sai aos pedaços, de onde vem o que o modelo sabe e como ele é treinado.
