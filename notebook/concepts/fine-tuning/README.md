# From model to assistant: fine-tuning

[Português](README.pt-BR.md) · [Notebook](../../README.md) · Previous: [scale](../scale/README.md) · Next: [constitution](../constitution/README.md)

**In one sentence:** fine-tuning is training an already-trained model a little more, for a few steps, on a small hand-picked set of examples; it is how a model that only continues text becomes an assistant that answers the right way.

## How it works

Pre-training (the [training](../training/README.md) page) teaches a model to continue any text. It knows a lot but does not know what is expected of it: asked "what is the capital of France?", a base model may continue with another question, because lists of questions exist on the internet too.

Fine-tuning uses **the same loop**, with three differences:

- **it starts from a trained model**, not from random numbers;
- **it uses few, hand-picked examples** (good conversations, answers in the right format);
- **it takes few steps**, to change the behaviour without erasing what the model already knows.

After that, today's assistants go through a second stage, by **preferences**: the model writes two answers, someone (a person or another model) says which is better, and training pushes the model towards the preferred ones.

## What the paper says

In the [Constitutional AI paper](../../../papers/2022-constitutional-ai.pdf), both stages appear in the abstract:

> "In the supervised phase we sample from an initial model, then generate self-critiques and revisions, and then finetune the original model on revised responses. In the RL phase, we sample from the finetuned model, use a model to evaluate which of the two samples is better, and then train a preference model from this dataset of AI preferences."
> (abstract, page 1)

The first sentence is fine-tuning; the second is learning from preferences. The next page, [constitution](../constitution/README.md), redoes the first in miniature.

## The experiment

```bash
cd notebook/concepts/fine-tuning
python3 fine_tuning.py
```

[`fine_tuning.py`](fine_tuning.py) trains microgpt for the usual 1,000 steps (the "base model") and then runs two fine-tunings of 150 steps, each starting from the same base model:

- **z names only:** of the 895 names starting with "z" that the base model did not see, the first 150, one per step;
- **half z, half others:** 75 of those "z" names, interleaved with 75 ordinary names.

On a Mac with Python 3.15, on 31 October 2026, it took 80 seconds.

| Model | generated names starting with z | loss on 200 ordinary names |
| --- | --- | --- |
| base | 1.5% | 2.343 |
| tuned on z only | **100%** | **3.581** |
| tuned half z, half others | **92%** | **2.501** |

Names generated after tuning on z only: `zayai zali zon zaylye zania zaren zailyn zarie zaha zadiri`.

What the table shows:

- **A few steps change a lot.** 150 steps (15% of the original training) took names with "z" from 1.5% to 100%.
- **Tuning too hard erases the rest.** After tuning on "z" only, the loss on ordinary names went to 3.58, **worse than random guessing** (3.30). The model did not become "specialized": it forgot what other names look like. This has a name: **catastrophic forgetting**.
- **Mixing protects.** With half ordinary names in the tuning, the model still writes 92% "z" names and the loss on ordinary ones stays at 2.50, close to the base. That is why real fine-tuning mixes the new examples with general data.

**Things to try:** replace every `'z'` in `fine_tuning.py` with another letter and see whether the same story repeats.

## Why it matters

- **It is what makes the assistant.** The same base model can become a polite assistant, a programmer or a translator, depending on the tuning examples.
- **It shows a risk.** Tuning a model on very narrow data can make it worse at everything else, and that does not show if you only test the new case. The experiment caught the problem only because it also measured ordinary names.
- **It shows the power of few examples.** 150 names changed the behaviour of a model trained on 1,000. In a large model, a few thousand well-chosen conversations change how a model trained on trillions of tokens answers.

## What we can build

- **Before tuning, measure what you might lose.** Any adjustment of a model, or even of a prompt, for a new case needs a battery of the old cases running alongside. The experiment shows why in numbers.
- **Examples are the product.** In fine-tuning, what decides the result is the choice of examples. A good collection of examples from one trade (a clinic's support, a shop's answers) is worth more than the choice of model.

## Open questions

- In the experiment, someone chose the "z" names. What if the model generated the examples itself, a critic pointed out what breaks a rule and a reviser fixed it? → **constitution**, the next page.
- How many steps of tuning on "z" only does it take for the loss on ordinary names to pass 3.30?
