# Training

[Português](README.pt-BR.md) · [Notebook](../../README.md) · Previous: [gradient](../gradient/README.md) · Next: [scale](../scale/README.md)

**In one sentence:** training is repeating the same loop thousands of times (take an example, predict, measure the error, step against the gradient) until the model makes few mistakes on text it has never seen.

## How it works

The [microgpt](../../../microgpt/microgpt.py) loop starts on line 152 and has four parts:

1. **Take an example.** One name per step, wrapped in the start and end token.
2. **Predict.** For each position, the model gives a probability to each of the 27 possible next letters.
3. **Measure the error.** The loss at each position is `-log(probability of the right letter)` (line 167): if the model gave the right letter 100%, the loss is 0; if it gave it almost nothing, the loss is large. The name's loss is the average.
4. **Adjust.** `loss.backward()` (line 172) computes the gradients and Adam takes the step (line 181), with a size that shrinks towards the end (line 175).

Two numbers help read the loss:

- **Random guessing.** If the model gave the same chance to all 27 options, the loss would be `ln(27) = 3.30`. It is the starting point of a model that knows nothing.
- **Loss on names never seen.** This is the number that matters. Few mistakes on the training names may be memorizing; few mistakes on the others is learning.

## What the paper says

The [Transformer paper](../../../papers/2017-attention-is-all-you-need.pdf) says what training its model cost:

> "We trained our models on one machine with 8 NVIDIA P100 GPUs. For our base models using the hyperparameters described throughout the paper, each training step took about 0.4 seconds. We trained the base models for a total of 100,000 steps or 12 hours."
> (section 5.2, page 7)

The same loop at another scale: 100 thousand steps on 8 graphics cards, against microgpt's 1,000 steps on an ordinary processor.

## The experiment

```bash
cd notebook/concepts/training
python3 training.py
```

[`training.py`](training.py) generates names before training, trains for the 1,000 steps while keeping the loss of each one, measures on 200 names the model never saw, and generates names again. On a Mac with Python 3.15, on 31 October 2026, it took 50 seconds.

**Before training** (the numbers are still random): `orgzqpdlw ptoabqmofyoqzxck eaktbsuhu zqcizclxmzgziotw qmcnezp hsentvzrknoqrvcl`. Random letters, random lengths.

**The loss, averaged every 100 steps:**

| Steps | Average loss |
| --- | --- |
| random guessing | 3.30 |
| 1 to 100 | 2.77 |
| 101 to 200 | 2.53 |
| 201 to 300 | 2.46 |
| 301 to 400 | 2.44 |
| 401 to 500 | 2.46 |
| 501 to 600 | 2.42 |
| 601 to 700 | 2.41 |
| 701 to 800 | 2.39 |
| 801 to 900 | 2.33 |
| 901 to 1,000 | 2.28 |
| **200 names never seen** | **2.34** |

**After training:** `dalian marian karin malin ariana alona elanon jaran`.

What the table shows:

- **Most of it comes early.** The first 100 steps already take the model away from guessing (3.30 to 2.77). After that, each hundred steps gains little.
- **It does not fall in a straight line.** Between steps 301 and 500 the loss even rises a little: each step looks at a single name, and some names are harder than others.
- **It learned, it did not memorize.** The loss on names never seen (2.34) stays close to the loss of the last training steps (2.28). Had it memorized, the gap would be large.

The names generated here differ from those in the [microgpt guide](../../../microgpt/README.md), because generating names before training uses up random numbers; the trained model is the same.

## Why it matters

- **It is what separates a base model from a dice roll.** Every language model went through this loop, with trillions of tokens instead of a thousand names.
- **It explains what "pre-training" is.** Predicting the next token over lots of text, with nobody saying what is right other than the text itself. microgpt does exactly that, in miniature.
- **It gives the right test.** A model is judged on what it has not seen. In any use of AI the question is the same: does it work on new cases, or only on the examples?

## What we can build

- **A live "training lesson".** The loop running on screen, random names turning into plausible names in under a minute. It is the most convincing experiment for someone who has never watched a model learn.
- **The habit of holding out test cases.** Before saying that an agent or a prompt "works", keep cases it has never seen and measure on them, the same way as the 200 names in this experiment.

## Open questions

- The loss stopped around 2.3. Is that the limit of the model or of the data? What happens with a bigger model? → **scale**, the next page.
- How much does the loss on unseen names improve with 3,000 steps instead of 1,000?
