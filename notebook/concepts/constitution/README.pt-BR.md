# Princípios escritos: a constituição

[English](README.md) · [Caderno](../../README.pt-BR.md) · Anterior: [ajuste fino](../fine-tuning/README.pt-BR.md) · Próximo: [agentes](../agents/README.pt-BR.md)

**Em uma frase:** na Constitutional AI, em vez de pessoas marcarem cada resposta ruim, o comportamento do modelo é guiado por uma lista curta de princípios escritos; o modelo gera, critica o que gerou à luz dos princípios, revisa, e é treinado nas próprias revisões.

## Como funciona

Para ensinar um assistente a não causar dano, o caminho óbvio é pedir a milhares de pessoas que leiam respostas e marquem as ruins. Funciona, mas é caro, lento, e o critério fica espalhado na cabeça de cada avaliador.

A Constitutional AI troca isso por um documento: a **constituição**, uma lista de princípios em linguagem comum. A fase supervisionada tem quatro passos:

1. **Gerar.** O modelo responde a pedidos, inclusive os difíceis.
2. **Criticar.** O próprio modelo relê a resposta e aponta onde ela fere um princípio.
3. **Revisar.** O modelo reescreve a resposta para respeitar o princípio.
4. **Ajustar.** O modelo original é treinado nas respostas revisadas: o [ajuste fino](../fine-tuning/README.pt-BR.md) da página anterior, agora com exemplos que o próprio modelo produziu.

Depois vem uma segunda fase, por preferências, em que um modelo compara pares de respostas com base nos princípios.

## O que o artigo diz

No [artigo da Constitutional AI](../../../papers/2022-constitutional-ai.pdf):

> "The only human oversight is provided through a list of rules or principles, and so we refer to the method as 'Constitutional AI'."
> (resumo, página 1)

> "In the supervised phase we sample from an initial model, then generate self-critiques and revisions, and then finetune the original model on revised responses."
> (resumo, página 1)

A figura 1, na página 2, desenha as duas fases.

## O experimento

```bash
cd notebook/concepts/constitution
python3 constitution.py
```

O [`constitution.py`](constitution.py) refaz a fase supervisionada no microgpt, com uma constituição de dois princípios para nomes:

1. no máximo 6 letras;
2. não termina em "n".

Uma diferença precisa ficar clara: no artigo, quem critica e revisa é o próprio modelo, que lê os princípios. O microgpt não lê; então o crítico e o revisor aqui são duas regras em Python. O revisor corta o nome em 6 letras e troca um "n" final por "a". Os três passos e o ajuste final são os do artigo; o crítico é que é de mentira.

Num Mac com Python 3.15, em 31/10/2026, levou 65 segundos.

| Modelo | ferem um princípio | nomes diferentes em 300 | exemplos |
| --- | --- | --- | --- |
| base | 40% | 266 | `kamon ann karai jaire vialan karia yeran anna` |
| depois de 300 passos nas próprias revisões | **0%** | **77** | `anaa ana anar anaa anelia anahe karaa aria` |
| depois de 60 passos | 2% | 128 | `jana jana karia laraa keara kara lelara elala` |

Algumas críticas e revisões: `kamon → kamoa`, `ann → ana`, `vialan → vialaa`, `yeran → yeraa` (todas por terminar em "n").

O que a tabela mostra:

- **Funciona.** Sem ninguém marcar um nome sequer, só com dois princípios escritos e as próprias revisões, as violações caíram de 40% para 0%.
- **Tem preço.** O modelo passou a gerar só 77 nomes diferentes em 300, e muitos estranhos (`anaa`, `karaa`). Ele aprendeu as manias do revisor: o atalho mais seguro para nunca terminar em "n" foi gerar quase tudo em "a".
- **A dose decide.** Com 60 passos em vez de 300, as violações ficam em 2% e a variedade sobe para 128. Obedecer mais custou criatividade; obedecer um pouco menos devolveu parte dela.

É a mesma tensão que o artigo enfrenta em escala: um assistente que, para não causar dano, se recusa a tudo é seguro e inútil. O artigo chama o objetivo de "harmless but non-evasive", inofensivo mas sem fugir da pergunta, e é por isso que a segunda fase também recompensa respostas úteis.

**Para experimentar:** troque `lab.train(ns, revised, 300)` por outro número de passos, ou mude o revisor do segundo princípio (`n[:-1] + 'a'`) para outra correção, e veja o que acontece com a variedade.

## Por que isso importa

- **Os princípios ficam à vista.** Em vez de um critério escondido em milhares de marcações, há um texto que qualquer um pode ler, discutir e mudar. É por isso que o método é o mais característico do Claude.
- **Escala sem multidão.** O modelo critica e revisa a si mesmo, então o treino de comportamento não depende de pessoas lendo respostas ruins o dia todo.
- **O revisor é metade do resultado.** O experimento mostra que um revisor ruim ensina manias ruins. A qualidade da crítica e da revisão define o modelo que sai.

## O que dá para construir

- **Constituição para os próprios agentes.** Um agente de atendimento, de vendas ou de saúde pode ter a sua lista curta de princípios, escrita pelo dono do negócio, usada para criticar e revisar cada resposta antes de ela sair. Sem treinar modelo nenhum: o ciclo de criticar e revisar já funciona com um modelo grande lendo o texto.
- **Medir obediência e variedade juntas.** Toda regra nova num agente deveria vir com as duas medidas do experimento: quantas respostas ainda ferem a regra e quanto a variedade e a utilidade caíram.

## Perguntas em aberto

- Até aqui, o modelo só gera texto. Como ele passa a fazer coisas no mundo, como consultar dados ou rodar um programa? → **agentes**, a próxima página.
- O que acontece se o revisor for o próprio microgpt, escolhendo entre vários nomes gerados o primeiro que respeita os princípios, em vez de corrigir à força?
