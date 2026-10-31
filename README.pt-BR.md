# Study, por Ciro Cesar Maciel

**Aprenda como a IA funciona rodando o menor código de verdade que faz isso, com um guia do lado.**

Por [Ciro Cesar Maciel](https://ciromaciel.click/?ref=oss-study), autor de [*IA por dentro*](https://ciromaciel.click/books/ia-por-dentro?ref=oss-study), o livro que explica como funcionam por dentro as inteligências artificiais que conversam.

[English](README.md)

Cada pasta guarda um código de referência, daqueles que um pesquisador escreve para mostrar a ideia inteira no menor número de linhas, exatamente como o autor publicou, e acrescenta o que o original deixa por sua conta: o que cada parte faz, como rodar, o que apareceu na tela quando rodamos e o que estudar depois.

## Comece aqui: um GPT inteiro em 199 linhas

```bash
git clone https://github.com/ciro-maciel/study && cd study/microgpt
python3 microgpt.py
```

A pasta [`microgpt/`](microgpt/) traz o microgpt do Andrej Karpathy: um GPT completo, com treino e geração, em Python puro. Sem PyTorch, sem NumPy, sem placa de vídeo; só `os`, `math` e `random`. Ele lê 32.033 nomes, aprende 4.192 números e depois inventa nomes que não estavam na lista.

Num Mac, com Python 3.15, o treino levou **42 segundos**. O erro caiu de 3,37 no primeiro passo para cerca de 2,2 no fim, e o modelo inventou `kamon`, `karai`, `vialan`, `yeran`, `keylen` e `alerin`.

O [guia](microgpt/README.pt-BR.md) percorre o arquivo de cima a baixo: o tokenizador, o autograd que faz o modelo aprender, a atenção, o otimizador, o laço de treino e a geração.

**Prefere ver a rodar?** [Treine um GPT](https://ciromaciel.click/tools/train-gpt?ref=oss-study) é o mesmo algoritmo reescrito em JavaScript, treinando no seu navegador em menos de um minuto, com cada número à vista: os parâmetros saindo do ruído, as quatro cabeças de atenção, os 64 neurônios e a chance de cada próxima letra.

## O que tem aqui

| Pasta | O que você aprende | Original de | Tempo para rodar |
| --- | --- | --- | --- |
| [`microgpt/`](microgpt/) | Como um GPT é montado e treinado, cada passo à vista | Andrej Karpathy | menos de um minuto |
| [`books/`](books/README.pt-BR.md) | Livros completos de domínio público, a começar por *A Riqueza das Nações*, de Adam Smith (1776) | os seus autores | leitura |
| [`papers/`](papers/) | Os três artigos científicos por trás do Claude: o Transformer, as leis de escala e a Constitutional AI, com como ler cada um junto com o código | pesquisadores do Google, da OpenAI e da Anthropic | leitura |

Novas pastas chegam conforme os livros precisam. Uma boa próxima pasta é um código pequeno, completo e que roda, explicando uma ideia só; veja o [CONTRIBUTING.md](CONTRIBUTING.md).

## Por que existe

A maioria das explicações de IA para na analogia ou pula direto para frameworks que escondem o mecanismo. Um código de referência como o microgpt mostra o mecanismo inteiro, mas foi escrito para quem já sabe o que está lendo. Este repositório fica no meio: o código de verdade, rodado de verdade, explicado em palavras simples, em português e em inglês.

É também o laboratório da série de livros *O Novo Básico*: [*IA por dentro*](https://ciromaciel.click/books/ia-por-dentro?ref=oss-study) explica em palavras como um modelo é treinado; aqui você treina um.

## Mais do Ciro Cesar Maciel

Eu faço software sozinho, com uma equipe de agentes de IA, e abro o que posso.

- **[Livros](https://ciromaciel.click/books?ref=oss-study)**: *O Novo Básico*, o que todo mundo precisa saber de IA para trabalhar, da primeira conversa com uma IA até a profissão que a implanta dentro das empresas.
- **Seis apps de Mac grátis e abertos**, MIT, assinados e autenticados pela Apple: [Cleaner](https://github.com/ciro-maciel/cleaner), [Screenshots](https://github.com/ciro-maciel/screenshots), [Speech to Text](https://github.com/ciro-maciel/speech-to-text), [Assistant](https://github.com/ciro-maciel/voice-assistant), [Windows](https://github.com/ciro-maciel/windows) e [Text to Speech](https://github.com/ciro-maciel/text-to-speech).
- **[Ferramentas grátis no navegador](https://ciromaciel.click/tools?ref=oss-study)** e o [Infrastructure](https://myinfrastructure.click/?ref=oss-study), a infraestrutura que agentes de IA já sabem operar.

**Acompanhe.** [Siga @ciro-maciel](https://github.com/ciro-maciel) e dê uma estrela neste repositório para ver cada pasta nova, e veja como tudo é feito no [YouTube](https://www.youtube.com/@ciro-maciel) e em [ciromaciel.click](https://ciromaciel.click/?ref=oss-study).

## Licença

Os guias deste repositório são MIT ([LICENSE](LICENSE)). O código de referência de cada pasta é do seu autor, creditado no topo do guia e no [NOTICE](NOTICE).
