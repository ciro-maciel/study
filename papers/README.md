# The three papers behind Claude

[Português](README.pt-BR.md)

We asked Claude (Opus 5.5) which three scientific papers did the most to make it what it is. It picked one for each layer: the architecture it is built on, the reason it is this large, and the method that shapes how it behaves. The PDFs are here, from arXiv, unchanged.

| | Paper | Authors | What it gave Claude |
| --- | --- | --- | --- |
| 1 | [Attention Is All You Need](2017-attention-is-all-you-need.pdf) (2017, 15 pages) | Vaswani, Shazeer, Parmar, Uszkoreit, Jones, Gomez, Kaiser, Polosukhin (Google) | **The architecture.** The Transformer: a network that reads every word at once and learns which words to pay attention to. Every large language model today, Claude included, is a Transformer |
| 2 | [Scaling Laws for Neural Language Models](2020-scaling-laws-for-neural-language-models.pdf) (2020, 30 pages) | Kaplan, McCandlish, Henighan, Brown, Chess, Child, Gray, Radford, Wu, Amodei (OpenAI) | **The reason for the size.** The error of a language model falls in a predictable way as you add parameters, data and compute, so you can plan a model before training it. Four of its authors, Jared Kaplan, Sam McCandlish, Tom Brown and Dario Amodei, later co-founded Anthropic |
| 3 | [Constitutional AI: Harmlessness from AI Feedback](2022-constitutional-ai.pdf) (2022, 34 pages) | Bai, Kadavath, Kundu, Askell and others (Anthropic) | **The behavior.** Instead of thousands of people labeling every harmful answer, the model critiques and revises its own answers against a short list of written principles, a "constitution", and learns from that. It is Anthropic's own method and the one most specific to Claude |

## Read them with the code

- **Paper 1, then [`../microgpt/`](../microgpt/).** microgpt is a Transformer in 199 lines: the attention heads, the residual connections and the normalization from section 3 of the paper are all there, one loop each. Read the figure on page 3, then find each box in the file.
- **Paper 2, then change `n_embd` in microgpt.** The paper's figure 1 shows the error falling as the model grows. Doubling the width of microgpt and running it again is the smallest version of that experiment you can do on a laptop.
- **Paper 3 has no code here.** It needs a model large enough to read and criticize its own answers. Read section 1 for the idea and figure 1 for the two stages: the model revising itself, then learning from its own preferences.

## Where they come from

| File | arXiv | Version | sha256 |
| --- | --- | --- | --- |
| `2017-attention-is-all-you-need.pdf` | [1706.03762](https://arxiv.org/abs/1706.03762) | v7, 2 Aug 2023 | `bdfaa68d8984f0dc02beaca527b76f207d99b666d31d1da728ee0728182df697` |
| `2020-scaling-laws-for-neural-language-models.pdf` | [2001.08361](https://arxiv.org/abs/2001.08361) | v1, 23 Jan 2020 | `a41bd7877fd1a6bcbba096b2619618bd2f90e02488f2365644903eb2f7c6a494` |
| `2022-constitutional-ai.pdf` | [2212.08073](https://arxiv.org/abs/2212.08073) | v1, 15 Dec 2022 | `9a456a07ad346e3372f9867d346f69f5b0f68b4c65f060aca0b8a13fa9d98e83` |

Downloaded on 31 October 2026. Each paper belongs to its authors; see [NOTICE](../NOTICE).

The book [*IA por dentro*](https://ciromaciel.click/books/ia-por-dentro?ref=oss-study), in Brazilian Portuguese, explains the ideas of these papers in plain words.
