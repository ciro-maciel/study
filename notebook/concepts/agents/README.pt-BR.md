# Agentes

[English](README.md) · [Caderno](../../README.pt-BR.md) · Anterior: [constituição](../constitution/README.pt-BR.md) · Fim da escada

**Em uma frase:** um agente é um modelo de linguagem dentro de um laço: em vez de só responder, ele pode pedir que um programa rode uma ferramenta, ler o resultado e decidir o próximo passo, até terminar a tarefa.

## Como funciona

Tudo o que as páginas anteriores mostraram termina num modelo que gera texto, um token por vez. Ele não consegue, sozinho, contar os nomes de uma planilha, abrir um site ou mandar um e-mail. O que ele consegue é **escrever um pedido** num formato combinado.

O laço do agente tem quatro passos:

1. **A pessoa pede** alguma coisa.
2. **O modelo decide.** Ou responde direto, ou escreve um pedido de ferramenta: o nome da ferramenta e os argumentos (`tool_use`).
3. **O programa executa.** Não é o modelo que roda a ferramenta: é o programa em volta dele, que pode recusar, pedir confirmação ou registrar tudo. O resultado volta para a conversa (`tool_result`).
4. **Repete** até o modelo responder em texto, sem pedir mais nada.

É exatamente o formato da API do Claude: o modelo devolve um bloco `tool_use`, o programa responde com um bloco `tool_result`, e a conversa continua.

## De onde vem

A escada até aqui se apoiou nos três artigos da pasta [`papers/`](../../../papers/README.pt-BR.md). Agentes não têm um artigo fundador entre eles: é uma forma de **usar** o modelo, não de construí-lo. O que torna o laço possível são as páginas anteriores juntas: o [treino](../training/README.pt-BR.md) dá ao modelo o conhecimento, o [ajuste fino](../fine-tuning/README.pt-BR.md) ensina o formato de pedir uma ferramenta, e a [constituição](../constitution/README.pt-BR.md) ajuda a decidir quando um pedido é aceitável.

## O experimento

```bash
cd notebook/concepts/agents
python3 agent.py
```

O [`agent.py`](agent.py) monta o laço completo com duas ferramentas sobre os 32.033 nomes do microgpt: `count_names` (conta os nomes que começam com um prefixo) e `longest_name` (devolve o mais longo). Uma honestidade importante: **o modelo aqui é um dublê**, uma função (`decide()`) que segue um plano fixo, para o laço rodar sem internet e sem custo. As mensagens têm o mesmo formato das do Claude; trocar `decide()` por uma chamada a um modelo de verdade não muda o resto do programa. Num Mac com Python 3.15, em 31/10/2026, levou menos de um segundo.

```
user: How many names start with 'ka', and which is the longest?
model asks for a tool: {"name": "count_names", "input": {"prefix": "ka"}}
the program runs it and answers: 1254
model asks for a tool: {"name": "longest_name", "input": {"prefix": "ka"}}
the program runs it and answers: "kamsiyochukwu"
model: 1254 names start with 'ka'; the longest is kamsiyochukwu.
6 messages, 2 tool calls
```

O que o experimento mostra:

- **O modelo não conta nada.** Os números (1.254 e "kamsiyochukwu") vêm do programa. O modelo só decide o que pedir e como juntar as respostas. É por isso que um agente acerta contas que o modelo sozinho erraria: lembre que ele [nem vê as letras](../token/README.pt-BR.md).
- **Quem executa é o programa.** Entre o pedido e a execução há uma linha de código que pode dizer não. É ali que moram a segurança e as permissões de um agente.
- **A resposta final sai do histórico.** Na terceira volta, o modelo responde lendo os dois resultados que estão na conversa.

**Para experimentar:** acrescente uma terceira ferramenta em `TOOLS` (por exemplo, a lista dos nomes com um prefixo) e um terceiro passo em `decide()` que a use.

## Por que isso importa

- **É onde a IA sai do texto e vai para o trabalho.** Consultar um sistema, preencher um formulário, mexer num arquivo: tudo isso é um modelo pedindo ferramentas num laço.
- **Separa o que o modelo sabe do que ele faz.** O conhecimento vem do treino; a ação vem das ferramentas que alguém decidiu dar a ele. Um agente é tão útil e tão seguro quanto as ferramentas e as regras do laço.
- **Muda o que vale a pena construir.** Em vez de um modelo melhor, muitas vezes o que falta é a ferramenta certa e um laço bem cuidado.

## O que dá para construir

- **Ferramentas pequenas e honestas.** Cada ferramenta faz uma coisa, com nome e descrição claros, e devolve um resultado verificável, como as duas deste experimento. É o que deixa o modelo acertar.
- **O laço com um modelo de verdade.** O próximo passo natural deste caderno é trocar `decide()` por uma chamada ao Claude, com as mesmas duas ferramentas, e comparar: o modelo de verdade escolhe as mesmas ferramentas que o dublê? Isso gasta tokens, então pede uma decisão antes.
- **Agentes com constituição.** Juntar esta página com a anterior: o laço do agente, com uma lista de princípios que o programa confere antes de executar cada ferramenta.

## Perguntas em aberto

- O dublê sabe a ordem certa das ferramentas porque alguém escreveu o plano. Um modelo de verdade, recebendo só as descrições de `TOOLS`, chegaria no mesmo plano?
- Onde fica o limite entre o que o programa deve conferir antes de executar e o que pode deixar o modelo decidir?

Esta é a última página da escada. As próximas nascem das perguntas em aberto de todas elas.
