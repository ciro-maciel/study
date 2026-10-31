# Embedding

[English](README.md) · [Caderno](../../README.pt-BR.md) · Anterior: [token](../token/README.pt-BR.md) · Próximo: [atenção](../attention/README.pt-BR.md)

**Em uma frase:** um embedding é a lista de números que o modelo aprende para cada token; tokens que se comportam parecido acabam com listas parecidas, e é assim que um número solto ganha significado.

## Como funciona

O token é só uma etiqueta: "a" é o número 0, "b" é o 1. Etiqueta não diz nada; 0 e 1 estarem perto não quer dizer que "a" e "b" se parecem. Por isso a primeira coisa que o modelo faz com cada token é trocá-lo por uma **lista de números** guardada numa tabela.

No [microgpt](../../../microgpt/microgpt.py), a tabela se chama `wte` (linha 81): 27 linhas, uma por token, cada uma com 16 números (`n_embd = 16`, linha 76). Na linha 109, `tok_emb = state_dict['wte'][token_id]` busca a linha do token. Na linha 110, uma segunda tabela, `wpe`, faz o mesmo para a **posição** (primeira letra, segunda letra...), e as duas listas são somadas.

No começo, a tabela é sorteada. Ninguém escreve nela. O treino ajusta esses números junto com todo o resto, só para errar menos a próxima letra. O que aparece na tabela depois é efeito colateral: letras que aparecem nos mesmos lugares acabam com listas parecidas.

Para medir "parecido", o experimento usa a **similaridade de cosseno**: +1 se as duas listas apontam para o mesmo lado, 0 se não têm relação, -1 se apontam para lados opostos.

## O que o artigo diz

No [artigo do Transformer](../../../papers/2017-attention-is-all-you-need.pdf):

> "we use learned embeddings to convert the input tokens and output tokens to vectors of dimension d_model"
> (seção 3.4, página 5)

E sobre a posição:

> "Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence."
> (seção 3.5, página 6)

O artigo usa senos e cossenos fixos para a posição; o microgpt, como o GPT-2, aprende a posição numa tabela, a `wpe`.

## O experimento

```bash
cd notebook/concepts/embedding
python3 embeddings.py
```

O [`embeddings.py`](embeddings.py) treina o microgpt pelos mesmos 1.000 passos do original e compara a tabela `wte` antes e depois. Num Mac com Python 3.15, em 31/10/2026, levou 47 segundos.

| | vogal com vogal | vogal com consoante | consoante com consoante |
| --- | --- | --- | --- |
| antes do treino | -0,01 | +0,00 | +0,00 |
| depois do treino | **+0,53** | **-0,29** | +0,22 |

| Letra | Mais parecidas, antes | Mais parecidas, depois |
| --- | --- | --- |
| `a` | t i w l | **o e u** q |
| `e` | m c o h | **u o a i** |
| `k` | j x b w | l j v w |
| `n` | p f j s | y h r w |

**Ninguém disse ao modelo o que é uma vogal.** Ele só tentou adivinhar a próxima letra de 1.000 nomes e, para isso, achou útil dar às vogais listas parecidas entre si e opostas às consoantes. A categoria "vogal" saiu dos dados.

Os 16 números do `a` depois do treino: `+0.13 +0.05 +0.24 -0.06 +0.04 -0.30 -0.40 -0.02 +0.01 +0.07 +0.35 +0.13 -0.09 -0.17 -0.17 -0.37`. Nenhum deles, sozinho, quer dizer "vogal"; o significado está no conjunto.

**Para experimentar:** troque `'aekn'` em `report()` por outras letras e veja quem fica perto de quem.

## Por que isso importa

- **É onde mora o "entendimento".** Num modelo grande, a mesma coisa acontece com milhares de dimensões e centenas de milhares de tokens: palavras de sentido parecido ficam com listas parecidas, sem ninguém ensinar sinônimos.
- **É a base da busca por significado.** Comparar embeddings é como um sistema acha o documento certo mesmo quando a pergunta usa outras palavras.
- **Explica um viés.** O modelo aprende as semelhanças que os dados mostram, inclusive as que ninguém queria.

## O que dá para construir

- **Busca por sentido num acervo próprio.** Um livro, uma base de atendimento ou um catálogo de receitas, onde a pessoa pergunta do jeito dela e acha o trecho certo.
- **Agrupar sem rotular.** Assim como as vogais se juntaram sozinhas, mensagens de clientes ou comentários se agrupam por assunto sem que alguém defina as categorias antes.
- **Um mapa visual.** Desenhar as 27 letras num plano, coloridas por vogal e consoante, antes e depois do treino: a figura mais simples para mostrar o que um modelo aprende.

## Perguntas em aberto

- O embedding diz o que cada token é. Mas como o modelo combina os tokens de uma frase, sabendo quais importam para o próximo? → **atenção**, a próxima página.
- O que aconteceria com as vogais se o modelo tivesse só 4 números por letra em vez de 16? (A página da [escala](../scale/README.pt-BR.md) treina larguras menores.)
