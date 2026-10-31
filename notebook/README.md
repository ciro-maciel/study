# The notebook

[Português](README.pt-BR.md) · [Repository](../README.md)

A study notebook about artificial intelligence, kept by two minds, so to speak: **Ciro Cesar Maciel**, who asks, runs the experiments and decides what is worth it, and **Claude**, who writes the pages, links them to each other and keeps them current. It answers three questions: what AI is, how it works on the inside, and what we can build with it.

One honest note about Claude: it does not learn between conversations. Every session starts from zero. What accumulates is what is written here, and that is why this notebook exists: it is the memory that lets us pick up where we left off.

## How it works

| Layer | What it is | Who writes it |
| --- | --- | --- |
| **Sources** | The code and papers in [`../microgpt/`](../microgpt/) and [`../papers/`](../papers/), always unchanged | the original authors |
| **Pages** | One concept per folder in [`concepts/`](concepts/), with an explanation, the passage from the paper, an experiment that runs in under a minute, why it matters and what we can build | Claude, from Ciro's questions |
| **Rules** | How the notebook is kept, in [`../AGENTS.md`](../AGENTS.md) | both, adjusted over time |

And two files that grow every session:

- [`log.md`](log.md): what was done and when, one line per event.
- [`predictions.md`](predictions.md): what we think AI will do, with a date, to check later.

**Each session:** pick the next concept on the ladder, read the page, run the experiment, ask. Every good question becomes part of a page or a new page instead of getting lost in the chat. Every so often, an **audit**: what went stale, what contradicts something else, what is mentioned but has no page yet.

## The ladder

From the smallest concept to the largest, each one standing on the one before.

| | Concept | Source | Page |
| --- | --- | --- | --- |
| 1 | **Token**: how text becomes numbers | microgpt · Transformer, sections 3.4 and 5.1 | [ready](concepts/token/README.md) |
| 2 | **Embedding**: how a number gains meaning | microgpt · Transformer, section 3.4 | next |
| 3 | **Attention**: how each word looks at the others | microgpt · Transformer, section 3.2 | |
| 4 | **Gradient**: how a number learns | microgpt (`class Value`) | |
| 5 | **Training**: the loop of predicting, missing and adjusting | microgpt | |
| 6 | **Scale**: why bigger gets better, and how far | Scaling Laws | |
| 7 | **From model to assistant**: fine-tuning and preferences | Constitutional AI | |
| 8 | **Written principles**: the constitution | Constitutional AI | |
| 9 | **Agents**: the model that uses tools | | |

The ladder is not fixed: a good question along the way can become a new rung.
