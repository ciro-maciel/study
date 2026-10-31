# Gradiente

[English](README.md) · [Caderno](../../README.pt-BR.md) · Anterior: [atenção](../attention/README.pt-BR.md) · Próximo: [treino](../training/README.pt-BR.md)

**Em uma frase:** o gradiente diz, para cada número do modelo, para que lado e com que força mexer nele para o erro cair; aprender é dar pequenos passos na direção contrária ao gradiente.

## Como funciona

O modelo tem 4.192 números (os parâmetros), e o erro depende de todos eles. A pergunta do treino é: se eu mexer um pouquinho neste número, o erro sobe ou desce, e quanto? Essa resposta é o gradiente daquele número.

Dá para descobrir no braço: mexer um número, recalcular o erro, ver a diferença. Mas seriam 4.192 recálculos a cada passo. O truque é a **retropropagação** (backpropagation): cada conta guarda de onde veio, e uma única volta de trás para frente calcula o gradiente de todos os números de uma vez, pela regra da cadeia.

No [microgpt](../../../microgpt/microgpt.py), isso é a `class Value` (linha 30). Cada soma, multiplicação ou potência cria um `Value` que lembra os seus "filhos" e a derivada local. O método `backward()` (linha 59) percorre esse grafo de trás para frente e preenche o `.grad` de cada número. Na linha 172, `loss.backward()` faz isso para o modelo inteiro, e na linha 181 cada parâmetro anda um passo contra o próprio gradiente.

## O que o artigo diz

O artigo do Transformer não explica a retropropagação; ela é tão básica que é pressuposta. O que ele diz é qual otimizador usa os gradientes:

> "We used the Adam optimizer [20] with β1 = 0.9, β2 = 0.98 and ε = 10^-9."
> (seção 5.3, página 7)

O microgpt usa o mesmo Adam (linhas 147 a 181), com outros valores (`beta1 = 0.85`, `beta2 = 0.99`). O Adam não anda direto na direção do gradiente: ele faz uma média dos gradientes recentes e ajusta o tamanho do passo de cada número, o que deixa o treino mais estável.

## O experimento

```bash
cd notebook/concepts/gradient
python3 gradient.py
```

O [`gradient.py`](gradient.py) usa a `class Value` do próprio microgpt, primeiro numa conta pequena, depois no modelo de verdade, sem treino nenhum. Num Mac com Python 3.15, em 31/10/2026, levou 21 segundos.

**1. Uma conta pequena:** `f = a × b + b²`, com `a = 2` e `b = -3`, dá `f = 3`.

| | df/da | df/db |
| --- | --- | --- |
| retropropagação (`backward()`) | -3,0 | -4,0 |
| no braço (mexer 0,000001 e medir) | -3,0000 | -4,0000 |

Os dois jeitos concordam. A retropropagação só é muito mais rápida: uma volta, em vez de uma conta por número.

**2. O modelo de verdade, uma palavra.** O modelo ainda sem treino erra `emma` com perda 3,4955. Uma única chamada de `backward()` calcula o gradiente dos 4.192 parâmetros: 3.616 deles saem diferentes de zero (os outros não participaram dessa palavra, como as linhas das letras que `emma` não tem). Depois, um passo contra o gradiente, de vários tamanhos:

| Tamanho do passo | perda em `emma` | perda em 200 outros nomes |
| --- | --- | --- |
| antes | 3,4955 | 3,2914 |
| 0,01 | 3,4256 (-0,07) | 3,2895 (-0,002) |
| 0,1 | 2,8610 (-0,63) | 3,2762 (-0,015) |
| 1 | 1,9234 (-1,57) | 3,2879 (-0,003) |
| 10 | **24,0197 (+20,52)** | **15,4791 (+12,19)** |

Três lições numa tabela:

- **O gradiente aponta o caminho.** Um passo pequeno contra ele sempre melhorou `emma`.
- **Aprender uma palavra ajuda pouco as outras.** Com passo 0,1, `emma` caiu 0,63, os outros nomes só 0,015. Com passo 1, `emma` caiu mais ainda, mas os outros quase não ganharam nada: o passo foi todo para decorar `emma`. Por isso o treino passa por milhares de palavras diferentes.
- **Passo grande demais destrói.** Com passo 10, o erro explode, em `emma` e em tudo. O gradiente diz a direção só ali perto; longe demais, ele não vale. Por isso o microgpt usa passos de 0,01 (linha 175) e os diminui até o fim do treino.

## Por que isso importa

- **É a única forma como o modelo aprende.** Nenhuma regra é escrita à mão: tudo o que as páginas anteriores mostraram (vogais, cabeças de atenção) saiu de milhões de passinhos como estes.
- **É por que treinar é caro.** Cada passo é uma ida (calcular o erro) e uma volta (calcular os gradientes) por todos os números. Num modelo grande, são centenas de bilhões de números, bilhões de vezes.
- **Explica "taxa de aprendizado".** É o tamanho do passo. O experimento mostra os dois jeitos de errar: pequena demais não sai do lugar, grande demais explode.

## O que dá para construir

- **Um "veja o modelo aprender" interativo.** Um controle deslizante para o tamanho do passo, e a pessoa vê o erro cair, estacionar ou explodir. A tabela acima, viva.
- **Intuição para quem decide.** Quem contrata IA ouve "precisamos de mais dados" e "mais treino". Saber que aprender é passo a passo, e que passo grande demais estraga, ajuda a fazer as perguntas certas.

## Perguntas em aberto

- Um passo melhora uma palavra. O que acontece quando se repete isso mil vezes, cada vez com um nome diferente? → **treino**, a próxima página.
- O Adam ajusta o passo de cada número. Quanto pior fica o microgpt com o passo simples, sem Adam?
