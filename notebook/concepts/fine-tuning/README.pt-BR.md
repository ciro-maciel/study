# Do modelo ao assistente: ajuste fino

[English](README.md) · [Caderno](../../README.pt-BR.md) · Anterior: [escala](../scale/README.pt-BR.md) · Próximo: [constituição](../constitution/README.pt-BR.md)

**Em uma frase:** ajuste fino é continuar treinando um modelo já pronto, por poucos passos, num conjunto pequeno e escolhido de exemplos; é assim que um modelo que só completa texto vira um assistente que responde do jeito certo.

## Como funciona

O pré-treino (a página do [treino](../training/README.pt-BR.md)) ensina o modelo a continuar qualquer texto. Ele sabe muito, mas não sabe o que se espera dele: perguntado "qual a capital da França?", um modelo base pode continuar com outra pergunta, porque listas de perguntas também existem na internet.

O ajuste fino usa **o mesmo laço**, com três diferenças:

- **parte de um modelo treinado**, não de números sorteados;
- **usa poucos exemplos, escolhidos a dedo** (conversas boas, respostas no formato certo);
- **dá poucos passos**, para mudar o comportamento sem apagar o que o modelo já sabe.

Depois disso, os assistentes de hoje passam por uma segunda etapa, por **preferências**: o modelo gera duas respostas, alguém (uma pessoa ou outro modelo) diz qual é melhor, e o treino empurra o modelo para o lado das preferidas.

## O que o artigo diz

No [artigo da Constitutional AI](../../../papers/2022-constitutional-ai.pdf), as duas etapas aparecem já no resumo:

> "In the supervised phase we sample from an initial model, then generate self-critiques and revisions, and then finetune the original model on revised responses. In the RL phase, we sample from the finetuned model, use a model to evaluate which of the two samples is better, and then train a preference model from this dataset of AI preferences."
> (resumo, página 1)

A primeira frase é ajuste fino; a segunda é o aprendizado por preferências. A próxima página, [constituição](../constitution/README.pt-BR.md), refaz a primeira em miniatura.

## O experimento

```bash
cd notebook/concepts/fine-tuning
python3 fine_tuning.py
```

O [`fine_tuning.py`](fine_tuning.py) treina o microgpt nos 1.000 passos de sempre (o "modelo base") e depois faz dois ajustes finos de 150 passos, cada um partindo do mesmo modelo base:

- **só nomes com z:** dos 895 nomes começados por "z" que o modelo base não viu, os 150 primeiros, um por passo;
- **metade z, metade outros:** 75 desses nomes com "z", intercalados com 75 nomes comuns.

Num Mac com Python 3.15, em 31/10/2026, levou 80 segundos.

| Modelo | nomes gerados que começam com z | perda em 200 nomes comuns |
| --- | --- | --- |
| base | 1,5% | 2,343 |
| ajuste só com z | **100%** | **3,581** |
| ajuste metade z, metade outros | **92%** | **2,501** |

Nomes gerados depois do ajuste só com z: `zayai zali zon zaylye zania zaren zailyn zarie zaha zadiri`.

O que a tabela mostra:

- **Poucos passos mudam muito.** 150 passos (15% do treino original) levaram os nomes com "z" de 1,5% para 100%.
- **Ajustar demais apaga o resto.** Depois do ajuste só com "z", a perda nos nomes comuns foi a 3,58, **pior do que chutar ao acaso** (3,30). O modelo não ficou "especializado": esqueceu como são os outros nomes. Isso tem nome: **esquecimento catastrófico**.
- **Misturar protege.** Com metade de nomes comuns no ajuste, o modelo ainda gera 92% de nomes com "z" e a perda nos comuns fica em 2,50, perto da base. É por isso que o ajuste fino de verdade mistura os exemplos novos com dados gerais.

**Para experimentar:** troque todas as ocorrências de `'z'` em `fine_tuning.py` por outra letra e veja se a mesma história se repete.

## Por que isso importa

- **É o que faz o assistente.** O mesmo modelo base pode virar um assistente educado, um programador ou um tradutor, conforme os exemplos do ajuste.
- **Explica um risco.** Ajustar um modelo em dados muito estreitos pode deixá-lo pior em todo o resto, e isso não aparece se só se testar o caso novo. O experimento só viu o problema porque mediu também os nomes comuns.
- **Mostra o poder de poucos exemplos.** 150 nomes mudaram o comportamento de um modelo treinado em 1.000. Num modelo grande, alguns milhares de conversas bem escolhidas mudam o jeito de responder de um modelo treinado em trilhões de tokens.

## O que dá para construir

- **Antes de ajustar, medir o que se pode perder.** Qualquer ajuste de um modelo, ou mesmo de um prompt, para um caso novo precisa de uma bateria dos casos antigos rodando junto. O experimento mostra o porquê em números.
- **Exemplos são o produto.** Num ajuste fino, o que define o resultado é a escolha dos exemplos. Uma boa coleção de exemplos de um ofício (atendimento de uma clínica, respostas de uma loja) vale mais do que o modelo escolhido.

## Perguntas em aberto

- No experimento, alguém escolheu os nomes com "z". E se o próprio modelo gerasse os exemplos, um crítico apontasse o que viola uma regra e um revisor corrigisse? → **constituição**, a próxima página.
- Quantos passos de ajuste só com "z" são precisos para a perda nos nomes comuns passar de 3,30?
