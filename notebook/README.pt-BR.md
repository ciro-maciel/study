# O caderno

[English](README.md) · [Repositório](../README.pt-BR.md)

Um caderno de estudo sobre inteligência artificial, mantido por duas pessoas, por assim dizer: o **Ciro Cesar Maciel**, que pergunta, roda e decide o que vale a pena, e o **Claude**, que escreve as páginas, liga uma à outra e as mantém em dia. Ele responde três perguntas: o que é a IA, como ela funciona por dentro e o que dá para construir com ela.

Uma coisa honesta sobre o Claude: ele não aprende entre conversas. Cada sessão começa do zero. O que acumula é o que fica escrito aqui, e é por isso que este caderno existe: ele é a memória que permite continuar de onde paramos.

## Como funciona

| Camada | O que é | Quem escreve |
| --- | --- | --- |
| **Fontes** | O código e os artigos em [`../microgpt/`](../microgpt/) e [`../papers/`](../papers/), sempre intactos | os autores originais |
| **Páginas** | Um conceito por pasta em [`concepts/`](concepts/), com explicação, trecho do artigo, um experimento que roda num notebook, por que importa e o que dá para construir | o Claude, a partir das perguntas do Ciro |
| **Regras** | Como o caderno é mantido, em [`../AGENTS.md`](../AGENTS.md) | os dois, ajustando com o tempo |

E dois arquivos que crescem a cada sessão:

- [`log.md`](log.md): o que foi feito e quando, uma linha por evento.
- [`predictions.pt-BR.md`](predictions.pt-BR.md): o que achamos que a IA vai fazer, com data, para conferir depois.

**Cada sessão:** escolher o próximo conceito da escada, ler a página, rodar o experimento, perguntar. Toda boa pergunta vira trecho de página ou página nova, em vez de se perder na conversa. De tempos em tempos, uma **auditoria**: o que ficou velho, o que se contradiz, o que é citado e ainda não tem página.

## A escada

Do menor conceito ao maior, cada um apoiado no anterior. Todas as páginas estão prontas desde 31/10/2026.

| | Conceito | Fonte | O que o experimento mostrou |
| --- | --- | --- | --- |
| 1 | [**Token**](concepts/token/README.pt-BR.md): como o texto vira número | microgpt · Transformer, seções 3.4 e 5.1 | O mesmo texto custa 43% mais tokens em português num tokenizador treinado em inglês; no Claude, 16% |
| 2 | [**Embedding**](concepts/embedding/README.pt-BR.md): como um número ganha significado | microgpt · Transformer, seções 3.4 e 3.5 | Sem ninguém dizer o que é vogal, as vogais ficam parecidas entre si (+0,53) e opostas às consoantes (-0,29) |
| 3 | [**Atenção**](concepts/attention/README.pt-BR.md): como cada token olha para os outros | microgpt · Transformer, seção 3.2 | As 4 cabeças aprendem hábitos diferentes: uma olha a própria letra, outra volta ao começo do nome |
| 4 | [**Gradiente**](concepts/gradient/README.pt-BR.md): como um número aprende | microgpt (`class Value`) · Transformer, seção 5.3 | Passo pequeno contra o gradiente melhora; passo grande demais faz o erro explodir de 3,5 para 24 |
| 5 | [**Treino**](concepts/training/README.pt-BR.md): o laço de prever, errar e ajustar | microgpt · Transformer, seção 5.2 | A perda sai de 3,30 (chute) para 2,28, e fica em 2,34 em nomes nunca vistos: aprendeu, não decorou |
| 6 | [**Escala**](concepts/scale/README.pt-BR.md): por que maior fica melhor, e até onde | Scaling Laws, seção 1.2 | Até 4.192 parâmetros, cada modelo quase 3 vezes maior erra um pouco menos; com 14.528 o erro quase não mexe e o treino fica 7 vezes mais lento: faltam dados |
| 7 | [**Do modelo ao assistente**](concepts/fine-tuning/README.pt-BR.md): ajuste fino | Constitutional AI, resumo | 150 passos levam os nomes com "z" de 1,5% a 100%, mas o modelo esquece o resto; misturar exemplos protege |
| 8 | [**Princípios escritos**](concepts/constitution/README.pt-BR.md): a constituição | Constitutional AI, resumo e figura 1 | Dois princípios e as próprias revisões levam as violações de 40% a 0%, ao custo de boa parte da variedade |
| 9 | [**Agentes**](concepts/agents/README.pt-BR.md): o modelo que usa ferramentas | o formato `tool_use` / `tool_result` do Claude | O modelo só decide o que pedir; quem conta e executa é o programa |

## O que a escada ensina, junto

- **Nada é escrito à mão.** Vogais, cabeças de atenção, o jeito de responder: tudo sai de passinhos contra o gradiente, em cima de dados.
- **Todo ganho tem um preço medido.** Português custa mais tokens, passo grande demais explode, ajustar demais apaga o resto, obedecer demais tira a variedade. As páginas mostram cada preço em números.
- **Julgar no que não foi visto.** Em todas as páginas que treinam, a medida que importa é a dos nomes que o modelo nunca viu.
- **O modelo pensa, o programa age.** O último degrau junta tudo: um modelo que só gera texto vira trabalho quando ganha ferramentas e um laço com regras.

## Para rodar tudo

Os experimentos estão em Python puro, sem nada para instalar. O [`lab.py`](lab.py) carrega o microgpt original sem mudar o arquivo e reproduz exatamente o resultado dele (os mesmos 20 nomes, o mesmo erro final de 2,6497). Rodando um de cada vez num Mac com Python 3.15, o mais rápido leva meio segundo e o mais longo, 80 segundos (o do ajuste fino).

A escada não é fixa: uma pergunta boa no meio do caminho pode virar degrau novo.
