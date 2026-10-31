# Written principles: the constitution

[Português](README.pt-BR.md) · [Notebook](../../README.md) · Previous: [fine-tuning](../fine-tuning/README.md) · Next: [agents](../agents/README.md)

**In one sentence:** in Constitutional AI, instead of people labelling every bad answer, the model's behaviour is guided by a short list of written principles; the model generates, critiques what it generated in light of the principles, revises, and is trained on its own revisions.

## How it works

To teach an assistant not to cause harm, the obvious path is to ask thousands of people to read answers and flag the bad ones. It works, but it is expensive, slow, and the standard ends up scattered across each rater's head.

Constitutional AI swaps that for a document: the **constitution**, a list of principles in plain language. The supervised phase has four steps:

1. **Generate.** The model answers requests, including difficult ones.
2. **Critique.** The model rereads its answer and points out where it breaks a principle.
3. **Revise.** The model rewrites the answer to respect the principle.
4. **Tune.** The original model is trained on the revised answers: the [fine-tuning](../fine-tuning/README.md) of the previous page, now with examples the model produced itself.

Then comes a second phase, by preferences, in which a model compares pairs of answers based on the principles.

## What the paper says

In the [Constitutional AI paper](../../../papers/2022-constitutional-ai.pdf):

> "The only human oversight is provided through a list of rules or principles, and so we refer to the method as 'Constitutional AI'."
> (abstract, page 1)

> "In the supervised phase we sample from an initial model, then generate self-critiques and revisions, and then finetune the original model on revised responses."
> (abstract, page 1)

Figure 1, on page 2, draws both phases.

## The experiment

```bash
cd notebook/concepts/constitution
python3 constitution.py
```

[`constitution.py`](constitution.py) redoes the supervised phase on microgpt, with a two-principle constitution for names:

1. at most 6 letters;
2. does not end in "n".

One difference must be clear: in the paper the critic and reviser are the model itself, reading the principles. microgpt cannot read; so the critic and the reviser here are two rules in Python. The reviser cuts the name to 6 letters and swaps a final "n" for "a". The three steps and the final tuning are the paper's; the critic is a stand-in.

On a Mac with Python 3.15, on 31 October 2026, it took 65 seconds.

| Model | break a principle | different names out of 300 | examples |
| --- | --- | --- | --- |
| base | 40% | 266 | `kamon ann karai jaire vialan karia yeran anna` |
| after 300 steps on its own revisions | **0%** | **77** | `anaa ana anar anaa anelia anahe karaa aria` |
| after 60 steps | 2% | 128 | `jana jana karia laraa keara kara lelara elala` |

Some critiques and revisions: `kamon → kamoa`, `ann → ana`, `vialan → vialaa`, `yeran → yeraa` (all for ending in "n").

What the table shows:

- **It works.** Without anyone labelling a single name, only two written principles and its own revisions, violations fell from 40% to 0%.
- **It has a price.** The model now writes only 77 different names out of 300, many of them odd (`anaa`, `karaa`). It learned the reviser's habits: the safest shortcut to never end in "n" was to end almost everything in "a".
- **The dose decides.** With 60 steps instead of 300, violations stay at 2% and variety rises to 128. Obeying more cost creativity; obeying a little less gave some back.

It is the same tension the paper faces at scale: an assistant that refuses everything to avoid harm is safe and useless. The paper calls the goal "harmless but non-evasive", and that is why the second phase also rewards helpful answers.

**Things to try:** replace `lab.train(ns, revised, 300)` with another number of steps, or change the second principle's reviser (`n[:-1] + 'a'`) to another fix, and see what happens to variety.

## Why it matters

- **The principles are in plain sight.** Instead of a standard hidden in thousands of labels, there is a text anyone can read, discuss and change. That is why this method is the one most specific to Claude.
- **It scales without a crowd.** The model critiques and revises itself, so behaviour training does not depend on people reading bad answers all day.
- **The reviser is half the result.** The experiment shows that a poor reviser teaches poor habits. The quality of the critique and the revision defines the model that comes out.

## What we can build

- **A constitution for your own agents.** A support, sales or health agent can have its short list of principles, written by the business owner, used to critique and revise each answer before it goes out. No model training needed: the critique-and-revise loop already works with a large model reading the text.
- **Measure obedience and variety together.** Every new rule in an agent should come with both of the experiment's measures: how many answers still break the rule, and how much variety and usefulness fell.

## Open questions

- So far the model only generates text. How does it start doing things in the world, like querying data or running a program? → **agents**, the next page.
- What happens if the reviser is microgpt itself, picking among several generated names the first one that respects the principles, instead of forcing a fix?
