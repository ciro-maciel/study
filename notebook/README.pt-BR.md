# O caderno

[English](README.md) · [Repositório](../README.pt-BR.md)

Um caderno de estudo sobre inteligência artificial, mantido por duas pessoas, por assim dizer: o **Ciro Cesar Maciel**, que pergunta, roda e decide o que vale a pena, e o **Claude**, que escreve as páginas, liga uma à outra e as mantém em dia. Ele responde três perguntas: o que é a IA, como ela funciona por dentro e o que dá para construir com ela.

Uma coisa honesta sobre o Claude: ele não aprende entre conversas. Cada sessão começa do zero. O que acumula é o que fica escrito aqui, e é por isso que este caderno existe: ele é a memória que permite continuar de onde paramos.

## Como funciona

| Camada | O que é | Quem escreve |
| --- | --- | --- |
| **Fontes** | O código e os artigos em [`../microgpt/`](../microgpt/) e [`../papers/`](../papers/), sempre intactos | os autores originais |
| **Páginas** | Um conceito por pasta em [`concepts/`](concepts/), com explicação, trecho do artigo, um experimento que roda em menos de um minuto, por que importa e o que dá para construir | o Claude, a partir das perguntas do Ciro |
| **Regras** | Como o caderno é mantido, em [`../AGENTS.md`](../AGENTS.md) | os dois, ajustando com o tempo |

E dois arquivos que crescem a cada sessão:

- [`log.md`](log.md): o que foi feito e quando, uma linha por evento.
- [`predictions.pt-BR.md`](predictions.pt-BR.md): o que achamos que a IA vai fazer, com data, para conferir depois.

**Cada sessão:** escolher o próximo conceito da escada, ler a página, rodar o experimento, perguntar. Toda boa pergunta vira trecho de página ou página nova, em vez de se perder na conversa. De tempos em tempos, uma **auditoria**: o que ficou velho, o que se contradiz, o que é citado e ainda não tem página.

## A escada

Do menor conceito ao maior, cada um apoiado no anterior.

| | Conceito | Fonte | Página |
| --- | --- | --- | --- |
| 1 | **Token**: como o texto vira número | microgpt · Transformer, seções 3.4 e 5.1 | [pronta](concepts/token/README.pt-BR.md) |
| 2 | **Embedding**: como um número ganha significado | microgpt · Transformer, seção 3.4 | próxima |
| 3 | **Atenção**: como cada palavra olha para as outras | microgpt · Transformer, seção 3.2 | |
| 4 | **Gradiente**: como um número aprende | microgpt (`class Value`) | |
| 5 | **Treino**: o laço de prever, errar e ajustar | microgpt | |
| 6 | **Escala**: por que maior fica melhor, e até onde | Scaling Laws | |
| 7 | **Do modelo ao assistente**: ajuste fino e preferências | Constitutional AI | |
| 8 | **Princípios escritos**: a constituição | Constitutional AI | |
| 9 | **Agentes**: o modelo que usa ferramentas | | |

A escada não é fixa: uma pergunta boa no meio do caminho pode virar degrau novo.
