# Attention

[Português](README.pt-BR.md) · [Notebook](../../README.md) · Previous: [embedding](../embedding/README.md) · Next: [gradient](../gradient/README.md)

**In one sentence:** attention is the step where each token looks at the tokens before it and decides how much each one matters for predicting the next; it is the idea the Transformer paper is named after.

## How it works

After the embedding, every token has its own list of numbers, but it is still on its own. To predict the letter after "isabel", the model has to look back: what came before changes everything.

Attention does this with three lists per token, computed from the embedding:

- **query** (`q`): what this token is looking for;
- **key** (`k`): what each earlier token offers;
- **value** (`v`): what each earlier token hands over if it is chosen.

The model compares the current token's query with the key of each earlier token (a multiplication and a sum), turns the scores into percentages that add up to 100% (the `softmax`) and mixes the values in that proportion. In [microgpt](../../../microgpt/microgpt.py) this is two lines: line 129 computes the scores (`attn_logits`) and line 130 turns them into weights (`attn_weights = softmax(attn_logits)`).

And it happens in **4 heads** at once (the loop on line 124), each with its own queries and keys. Each head can learn to look for something different.

## What the paper says

In the [Transformer paper](../../../papers/2017-attention-is-all-you-need.pdf):

> "We call our particular attention "Scaled Dot-Product Attention" (Figure 2). The input consists of queries and keys of dimension d_k, and values of dimension d_v. We compute the dot products of the query with all keys, divide each by √d_k, and apply a softmax function to obtain the weights on the values."
> (section 3.2.1, page 4)

The division by √d_k is in microgpt: it is the `/ head_dim**0.5` on line 129. And about the several heads:

> "Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions."
> (section 3.2.2, page 5)

## The experiment

```bash
cd notebook/concepts/attention
python3 attention.py
```

[`attention.py`](attention.py) trains microgpt for the 1,000 steps and then watches the weights of line 130 while it reads 300 names it has never seen. The original file does not change: the notebook's lab ([`lab.py`](../../lab.py)) adds, in memory only, one line that records the weights. On a Mac with Python 3.15, on 31 October 2026, it took 53 seconds.

**Where each head looks, on average** (from the third letter on, when start, previous letter and current letter are three different tokens):

| Head | start of the name | previous letter | current letter | the rest |
| --- | --- | --- | --- | --- |
| 0 | 22% | 24% | 18% | 36% |
| 1 | 19% | 29% | 21% | 30% |
| 2 | 19% | 30% | 12% | 39% |
| 3 | 20% | 29% | 10% | 41% |

**Reading "isabella"** (the dot is the start token), the token each head looks at most at each position:

| Reading | head 0 | head 1 | head 2 | head 3 |
| --- | --- | --- | --- | --- |
| `i` | `.` 73% | `.` 76% | `i` 56% | `.` 67% |
| `s` | `.` 44% | `s` 44% | `i` 37% | `.` 45% |
| `a` | `i` 26% | `a` 45% | `i` 60% | `.` 58% |
| `b` | `i` 26% | `a` 30% | `i` 35% | `.` 21% |
| `e` | `i` 19% | `e` 32% | `b` 56% | `.` 37% |
| `l` | `i` 26% | `.` 19% | `.` 21% | `a` 23% |
| `l` | `i` 22% | `.` 15% | `.` 23% | `e` 19% |
| `a` | `i` 14% | `l` 18% | `b` 70% | `l` 30% |

The heads do not do the same thing. Head 1 looks a lot at its own letter; head 2 goes back hard to striking letters from the start (`i`, `b`); head 3 looks at the start of the name during the first letters, which helps it know how far into the name it is; head 0 stays fixed on the initial `i`. Nobody gave them these roles: they came out of training, like the vowels in the embedding.

What cannot be said: that each head "understands" a rule. The numbers show where it looks, not why. Reading the why inside a model is a whole research field, interpretability.

**Things to try:** replace `name = 'isabella'` with another name and see whether the heads keep the same habits.

## Why it matters

- **It is what lets a model read context.** "Bank" means different things in "we sat on the river bank" and "I opened an account at the bank"; attention is what lets the rest of the sentence decide.
- **It is why context costs.** Every token looks at all the earlier ones. Doubling the text doubles the number of tokens and quadruples the number of comparisons. That is why long context is expensive and slow.
- **It is the heart of the Transformer.** Before it, models read one word at a time, in order. With attention, every position is computed in parallel, which made it possible to train much larger models.

## What we can build

- **An attention viewer.** Type a sentence and see, in colour, where the model looked at each word. It teaches in seconds what would take a chapter.
- **Send less context.** Since each token compares itself with all the earlier ones, it pays to send a model only the passage that matters: cheaper, faster and often better.

## Open questions

- Nobody wrote the attention weights. How did the model arrive at them? → **gradient**, the next page.
- With more layers, a head can look at the output of another. What changes when `n_layer` goes from 1 to 2?
