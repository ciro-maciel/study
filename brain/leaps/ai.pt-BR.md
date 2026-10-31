# Inteligência artificial (2017 a 2022, em curso)

[English](ai.md) · [Cérebro](../README.pt-BR.md) · Anterior: [redes sociais](social-networks.pt-BR.md) · Próximo: [robôs](robots.pt-BR.md)

**Em uma frase:** os modelos de linguagem estão tornando barato produzir texto, código e raciocínio sob demanda, e a conversa virou a interface de qualquer coisa.

## O que existia antes

Computadores faziam exatamente o que um programa mandava. Para cada tarefa nova, alguém precisava escrever o programa. A pesquisa em IA existia desde os anos 1950, mas os sistemas eram estreitos: cada um sabia uma coisa.

## O salto

| Quando | O quê |
| --- | --- |
| 2017 | Pesquisadores do Google publicam o [Transformer](../../papers/2017-attention-is-all-you-need.pdf), a arquitetura de todos os grandes modelos atuais |
| 2020 | As [leis de escala](../../papers/2020-scaling-laws-for-neural-language-models.pdf) mostram que o erro cai de forma previsível com mais parâmetros, dados e computação |
| 2022 | A Anthropic publica a [Constitutional AI](../../papers/2022-constitutional-ai.pdf); em 30/11/2022, a OpenAI lança o ChatGPT |

O [caderno](../../notebook/README.pt-BR.md) deste repositório explica cada peça por dentro, com experimentos.

## A análise

- **O que ficou barato:** produzir texto, código, resumos e análises. Trabalho que levava horas de uma pessoa especializada passa a levar segundos e centavos.
- **A camada aberta:** parcialmente aberta. Os artigos de pesquisa foram publicados, existem modelos com pesos abertos, e protocolos abertos ligam modelos a ferramentas (o Model Context Protocol, publicado pela Anthropic em 2024). Mas os modelos mais capazes e a computação para treiná-los estão concentrados em poucas empresas.
- **A interface para as pessoas:** a conversa. O Transformer tinha 5 anos quando o chat o pôs na mão de qualquer pessoa.
- **O que ligou:** **o conhecimento escrito da humanidade a qualquer pergunta**, na língua de quem pergunta.
- **O lado ruim:** o modelo erra com confiança, o trabalho de muitas profissões muda de forma, e a concentração de computação dá poder a poucos. A conta de energia é grande e crescente.

## Fontes

- Os três artigos, em PDF: [`../../papers/`](../../papers/README.pt-BR.md)
- O lançamento do ChatGPT em 30/11/2022: <https://en.wikipedia.org/wiki/ChatGPT>
- O Model Context Protocol: <https://www.anthropic.com/news/model-context-protocol>

## Ligações

Padrões: [um custo despenca](../patterns/README.pt-BR.md#1-um-custo-despenca), [o salto acontece na interface](../patterns/README.pt-BR.md#4-o-salto-acontece-na-interface). Fronteira: [agentes que trabalham](../frontier/README.pt-BR.md#2-agentes-que-trabalham-pelas-pessoas), [o conhecimento na língua de cada um](../frontier/README.pt-BR.md#3-o-conhecimento-na-língua-de-cada-um).
