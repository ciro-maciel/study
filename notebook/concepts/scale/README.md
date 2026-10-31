# Scale

[Português](README.pt-BR.md) · [Notebook](../../README.md) · Previous: [training](../training/README.md) · Next: [fine-tuning](../fine-tuning/README.md)

**In one sentence:** a bigger model makes fewer mistakes in a predictable way, but only if data and compute grow with it; with the data held still, growing the model stops helping and only gets more expensive.

## How it works

A model's size is its number of parameters. In [microgpt](../../../microgpt/microgpt.py), the main knob is the width, `n_embd = 16` (line 76): how many numbers each token carries. Doubling the width almost quadruples the parameters, because the matrices have width in both dimensions.

Three things can grow:

- **the model** (parameters);
- **the data** (how many different examples it sees);
- **the compute** (how many steps, how much calculation).

The finding of the scaling laws paper is that the error falls along a predictable curve, a **power law**, when you grow any of them, as long as the others are not holding it back. Like a recipe: doubling the flour does nothing if the water stays the same.

## What the paper says

In the [scaling laws paper](../../../papers/2020-scaling-laws-for-neural-language-models.pdf):

> "The loss scales as a power-law with model size, dataset size, and the amount of compute used for training, with some trends spanning more than seven orders of magnitude."
> (abstract, page 1)

And the formula for model size:

> "For models with a limited number of parameters, trained to convergence on sufficiently large datasets: L(N) = (N_c/N)^α_N ; α_N ∼ 0.076"
> (section 1.2, equation 1.1, page 4)

In practice: **multiplying the parameters by 10 multiplies the error by about 0.84**, that is, takes off about 16%. Each multiplication by 10 gains the same fraction, never a leap. The important part is the condition: "trained to convergence on sufficiently large datasets".

## The experiment

```bash
cd notebook/concepts/scale
python3 scale.py
```

[`scale.py`](scale.py) trains the same microgpt at three widths, with the same 1,000 steps and the same names, and measures all of them on the same 200 names none of them saw. On a Mac with Python 3.15, on 31 October 2026, it took 67 seconds. Width 32 was run separately, by changing the list of widths.

| Width | Parameters | Loss on names never seen | Training time |
| --- | --- | --- | --- |
| 4 | 472 | 2.425 | 5 s |
| 8 | 1,328 (2.8×) | 2.386 (-0.039) | 13 s |
| 16 | 4,192 (3.2×) | 2.343 (-0.043) | 49 s |
| 32 | 14,528 (3.5×) | **2.336 (-0.007)** | **332 s** |

What the table shows:

- **Up to width 16, the law shows.** Each time the parameters nearly triple, the error falls by a similar amount, about 0.04. Small, regular gains, the shape the paper measures.
- **Then it stops.** From 16 to 32, the model got 3.5 times bigger and the error barely moved (-0.007). The 1,000 training names became the bottleneck: the bigger model has nothing more to learn from so few examples.
- **The cost does not stop.** Training time rose almost 7 times, from 49 to 332 seconds, for a gain that barely shows.

The absolute numbers are not the paper's: names carry a lot of randomness no model removes (nobody guesses the next letter of a name for sure), and microgpt does not train to convergence. What repeats is the shape: regular gains while the data holds out, and the wall when it runs out.

**Things to try:** replace `for width in [4, 8, 16]` with `[32]` to see width 32 on its own (about 5 minutes), or raise the steps in `lab.train(ns, ns['docs'], 1000)` to give the bigger models more data.

## Why it matters

- **It explains the race for size.** Because the gain is predictable, you can plan how much to invest in a model before training it. That predictability is what justified training ever larger models.
- **It explains why data became the most contested resource.** The experiment shows the wall: without more data, more model does not help.
- **It helps choose a model day to day.** The bigger model is more expensive and slower, and does not always make fewer mistakes on your task. It pays to measure on your case before paying for the biggest.

## What we can build

- **Measure before switching to a bigger model.** For an agent or a task, run the same test cases on the smaller and the bigger model, and see whether the difference pays for the cost. Often the bottleneck is the example or the instruction, not the size, as width 32 showed.
- **A "is it worth it?" calculator.** Given each model's cost and the error measured on real cases, show the cost per correct answer. It is the table above, in money.

## Open questions

- A big, well-trained model knows a lot but still only continues text. How does it become an assistant that answers the right way? → **fine-tuning**, the next page.
- With 3,000 steps instead of 1,000, does width 32 pull ahead of 16 again?
