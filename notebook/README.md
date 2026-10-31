# The notebook

[Português](README.pt-BR.md) · [Repository](../README.md)

A study notebook about artificial intelligence, kept by two minds, so to speak: **Ciro Cesar Maciel**, who asks, runs the experiments and decides what is worth it, and **Claude**, who writes the pages, links them to each other and keeps them current. It answers three questions: what AI is, how it works on the inside, and what we can build with it.

One honest note about Claude: it does not learn between conversations. Every session starts from zero. What accumulates is what is written here, and that is why this notebook exists: it is the memory that lets us pick up where we left off.

## How it works

| Layer | What it is | Who writes it |
| --- | --- | --- |
| **Sources** | The code and papers in [`../microgpt/`](../microgpt/) and [`../papers/`](../papers/), always unchanged | the original authors |
| **Pages** | One concept per folder in [`concepts/`](concepts/), with an explanation, the passage from the paper, an experiment that runs on a laptop, why it matters and what we can build | Claude, from Ciro's questions |
| **Rules** | How the notebook is kept, in [`../AGENTS.md`](../AGENTS.md) | both, adjusted over time |

And two files that grow every session:

- [`log.md`](log.md): what was done and when, one line per event.
- [`predictions.md`](predictions.md): what we think AI will do, with a date, to check later.

**Each session:** pick the next concept on the ladder, read the page, run the experiment, ask. Every good question becomes part of a page or a new page instead of getting lost in the chat. Every so often, an **audit**: what went stale, what contradicts something else, what is mentioned but has no page yet.

## The ladder

From the smallest concept to the largest, each one standing on the one before. Every page has been ready since 31 October 2026.

| | Concept | Source | What the experiment showed |
| --- | --- | --- | --- |
| 1 | [**Token**](concepts/token/README.md): how text becomes numbers | microgpt · Transformer, sections 3.4 and 5.1 | The same text costs 43% more tokens in Portuguese on a tokenizer trained on English; on Claude, 16% |
| 2 | [**Embedding**](concepts/embedding/README.md): how a number gains meaning | microgpt · Transformer, sections 3.4 and 3.5 | With nobody saying what a vowel is, vowels end up alike (+0.53) and opposite to consonants (-0.29) |
| 3 | [**Attention**](concepts/attention/README.md): how each token looks at the others | microgpt · Transformer, section 3.2 | The 4 heads learn different habits: one looks at its own letter, another goes back to the start of the name |
| 4 | [**Gradient**](concepts/gradient/README.md): how a number learns | microgpt (`class Value`) · Transformer, section 5.3 | A small step against the gradient improves; too big a step makes the error explode from 3.5 to 24 |
| 5 | [**Training**](concepts/training/README.md): the loop of predicting, missing and adjusting | microgpt · Transformer, section 5.2 | The loss goes from 3.30 (guessing) to 2.28, and stays at 2.34 on names never seen: it learned, it did not memorize |
| 6 | [**Scale**](concepts/scale/README.md): why bigger gets better, and how far | Scaling Laws, section 1.2 | Up to 4,192 parameters, each model nearly 3 times bigger errs a little less; at 14,528 the error barely moves and training gets 7 times slower: the data runs out |
| 7 | [**From model to assistant**](concepts/fine-tuning/README.md): fine-tuning | Constitutional AI, abstract | 150 steps take "z" names from 1.5% to 100%, but the model forgets the rest; mixing examples protects |
| 8 | [**Written principles**](concepts/constitution/README.md): the constitution | Constitutional AI, abstract and figure 1 | Two principles and its own revisions take violations from 40% to 0%, at the cost of much of the variety |
| 9 | [**Agents**](concepts/agents/README.md): the model that uses tools | Claude's `tool_use` / `tool_result` format | The model only decides what to ask for; the program does the counting and the running |

## What the ladder teaches, together

- **Nothing is written by hand.** Vowels, attention heads, the way of answering: all of it comes from small steps against the gradient, on top of data.
- **Every gain has a measured price.** Portuguese costs more tokens, too big a step explodes, tuning too hard erases the rest, obeying too much takes away variety. The pages show each price in numbers.
- **Judge on what was not seen.** On every page that trains, the measure that matters is the one on names the model never saw.
- **The model thinks, the program acts.** The last rung joins everything: a model that only generates text becomes work when it gets tools and a loop with rules.

## Running it all

The experiments are pure Python, with nothing to install. [`lab.py`](lab.py) loads the original microgpt without changing the file and reproduces its result exactly (the same 20 names, the same final loss of 2.6497). Run one at a time on a Mac with Python 3.15, the fastest takes half a second and the longest 80 seconds (the fine-tuning one).

The ladder is not fixed: a good question along the way can become a new rung.
