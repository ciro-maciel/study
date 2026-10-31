# Treino

[English](README.md) · [Caderno](../../README.pt-BR.md) · Anterior: [gradiente](../gradient/README.pt-BR.md) · Próximo: [escala](../scale/README.pt-BR.md)

**Em uma frase:** treinar é repetir milhares de vezes o mesmo laço (pegar um exemplo, prever, medir o erro, dar um passo contra o gradiente) até o modelo errar pouco em textos que ele nunca viu.

## Como funciona

O laço do [microgpt](../../../microgpt/microgpt.py) começa na linha 152 e tem quatro partes:

1. **Pegar um exemplo.** Um nome por passo, cercado pelo token de início e fim.
2. **Prever.** Para cada posição, o modelo dá uma probabilidade a cada uma das 27 opções de próxima letra.
3. **Medir o erro.** A perda de cada posição é `-log(probabilidade da letra certa)` (linha 167): se o modelo deu 100% à letra certa, a perda é 0; se deu quase nada, a perda é grande. A perda do nome é a média.
4. **Ajustar.** `loss.backward()` (linha 172) calcula os gradientes e o Adam dá o passo (linha 181), com um tamanho que diminui até o fim (linha 175).

Dois números ajudam a ler a perda:

- **Chute ao acaso.** Se o modelo desse a mesma chance às 27 opções, a perda seria `ln(27) = 3,30`. É o ponto de partida de quem não sabe nada.
- **Perda em nomes nunca vistos.** É o número que importa. Errar pouco nos nomes do treino pode ser só decoreba; errar pouco nos outros é aprender.

## O que o artigo diz

O [artigo do Transformer](../../../papers/2017-attention-is-all-you-need.pdf) conta quanto custou o treino do modelo dele:

> "We trained our models on one machine with 8 NVIDIA P100 GPUs. For our base models using the hyperparameters described throughout the paper, each training step took about 0.4 seconds. We trained the base models for a total of 100,000 steps or 12 hours."
> (seção 5.2, página 7)

O mesmo laço, em outra escala: 100 mil passos em 8 placas de vídeo, contra os 1.000 passos do microgpt num processador comum.

## O experimento

```bash
cd notebook/concepts/training
python3 training.py
```

O [`training.py`](training.py) gera nomes antes de treinar, treina pelos 1.000 passos guardando a perda de cada um, mede em 200 nomes que o modelo nunca viu e gera nomes de novo. Num Mac com Python 3.15, em 31/10/2026, levou 50 segundos.

**Antes do treino** (os números ainda são sorteados): `orgzqpdlw ptoabqmofyoqzxck eaktbsuhu zqcizclxmzgziotw qmcnezp hsentvzrknoqrvcl`. Letras ao acaso, tamanhos ao acaso.

**A perda, em média a cada 100 passos:**

| Passos | Perda média |
| --- | --- |
| chute ao acaso | 3,30 |
| 1 a 100 | 2,77 |
| 101 a 200 | 2,53 |
| 201 a 300 | 2,46 |
| 301 a 400 | 2,44 |
| 401 a 500 | 2,46 |
| 501 a 600 | 2,42 |
| 601 a 700 | 2,41 |
| 701 a 800 | 2,39 |
| 801 a 900 | 2,33 |
| 901 a 1.000 | 2,28 |
| **200 nomes nunca vistos** | **2,34** |

**Depois do treino:** `dalian marian karin malin ariana alona elanon jaran`.

O que a tabela mostra:

- **A maior parte vem no começo.** Os primeiros 100 passos já tiram o modelo do chute (3,30 para 2,77). Depois, cada centena de passos ganha pouco.
- **Não cai em linha reta.** Entre os passos 301 e 500 a perda até sobe um pouco: cada passo olha um nome só, e alguns nomes são mais difíceis que outros.
- **Ele aprendeu, não decorou.** A perda nos nomes nunca vistos (2,34) fica perto da perda dos últimos passos de treino (2,28). Se tivesse decorado, a diferença seria grande.

Os nomes gerados aqui são diferentes dos do [guia do microgpt](../../../microgpt/README.pt-BR.md), porque gerar nomes antes do treino consome números aleatórios; o modelo treinado é o mesmo.

## Por que isso importa

- **É o que separa um modelo base de um sorteio.** Todo modelo de linguagem passou por este laço, com trilhões de tokens em vez de mil nomes.
- **Explica o que é "pré-treino".** Prever o próximo token em muito texto, sem ninguém dizer o que é certo além do próprio texto. O microgpt faz exatamente isso, em miniatura.
- **Dá o critério certo para julgar.** Um modelo se avalia no que ele não viu. Em qualquer uso de IA, a pergunta é a mesma: funciona nos casos novos ou só nos exemplos?

## O que dá para construir

- **Uma "aula de treino" ao vivo.** O laço rodando na tela, nomes ao acaso virando nomes plausíveis em menos de um minuto. É o experimento mais convincente para alguém que nunca viu um modelo aprender.
- **O hábito de separar exemplos de teste.** Antes de dizer que um agente ou um prompt "funciona", guardar casos que ele nunca viu e medir neles, do mesmo jeito que os 200 nomes deste experimento.

## Perguntas em aberto

- A perda parou em torno de 2,3. É limite do modelo ou dos dados? O que acontece com um modelo maior? → **escala**, a próxima página.
- Quanto a perda dos nomes nunca vistos melhora com 3.000 passos em vez de 1.000?
