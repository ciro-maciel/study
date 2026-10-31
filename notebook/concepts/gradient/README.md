# Gradient

[Português](README.pt-BR.md) · [Notebook](../../README.md) · Previous: [attention](../attention/README.md) · Next: [training](../training/README.md)

**In one sentence:** the gradient says, for each number in the model, which way and how hard to move it for the error to fall; learning is taking small steps against the gradient.

## How it works

The model has 4,192 numbers (the parameters), and the error depends on all of them. The training question is: if I move this number a little, does the error go up or down, and by how much? That answer is the gradient of that number.

You could find it by hand: move one number, recompute the error, look at the difference. But that would be 4,192 recomputations per step. The trick is **backpropagation**: every operation remembers where it came from, and a single pass backwards computes the gradient of every number at once, by the chain rule.

In [microgpt](../../../microgpt/microgpt.py) this is `class Value` (line 30). Every sum, product or power creates a `Value` that remembers its "children" and the local derivative. The `backward()` method (line 59) walks that graph backwards and fills in each number's `.grad`. On line 172, `loss.backward()` does this for the whole model, and on line 181 each parameter takes a step against its own gradient.

## What the paper says

The Transformer paper does not explain backpropagation; it is so basic that it is assumed. What it says is which optimizer uses the gradients:

> "We used the Adam optimizer [20] with β1 = 0.9, β2 = 0.98 and ε = 10^-9."
> (section 5.3, page 7)

microgpt uses the same Adam (lines 147 to 181), with other values (`beta1 = 0.85`, `beta2 = 0.99`). Adam does not step straight along the gradient: it averages recent gradients and adjusts each number's step size, which makes training steadier.

## The experiment

```bash
cd notebook/concepts/gradient
python3 gradient.py
```

[`gradient.py`](gradient.py) uses microgpt's own `class Value`, first on a small formula, then on the real model, with no training at all. On a Mac with Python 3.15, on 31 October 2026, it took 21 seconds.

**1. A small formula:** `f = a × b + b²`, with `a = 2` and `b = -3`, gives `f = 3`.

| | df/da | df/db |
| --- | --- | --- |
| backpropagation (`backward()`) | -3.0 | -4.0 |
| by hand (nudge by 0.000001 and measure) | -3.0000 | -4.0000 |

Both agree. Backpropagation is just far faster: one pass instead of one computation per number.

**2. The real model, one word.** The untrained model misses `emma` with a loss of 3.4955. A single call to `backward()` computes the gradient of all 4,192 parameters: 3,616 come out non-zero (the others took no part in this word, like the rows of letters `emma` does not contain). Then one step against the gradient, of several sizes:

| Step size | loss on `emma` | loss on 200 other names |
| --- | --- | --- |
| before | 3.4955 | 3.2914 |
| 0.01 | 3.4256 (-0.07) | 3.2895 (-0.002) |
| 0.1 | 2.8610 (-0.63) | 3.2762 (-0.015) |
| 1 | 1.9234 (-1.57) | 3.2879 (-0.003) |
| 10 | **24.0197 (+20.52)** | **15.4791 (+12.19)** |

Three lessons in one table:

- **The gradient points the way.** A small step against it always improved `emma`.
- **Learning one word helps the others little.** With step 0.1, `emma` fell 0.63 and the other names only 0.015. With step 1, `emma` fell even more, but the others gained almost nothing: the whole step went into memorizing `emma`. That is why training goes through thousands of different words.
- **Too big a step destroys.** With step 10 the error explodes, on `emma` and everywhere. The gradient gives the direction only nearby; too far away, it no longer holds. That is why microgpt uses steps of 0.01 (line 175) and shrinks them towards the end of training.

## Why it matters

- **It is the only way the model learns.** No rule is written by hand: everything the earlier pages showed (vowels, attention heads) came from millions of small steps like these.
- **It is why training is expensive.** Each step is a pass forward (compute the error) and a pass back (compute the gradients) through every number. In a large model that is hundreds of billions of numbers, billions of times.
- **It explains "learning rate".** It is the step size. The experiment shows both ways to get it wrong: too small does not move, too big explodes.

## What we can build

- **An interactive "watch the model learn".** A slider for the step size, and you see the error fall, stall or explode. The table above, alive.
- **Intuition for whoever decides.** People who buy AI hear "we need more data" and "more training". Knowing that learning is step by step, and that too big a step breaks it, helps ask the right questions.

## Open questions

- One step improves one word. What happens when you repeat it a thousand times, each time with a different name? → **training**, the next page.
- Adam adjusts each number's step. How much worse does microgpt get with the plain step, without Adam?
