# A empresa de uma pessoa

[English](2026-10-31-the-one-person-company.md) · [Teses](README.pt-BR.md)

- **Data:** 31 de outubro de 2026
- **Autores:** Ciro Cesar Maciel e Claude (Opus 5.5)
- **Estado:** aberta. Será revista depois das quatro primeiras semanas de operação da empresa de prova.

## A tese em uma frase

**Nos próximos anos, a unidade de produção deixa de ser a empresa com muitos funcionários e passa a ser a pessoa com muitos agentes; o que precisamos criar é a empresa de uma pessoa, completa e em português, guiada por princípios que o dono escreve, junto com a escola que ensina a tocá-la.**

## Em que momento estamos

Em 1776, Adam Smith publicou [*A Riqueza das Nações*](../books/the-wealth-of-nations/README.pt-BR.md) mostrando que a riqueza vem da divisão do trabalho. Dez pessoas, cada uma fazendo uma parte, produziam mais de 48 mil alfinetes por dia; sozinhas, talvez nem vinte cada (livro I, capítulo 1). E ele apontou a terceira razão desse ganho: as máquinas que "enable one man to do the work of many". Nas décadas seguintes, o trabalho físico ficou barato e o mundo mudou de forma.

Estamos no mesmo ponto, agora para o trabalho intelectual: escrever, analisar, programar, atender, planejar. A diferença é a velocidade. A Revolução Industrial levou gerações; esta está levando anos.

## O que os textos deste repositório dizem juntos

| Texto | O que diz | O que significa agora |
| --- | --- | --- |
| [Smith](../books/the-wealth-of-nations/README.pt-BR.md), livro I, capítulo 3 | A divisão do trabalho é limitada pelo tamanho do mercado | Esse limite está sendo derrubado: uma pessoa sozinha já pode ter uma divisão de trabalho inteira, feita por agentes. A fábrica de alfinetes cabe dentro de uma pessoa |
| [Leis de escala](../papers/2020-scaling-laws-for-neural-language-models.pdf) (2020) | O erro de um modelo cai de forma previsível com mais parâmetros, dados e computação | Os modelos vão continuar melhorando, e dá para planejar contando com isso: quem constrói hoje deve construir para o modelo do ano que vem |
| [Transformer](../papers/2017-attention-is-all-you-need.pdf) (2017) e o [microgpt](../microgpt/README.pt-BR.md) | O algoritmo inteiro de um GPT cabe em 199 linhas; "todo o resto é só eficiência" | O algoritmo não é mais a vantagem de ninguém. Treinar modelo próprio é jogo de quem tem bilhões em computação; a vantagem está em outro lugar |
| [Constitutional AI](../papers/2022-constitutional-ai.pdf) (2022) | O comportamento de um modelo pode ser guiado por uma lista de princípios escritos | Quem escreve os princípios define o que a máquina faz. O poder novo é de quem sabe dizer, em palavras, como o trabalho deve ser feito |
| Smith, livro V, capítulo 1 | A divisão do trabalho pode embrutecer quem a vive; o remédio é educação pública, "a little school" em cada paróquia | O risco se repete: pessoas que delegam tudo à IA e param de pensar. O remédio continua o mesmo: ensinar |
| Uma medição nossa, em 31/10/2026 | O mesmo texto custa 16% mais tokens em português do que em inglês no tokenizador do Claude | Quem pensa em português chega ao salto pagando mais e achando menos. É um mercado ainda mal servido |

## O que acreditamos que temos que criar

Uma coisa só, feita de quatro peças:

1. **A fábrica.** Uma pessoa, com um agente para cada departamento (vendas, marketing, atendimento, finanças, produto), cada um com uma métrica, um ritmo e uma lista do que precisa de aprovação. O dono decide, aprova e confere; não faz o trabalho no lugar deles.
2. **A constituição de cada negócio.** O dono escreve, na língua dele, os princípios do próprio negócio: o que a empresa é, o que nunca dizer, o que pode prometer, até quanto pode dar de desconto, quando devolver dinheiro, quando chamar o dono. Os agentes trabalham dentro disso, e todo texto que sai é conferido contra isso antes de sair.
3. **A memória do negócio.** O que foi decidido, aprendido e combinado não se perde de uma conversa para outra. É o que Vannevar Bush imaginou em 1945, agora dentro de cada empresa.
4. **A escola.** A "little school" de Smith em versão de hoje: o que todo mundo precisa saber de IA para trabalhar e para dirigir agentes sem perder o próprio julgamento.

As peças técnicas já existem. O que falta é juntá-las numa coisa só e provar que funciona numa empresa de verdade.

## O próximo passo da empresa autônoma

**Provar numa empresa real, com resultado voltado ao cliente, antes de oferecer a qualquer outra pessoa.** A empresa de prova é uma loja real de receitas, de uma dona que não é técnica.

**Semana 0: a loja precisa conseguir vender.** Nenhum agente melhora uma loja que não consegue receber um pagamento ou entregar o que vendeu. Antes de ligar a equipe:

- o pagamento ligado à conta real da dona;
- o arquivo de entrega em cada produto;
- o caminho do cliente até a loja (a rede social leva à loja, não a outro lugar);
- uma compra real de ponta a ponta, do pagamento ao arquivo no e-mail do comprador.

**A constituição.** A dona escreve a dela, a partir dos princípios que a casa já publica, mais as regras de ação. É a parte que só ela pode fazer.

**Quatro semanas com cinco agentes:**

| Agente | O que é dele | A métrica |
| --- | --- | --- |
| Diretor de operações | a empresa andando, cada entrega com um dono | entregas no prazo |
| Orgânico | a rede social | cliques para a loja |
| SEO | as receitas achadas na busca | visitas vindas da busca |
| Atendimento | quem comprou e quem tem dúvida | tempo de resposta |
| Financeiro | vendas, taxas e o placar | vendas por semana |

**O placar, toda sexta:** vendas; entregas no prazo; tarefas que começaram sem a dona pedir; aprovações que ela deu; erros, e o que mudou na constituição por causa deles.

**O que sai da prova:** o caminho para qualquer pessoa montar a própria empresa (escolher o negócio, escrever a constituição, a equipe nasce); o livro sobre a empresa de uma pessoa, com cena, prova e limite reais; e a história contada com os números.

## O que não criar

- **Um modelo próprio:** as leis de escala dizem que esse jogo é de quem tem computação.
- **Mais um feed que captura atenção:** é o lado ruim das redes sociais, e o mundo já tem o bastante.
- **Agente que age sem princípios escritos e sem alguém conferindo:** é o erro que derruba a confiança de todo o resto.

## O papel de cada um

- **Ciro:** o dono da fábrica. Escolhe o que construir, escreve (ou ajuda o dono a escrever) os princípios e ensina as pessoas. São as três coisas que a máquina não faz por ninguém.
- **Claude:** os trabalhadores da fábrica. Executa, critica o próprio trabalho à luz dos princípios e mantém a memória em dia. Com uma honestidade: não lembra entre conversas. Por isso a memória escrita não é detalhe; é o que permite trabalhar junto.

## O que derrubaria esta tese

- Os erros dos agentes no mundo real (dinheiro, clientes, dados) ficarem caros demais para compensar o tempo poupado.
- As pessoas preferirem continuar contratando pessoas para tudo, mesmo com a máquina mais barata.
- Os grandes laboratórios entregarem sozinhos a empresa completa, na língua de cada um, antes de qualquer outro.
- Na prova: depois de quatro semanas vendendo de verdade, a dona continuar fazendo o trabalho em vez de aprovar, ou nenhuma tarefa começar sem ela.
