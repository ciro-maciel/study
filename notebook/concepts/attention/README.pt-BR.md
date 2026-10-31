# Atenção

[English](README.md) · [Caderno](../../README.pt-BR.md) · Anterior: [embedding](../embedding/README.pt-BR.md) · Próximo: [gradiente](../gradient/README.pt-BR.md)

**Em uma frase:** atenção é o passo em que cada token olha para os tokens anteriores e decide quanto cada um importa para prever o próximo; é a ideia que dá nome ao artigo do Transformer.

## Como funciona

Depois do embedding, cada token tem a sua lista de números, mas ainda está sozinho. Para prever a letra seguinte de "isabel", o modelo precisa olhar para trás: o que veio antes muda tudo.

A atenção faz isso com três listas por token, calculadas a partir do embedding:

- **pergunta** (`q`, query): o que este token está procurando;
- **chave** (`k`, key): o que cada token anterior oferece;
- **valor** (`v`, value): o que cada token anterior entrega se for escolhido.

O modelo compara a pergunta do token atual com a chave de cada token anterior (uma multiplicação e uma soma), transforma as notas em porcentagens que somam 100% (o `softmax`) e mistura os valores nessa proporção. No [microgpt](../../../microgpt/microgpt.py) isso são duas linhas: a 129 calcula as notas (`attn_logits`) e a 130 as transforma em pesos (`attn_weights = softmax(attn_logits)`).

E isso acontece em **4 cabeças** ao mesmo tempo (o laço da linha 124), cada uma com as próprias perguntas e chaves. Cada cabeça pode aprender a procurar uma coisa diferente.

## O que o artigo diz

No [artigo do Transformer](../../../papers/2017-attention-is-all-you-need.pdf):

> "We call our particular attention "Scaled Dot-Product Attention" (Figure 2). The input consists of queries and keys of dimension d_k, and values of dimension d_v. We compute the dot products of the query with all keys, divide each by √d_k, and apply a softmax function to obtain the weights on the values."
> (seção 3.2.1, página 4)

A divisão por √d_k está no microgpt: é o `/ head_dim**0.5` da linha 129. E sobre as várias cabeças:

> "Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions."
> (seção 3.2.2, página 5)

## O experimento

```bash
cd notebook/concepts/attention
python3 attention.py
```

O [`attention.py`](attention.py) treina o microgpt pelos 1.000 passos e depois espia os pesos da linha 130 enquanto ele lê 300 nomes que nunca viu. O arquivo original não muda: o laboratório do caderno ([`lab.py`](../../lab.py)) acrescenta, só na memória, uma linha que anota os pesos. Num Mac com Python 3.15, em 31/10/2026, levou 53 segundos.

**Para onde cada cabeça olha, em média** (a partir da terceira letra, quando início, letra anterior e letra atual são três tokens diferentes):

| Cabeça | início do nome | letra anterior | letra atual | o resto |
| --- | --- | --- | --- | --- |
| 0 | 22% | 24% | 18% | 36% |
| 1 | 19% | 29% | 21% | 30% |
| 2 | 19% | 30% | 12% | 39% |
| 3 | 20% | 29% | 10% | 41% |

**Lendo "isabella"** (o ponto é o token de início), o token para onde cada cabeça mais olha em cada posição:

| Lendo | cabeça 0 | cabeça 1 | cabeça 2 | cabeça 3 |
| --- | --- | --- | --- | --- |
| `i` | `.` 73% | `.` 76% | `i` 56% | `.` 67% |
| `s` | `.` 44% | `s` 44% | `i` 37% | `.` 45% |
| `a` | `i` 26% | `a` 45% | `i` 60% | `.` 58% |
| `b` | `i` 26% | `a` 30% | `i` 35% | `.` 21% |
| `e` | `i` 19% | `e` 32% | `b` 56% | `.` 37% |
| `l` | `i` 26% | `.` 19% | `.` 21% | `a` 23% |
| `l` | `i` 22% | `.` 15% | `.` 23% | `e` 19% |
| `a` | `i` 14% | `l` 18% | `b` 70% | `l` 30% |

As cabeças não fazem a mesma coisa. A 1 olha muito para a própria letra; a 2 volta com força a letras marcantes do começo (`i`, `b`); a 3 olha para o início do nome nas primeiras letras, o que ajuda a saber em que ponto do nome está; a 0 fica presa no `i` inicial. Ninguém deu a elas esses papéis: eles saíram do treino, como as vogais no embedding.

O que não dá para dizer: que cada cabeça "entende" uma regra. Os números mostram para onde ela olha, não por quê. Ler o porquê dentro de um modelo é um campo de pesquisa inteiro, a interpretabilidade.

**Para experimentar:** troque `name = 'isabella'` por outro nome e veja se as cabeças mantêm os mesmos hábitos.

## Por que isso importa

- **É o que deixa o modelo ler contexto.** "Banco" quer dizer coisas diferentes em "sentei no banco da praça" e "abri conta no banco"; é a atenção que deixa o resto da frase decidir.
- **É por que o contexto custa.** Cada token olha para todos os anteriores. Dobrar o texto dobra o número de tokens e quadruplica o número de comparações. Por isso contexto longo é caro e lento.
- **É o coração do Transformer.** Antes dele, os modelos liam uma palavra por vez, em ordem. Com atenção, todas as posições são calculadas em paralelo, o que permitiu treinar modelos muito maiores.

## O que dá para construir

- **Um visualizador de atenção.** A pessoa digita uma frase e vê, colorido, para onde o modelo olhou em cada palavra. Ensina em segundos o que levaria um capítulo.
- **Mandar menos contexto.** Sabendo que cada token compara com todos os anteriores, vale mandar a um modelo só o trecho que importa: fica mais barato, mais rápido e, muitas vezes, melhor.

## Perguntas em aberto

- Os pesos da atenção não foram escritos por ninguém. Como o modelo chegou a eles? → **gradiente**, a próxima página.
- Com mais camadas, uma cabeça pode olhar para o resultado de outra. O que muda quando o `n_layer` passa de 1 para 2?
