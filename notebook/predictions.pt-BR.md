# Previsões

[English](predictions.md) · [Caderno](README.pt-BR.md)

O que achamos que a IA vai fazer, escrito antes de acontecer. Cada previsão tem quem fez, quando, uma frase que dá para conferir sem discussão e a data da conferência. Na data, a gente relê e dá a nota: **acertou**, **errou** ou **cedo demais**, com o motivo. Uma previsão nunca é apagada nem reescrita depois: é isso que dá valor à nota.

O objetivo não é acertar. É aprender a separar o que a IA faz de verdade do que é promessa, inclusive as nossas.

| # | Quem | Feita em | Previsão | Conferir em | Nota |
| --- | --- | --- | --- | --- | --- |
| 1 | Claude | 31/10/2026 | O mesmo texto em português vai custar **no máximo 20% a mais** de tokens do que em inglês no tokenizador do modelo mais novo do Claude. Como conferir: contar os tokens do [`sample.pt.md`](concepts/token/sample.pt.md) e do [`sample.en.md`](concepts/token/sample.en.md) com o contador de tokens da API. A medida de hoje ainda não foi feita; é a primeira tarefa da próxima sessão | 31/10/2027 | |
| 2 | Ciro | | | | |

**Medições de base** (anotadas ao lado, nunca dentro da previsão):

- **#1, em 31/10/2026:** o português já custa **16% a mais** no Claude Opus 5.5 (1.837 contra 1.581 tokens; veja a [página do token](concepts/token/README.pt-BR.md), experimento 4). A previsão já vale hoje: foi feita antes de medir e saiu fraca. A lição fica registrada: **medir antes de prever**. A conferência de 2027 continua, e o que importa nela passa a ser se a diferença caiu abaixo de 16%.
