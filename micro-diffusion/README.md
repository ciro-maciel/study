# Micro Diffusion: text that appears all at once

[Português](README.pt-BR.md)

A GPT writes one letter after the other, left to right. A diffusion model does it another way: it starts from a word where every letter is erased and fills in the blanks a few at a time, the ones it is surest about first, until nothing is erased. Image generators work like this; text models that write this way exist too. This file shows the whole idea on first names, in about 350 lines of Python and NumPy, training in seconds.

- **Author:** Siwoo4985
- **Original:** <https://github.com/Siwoo4985/Micro-Diffusion> (MIT)
- **Copied from commit:** `00535e70f8328bfb445ecc88d96f738ece76961c`, on 6 November 2026, unchanged: `train_pure.py` and `names.txt`
- **sha256:** `train_pure.py` `ea89c17b1f99199ad7b10047f77980b02a94c4883766ea43ddadce872c45cc04`

## Run it

It needs NumPy (microgpt needs nothing; this one does the arithmetic on whole matrices at once):

```bash
python3 -m pip install numpy
python3 train_pure.py --seed 42
```

What we saw on a Mac (Apple M4 Pro, Python 3.15.2, NumPy 2.5.4) on 6 November 2026. With `--seed 42` the output repeated exactly on a second run.

| | |
| --- | --- |
| Names | 31,979 (up to 12 letters) |
| Parameters | 238,672 |
| Training | 5,000 steps of 64 names, in 5 seconds |
| Some invented names | `honcea`, `avilya`, `nokan`, `lymane`, `kaihan`, `jaholyn`, `salma`, `marce` |

## Erasing, then filling in

First it shows the **forward process**, the easy direction: take a real name and erase more letters at each step `t`, following a schedule that ends with everything erased (`_` is an erased letter):

```
Forward Process: "matison"
  t=  0 (mask   0.0%): matison
  t=  5 (mask   4.2%): _atison
  t= 10 (mask  15.3%): matis_n
  t= 20 (mask  50.6%): _at_s_n
  t= 30 (mask  85.6%): _______
  t= 40 (mask 100.0%): _______
```

**Training** is that same erasing, thousands of times: pick names, pick a `t` between 1 and 40, erase that share of letters, and ask the model to guess every original letter. The error goes down as it learns:

```
  step |     loss |   t |  mask%
     0 |   3.3550 |   8 |  10.1%
  2500 |   0.0697 |   4 |   2.8%
  4999 |   0.9560 |  24 |  65.9%
```

The error jumps around because `t` changes at every step: with 3% erased the answer is almost given, with 66% erased it is hard. Compare lines with similar `t`, not neighbours.

**Generating** goes the other way. Start with 12 erased letters, ask the model for every blank, keep the guesses it is most confident about and erase the rest again; repeat 40 times. Four names being born:

```
  t= 40 (  0.0%): ___________ | ___________ | ___________ | ___________
  t= 30 ( 25.0%): _y | _oncea | avi_ya | no_an
  t= 20 ( 50.0%): ty | honcea | avilya | nokan
```

`honcea` had its middle before its first letter. That is the difference from a GPT, which could never decide the end of a word before its beginning.

## What is inside, in file order

| Part | What it does |
| --- | --- |
| **Config** | 12 letters at most, 256 neurons per layer, 40 noise levels (`T`), 5,000 steps, 64 names per step |
| **Tokenizer** | One number per letter, plus `PAD` (the name ended) and `MASK` (erased) |
| **Noise schedule** (`cosine_mask_rate`, `add_noise`) | How much to erase at each `t`: little at first, everything at the end |
| **Denoiser** (`forward`) | An MLP, three layers with a skip connection, that sees the whole name at once (each letter as 28 zeros and a one) plus `t`, and guesses all 12 letters |
| **Training** (`train_step`) | Erase, guess, measure the error, and the backward pass written by hand: no autograd here, every derivative is spelled out |
| **Sampling** (`sample`) | From all erased to a name in 40 steps, revealing the surest letters first |

## microgpt and this, side by side

| | [microgpt](../microgpt/) | Micro Diffusion |
| --- | --- | --- |
| Writes | one letter after another, left to right | all letters at once, the surest first |
| Model | a Transformer with attention | an MLP that sees the whole name |
| Derivatives | `Value` autograd, computed automatically | written by hand, layer by layer |
| Arithmetic | one number at a time, pure Python | whole matrices at once, NumPy |
| Training on the same Mac | 42 s, 1,000 names | 5 s, 320,000 names |

The last line is the next step after [how fast, and why](../microgpt/README.md#how-fast-and-why): the speed here comes from doing matrices at once, not from a faster language.

## Things to try

- `--temperature 0.6` or `1.0`: the run already prints both; safer names at 0.6, stranger at 1.0.
- `--steps 500`: a tenth of the training. Ours came out as `jlmin`, `fnaicna`, `rdibnr`: the shape of a name is not there yet.
- `T = 40` → `10` (in a copy): four times fewer steps to generate, each one revealing more letters at once. We expected worse names and did not see it: ours came out as `karye`, `dorton`, `nona`, `narrah`. Fifteen names are too few to tell; try it and count.

## Learned from

- [Micro-Diffusion](https://github.com/Siwoo4985/Micro-Diffusion): the code itself, and the idea of explaining text diffusion in the same minimal style as microgpt.

## Study next

1. [microgpt](../microgpt/), the left-to-right way, to compare.
2. The author's [`train.py`](https://github.com/Siwoo4985/Micro-Diffusion/blob/main/train.py): the same diffusion with a Transformer in PyTorch.
