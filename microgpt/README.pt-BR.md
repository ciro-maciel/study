# microgpt: um GPT inteiro em 199 linhas

[English](README.md)

Um GPT completo, do texto à geração, em **199 linhas de Python puro**. Usa só `os`, `math` e `random`: sem PyTorch, sem NumPy, sem placa de vídeo. O arquivo abre assim: "este arquivo é o algoritmo completo; todo o resto é só eficiência".

- **Autor:** Andrej Karpathy
- **Original:** <https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95>
- **Versão fixada:** `14fb038816c7aae0bb9342c2dbf1a51dd134a5ff`
- **sha256:** `d47d88c2fd432c8ebdc1048beab7f7eb64ea7e0e664e11b812d72a6d95ebccee`

O código não fica guardado neste repositório. O `get.sh` baixa essa versão exata do gist do autor e se recusa a guardá-la se o sha256 for diferente.

## Rodar

```bash
./get.sh
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

## Para experimentar

Mude uma linha, rode de novo, compare. Edite uma cópia (`cp microgpt.py experimento.py`), para o `get.sh` manter o original intacto.

- `temperature = 0.5` → `1.0`: nomes mais estranhos. → `0.1`: nomes seguros e repetidos.
- `num_steps = 1000` → `3000`: erro menor, nomes mais convincentes, três vezes a espera.
- `n_embd = 16` → `32`: um modelo mais largo; veja quanto crescem os parâmetros e o tempo.
- Troque o `input.txt` por uma lista sua, um item por linha (cidades, nomes de produto, palavras em português) e não mude mais nada.

## Para estudar em seguida

1. [`micrograd`](https://github.com/karpathy/micrograd): só o autograd, explicado.
2. [`nn-zero-to-hero`](https://github.com/karpathy/nn-zero-to-hero): o curso em vídeo, do zero ao GPT.
3. [`nanoGPT`](https://github.com/karpathy/nanoGPT): o mesmo GPT em PyTorch, em escala de verdade.
4. [`nanochat`](https://github.com/karpathy/nanochat): um ChatGPT inteiro, de ponta a ponta.

E o livro: [*IA por dentro*](https://ciromaciel.click/books/ia-por-dentro?ref=oss-study), sobre por que a resposta sai aos pedaços, de onde vem o que o modelo sabe e como ele é treinado.
