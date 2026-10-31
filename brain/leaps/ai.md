# Artificial intelligence (2017 to 2022, under way)

[Português](ai.pt-BR.md) · [Brain](../README.md) · Previous: [social networks](social-networks.md) · Next: [robots](robots.md)

**In one sentence:** language models are making it cheap to produce text, code and reasoning on demand, and conversation has become the interface to anything.

## What existed before

Computers did exactly what a program told them. For each new task, someone had to write the program. AI research had existed since the 1950s, but the systems were narrow: each one knew one thing.

## The leap

| When | What |
| --- | --- |
| 2017 | Google researchers publish the [Transformer](../../papers/2017-attention-is-all-you-need.pdf), the architecture of every large model today |
| 2020 | The [scaling laws](../../papers/2020-scaling-laws-for-neural-language-models.pdf) show the error falls predictably with more parameters, data and compute |
| 2022 | Anthropic publishes [Constitutional AI](../../papers/2022-constitutional-ai.pdf); on 30 Nov 2022, OpenAI launches ChatGPT |

This repository's [notebook](../../notebook/README.md) explains each piece from the inside, with experiments.

## The analysis

- **What became cheap:** producing text, code, summaries and analyses. Work that took a specialist hours now takes seconds and cents.
- **The open layer:** partly open. The research papers were published, there are models with open weights, and open protocols connect models to tools (the Model Context Protocol, published by Anthropic in 2024). But the most capable models and the compute to train them are concentrated in a few companies.
- **The interface for people:** conversation. The Transformer was 5 years old when chat put it in anyone's hands.
- **What it connected:** **humanity's written knowledge to any question**, in the asker's language.
- **The bad side:** models are confidently wrong, the work of many professions changes shape, and concentrated compute gives power to few. The energy bill is large and growing.

## Sources

- The three papers, as PDFs: [`../../papers/`](../../papers/README.md)
- The launch of ChatGPT on 30 November 2022: <https://en.wikipedia.org/wiki/ChatGPT>
- The Model Context Protocol: <https://www.anthropic.com/news/model-context-protocol>

## Links

Patterns: [a cost collapses](../patterns/README.md#1-a-cost-collapses), [the leap happens at the interface](../patterns/README.md#4-the-leap-happens-at-the-interface). Frontier: [agents that work](../frontier/README.md#2-agents-that-work-for-people), [knowledge in everyone's language](../frontier/README.md#3-knowledge-in-everyones-language).
