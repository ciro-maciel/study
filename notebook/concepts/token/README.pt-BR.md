# Token

[English](README.md) · [Caderno](../../README.pt-BR.md) · Próximo: embedding (ainda não escrito)

**Em uma frase:** um token é o pedaço de texto que o modelo enxerga como uma unidade; ele não lê letras nem palavras, lê uma sequência de números, e cada número é um pedaço.

## Como funciona

Um modelo de linguagem só faz conta. Antes de qualquer coisa, o texto precisa virar número, e o **tokenizador** é a peça que faz isso, nos dois sentidos: texto para números na entrada, números para texto na saída.

Há duas formas de cortar o texto, e o repositório tem as duas:

- **Uma letra, um token.** É o que o [microgpt](../../../microgpt/microgpt.py) faz nas linhas 24 a 26: junta todas as letras que aparecem nos nomes, ordena, e a posição de cada letra na lista vira o número dela. São 26 letras mais um token especial (`BOS`) que marca onde um nome começa e termina: 27 no total. Simples, mas cada palavra vira muitos tokens, e o modelo precisa aprender do zero que "t" e "h" juntos costumam formar "th".
- **Pedaços que se repetem.** É o que os modelos de verdade fazem, com a técnica chamada **byte-pair encoding** (BPE). Começa com os 256 bytes possíveis, procura o par de vizinhos que mais aparece no texto, cola os dois num token novo e repete. Depois de algumas centenas de colagens, as partes comuns da língua viram um token só: "the ", "ção", "ing".

Por isso um modelo como o Claude não vê "atenção" como uma palavra: vê de um a alguns pedaços, conforme o que o tokenizador dele aprendeu.

## O que o artigo diz

No [artigo do Transformer](../../../papers/2017-attention-is-all-you-need.pdf), duas passagens curtas:

> "we use learned embeddings to convert the input tokens and output tokens to vectors of dimension d_model"
> (seção 3.4, página 5)

Ou seja: depois do tokenizador, cada número vira uma lista de números aprendida, o **embedding**. É o próximo conceito do caderno.

> "Sentences were encoded using byte-pair encoding [3], which has a shared source-target vocabulary of about 37000 tokens."
> (seção 5.1, página 7)

O Transformer original já usava BPE, com um vocabulário de cerca de 37 mil tokens.

## O experimento

```bash
cd notebook/concepts/token
python3 tokens.py
```

O [`tokens.py`](tokens.py) é um tokenizador BPE em Python puro, com 300 colagens, treinado no README deste repositório, congelado em 31/10/2026 em [`sample.en.md`](sample.en.md) e [`sample.pt.md`](sample.pt.md): o mesmo texto em inglês e em português. Roda em menos de um segundo.

O que saiu num Mac com Python 3.15, em 31 de outubro de 2026:

**1. Uma letra, um token:** `attention` vira 9 tokens.

**2. BPE treinado no texto em inglês.** Os primeiros pedaços que ele aprendeu: `e␣`, `th`, `s␣`, `,␣`, `in`, `t␣`. Os mais longos são links inteiros, como `](https://ciromaciel.click/?ref=oss-study)`, porque se repetem muito nesse texto: **o tokenizador aprende o que se repete, não o que faz sentido.**

| Texto | Tokens | Pedaços |
| --- | --- | --- |
| `the code` | 3 | `the␣` · `co` · `de` |
| `microgpt` | 1 | `microgpt` |
| `attention` | 4 | `a` · `tt` · `ent` · `ion` |
| `atenção` | 7 | `at` · `en` · `<c3>` · `<a7>` · `<c3>` · `<a3>` · `o` |

O "ç" e o "ã" ocupam dois bytes cada. Um tokenizador que só viu inglês nunca juntou esses bytes, então cada letra acentuada vira dois tokens que, sozinhos, nem são letra.

**3. O mesmo texto, duas línguas, dois tokenizadores:**

| Treinado em | Inglês | Português | O português custa |
| --- | --- | --- | --- |
| inglês | 1.535 tokens | 2.199 tokens | **43% a mais** |
| português | 2.176 tokens | 1.606 tokens | 26% a menos |

Os dois textos têm quase o mesmo tamanho (4.092 e 4.174 caracteres). O que muda é a língua em que o tokenizador aprendeu.

**Para experimentar:**
- `MERGES = 300` → `30`: poucas colagens, pedaços curtos. `microgpt` vira 6 tokens (`m · ic · ro · g · p · t`) e o português custa só 13% a mais.
- `MERGES = 300` → `1000`: o tokenizador **decora o texto**. Com pouco texto e colagens demais, o começo do README inteiro vira um único token, e o português passa a custar 216% a mais. É o mesmo problema que um modelo tem quando decora os exemplos em vez de aprender: funciona perfeito no que já viu e mal em todo o resto.
- Troque `'atenção'` na lista de palavras por seu nome, ou por uma palavra técnica do seu trabalho.

## Por que isso importa

- **Preço.** Modelos são cobrados por token, na entrada e na saída. O mesmo pedido pode custar mais em português do que em inglês, conforme o tokenizador do modelo.
- **Memória.** O limite de contexto ("quanto o modelo lembra de uma vez") é contado em tokens, não em páginas.
- **A resposta sai aos pedaços.** O modelo gera **um token por vez**: escolhe o próximo pedaço, acrescenta ao texto e repete. É por isso que a resposta aparece aos poucos na tela, e é a pergunta da capa do *IA por dentro*.
- **Erros curiosos.** Contar letras de uma palavra é difícil para um modelo porque ele não vê as letras, vê os pedaços.

A medida do experimento 3 vale para este tokenizador pequeno, treinado num texto só. Os tokenizadores dos modelos grandes aprendem com muito mais texto e muitas línguas, então a diferença real é outra. O mecanismo é o mesmo, e a diferença real se mede contando os tokens do mesmo texto nos dois idiomas no modelo que se usa.

## O que dá para construir

- **Medir antes de escolher a língua de um agente.** Um agente de IA manda as mesmas instruções em todo pedido. Contar os tokens dessas instruções em português e em inglês, no modelo que ele usa, diz se vale escrevê-las em inglês e deixar só a conversa com a pessoa em português.
- **Uma ferramenta grátis: "quanto custa o seu texto".** A pessoa cola um texto e vê os pedaços coloridos e quantos tokens ele custa. Ensina o conceito em dez segundos.
- **O anexo prático do livro.** Os capítulos "Uma palavra de cada vez" e "A matéria-prima: dados e tokens" do [*IA por dentro*](https://ciromaciel.click/books/ia-por-dentro?ref=oss-study) explicam em palavras; este experimento é o "faça você mesmo" deles.

## Perguntas em aberto

- Se o token é só um número, como o modelo sabe que "gato" e "cachorro" estão mais perto um do outro do que de "parafuso"? → **embedding**, a próxima página.
- Quantos tokens tem o vocabulário do Claude, e quanto o português custa a mais nele? Medir com o contador de tokens da API.
