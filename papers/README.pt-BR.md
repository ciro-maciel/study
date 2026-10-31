# Os três artigos por trás do Claude

[English](README.md)

Perguntamos ao Claude (Opus 5.5) quais três artigos científicos mais fizeram dele o que ele é. Ele escolheu um para cada camada: a arquitetura sobre a qual é construído, o motivo de ser tão grande e o método que molda como ele se comporta. Os PDFs estão aqui, do arXiv, sem alteração.

| | Artigo | Autores | O que deu ao Claude |
| --- | --- | --- | --- |
| 1 | [Attention Is All You Need](2017-attention-is-all-you-need.pdf) (2017, 15 páginas) | Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin (Google) | **A arquitetura.** O Transformer: uma rede que lê todas as palavras de uma vez e aprende em quais prestar atenção. Todo grande modelo de linguagem de hoje, o Claude incluído, é um Transformer |
| 2 | [Scaling Laws for Neural Language Models](2020-scaling-laws-for-neural-language-models.pdf) (2020, 30 páginas) | Kaplan, McCandlish, Henighan, Brown, Chess, Child, Gray, Radford, Wu, Amodei (OpenAI) | **O motivo do tamanho.** O erro de um modelo de linguagem cai de forma previsível conforme crescem os parâmetros, os dados e a computação, então dá para planejar um modelo antes de treiná-lo. Quatro dos autores, Jared Kaplan, Sam McCandlish, Tom Brown e Dario Amodei, depois cofundaram a Anthropic |
| 3 | [Constitutional AI: Harmlessness from AI Feedback](2022-constitutional-ai.pdf) (2022, 34 páginas) | Bai, Kadavath, Kundu, Askell e outros (Anthropic) | **O comportamento.** Em vez de milhares de pessoas marcarem cada resposta prejudicial, o modelo critica e reescreve as próprias respostas a partir de uma lista curta de princípios escritos, uma "constituição", e aprende com isso. É o método da própria Anthropic e o mais característico do Claude |

## Leia junto com o código

- **Artigo 1, depois [`../microgpt/`](../microgpt/).** O microgpt é um Transformer em 199 linhas: as cabeças de atenção, as conexões residuais e a normalização da seção 3 do artigo estão todas lá, um laço cada. Leia a figura da página 3 e depois ache cada caixa no arquivo.
- **Artigo 2, depois mude o `n_embd` no microgpt.** A figura 1 do artigo mostra o erro caindo conforme o modelo cresce. Dobrar a largura do microgpt e rodar de novo é a menor versão desse experimento que dá para fazer num notebook.
- **O artigo 3 não tem código aqui.** Ele precisa de um modelo grande o bastante para ler e criticar as próprias respostas. Leia a seção 1 para a ideia e a figura 1 para as duas etapas: o modelo se corrigindo e depois aprendendo com as próprias preferências.

## De onde vêm

| Arquivo | arXiv | Versão | sha256 |
| --- | --- | --- | --- |
| `2017-attention-is-all-you-need.pdf` | [1706.03762](https://arxiv.org/abs/1706.03762) | v7, 2 ago. 2023 | `bdfaa68d8984f0dc02beaca527b76f207d99b666d31d1da728ee0728182df697` |
| `2020-scaling-laws-for-neural-language-models.pdf` | [2001.08361](https://arxiv.org/abs/2001.08361) | v1, 23 jan. 2020 | `a41bd7877fd1a6bcbba096b2619618bd2f90e02488f2365644903eb2f7c6a494` |
| `2022-constitutional-ai.pdf` | [2212.08073](https://arxiv.org/abs/2212.08073) | v1, 15 dez. 2022 | `9a456a07ad346e3372f9867d346f69f5b0f68b4c65f060aca0b8a13fa9d98e83` |

Baixados em 31 de outubro de 2026. Cada artigo é dos seus autores; veja o [NOTICE](../NOTICE).

O livro [*IA por dentro*](https://ciromaciel.click/books/ia-por-dentro?ref=oss-study) explica as ideias desses artigos em palavras simples.
