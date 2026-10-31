# Embedding

[Português](README.pt-BR.md) · [Notebook](../../README.md) · Previous: [token](../token/README.md) · Next: [attention](../attention/README.md)

**In one sentence:** an embedding is the list of numbers a model learns for each token; tokens that behave alike end up with similar lists, and that is how a bare number gains meaning.

## How it works

A token is only a label: "a" is number 0, "b" is 1. A label says nothing; 0 and 1 being close does not mean "a" and "b" are alike. So the first thing a model does with each token is swap it for a **list of numbers** kept in a table.

In [microgpt](../../../microgpt/microgpt.py) that table is called `wte` (line 81): 27 rows, one per token, each with 16 numbers (`n_embd = 16`, line 76). On line 109, `tok_emb = state_dict['wte'][token_id]` looks up the token's row. On line 110 a second table, `wpe`, does the same for the **position** (first letter, second letter...), and the two lists are added.

At the start the table is random. Nobody writes in it. Training adjusts those numbers together with everything else, only to miss the next letter less often. What appears in the table afterwards is a side effect: letters that show up in the same places end up with similar lists.

To measure "similar", the experiment uses **cosine similarity**: +1 when two lists point the same way, 0 when they are unrelated, -1 when they point in opposite directions.

## What the paper says

In the [Transformer paper](../../../papers/2017-attention-is-all-you-need.pdf):

> "we use learned embeddings to convert the input tokens and output tokens to vectors of dimension d_model"
> (section 3.4, page 5)

And about position:

> "Since our model contains no recurrence and no convolution, in order for the model to make use of the order of the sequence, we must inject some information about the relative or absolute position of the tokens in the sequence."
> (section 3.5, page 6)

The paper uses fixed sines and cosines for position; microgpt, like GPT-2, learns position in a table, `wpe`.

## The experiment

```bash
cd notebook/concepts/embedding
python3 embeddings.py
```

[`embeddings.py`](embeddings.py) trains microgpt for the original's 1,000 steps and compares the `wte` table before and after. On a Mac with Python 3.15, on 31 October 2026, it took 47 seconds.

| | vowel with vowel | vowel with consonant | consonant with consonant |
| --- | --- | --- | --- |
| before training | -0.01 | +0.00 | +0.00 |
| after training | **+0.53** | **-0.29** | +0.22 |

| Letter | Most similar, before | Most similar, after |
| --- | --- | --- |
| `a` | t i w l | **o e u** q |
| `e` | m c o h | **u o a i** |
| `k` | j x b w | l j v w |
| `n` | p f j s | y h r w |

**Nobody told the model what a vowel is.** It only tried to guess the next letter of 1,000 names and, to do that, found it useful to give vowels lists that resemble each other and oppose the consonants. The category "vowel" came out of the data.

The 16 numbers of `a` after training: `+0.13 +0.05 +0.24 -0.06 +0.04 -0.30 -0.40 -0.02 +0.01 +0.07 +0.35 +0.13 -0.09 -0.17 -0.17 -0.37`. None of them alone means "vowel"; the meaning is in the whole list.

**Things to try:** replace `'aekn'` in `report()` with other letters and see who ends up near whom.

## Why it matters

- **It is where "understanding" lives.** In a large model the same thing happens with thousands of dimensions and hundreds of thousands of tokens: words with similar meanings end up with similar lists, with nobody teaching synonyms.
- **It is the basis of search by meaning.** Comparing embeddings is how a system finds the right document even when the question uses other words.
- **It explains a bias.** The model learns the similarities the data shows, including the ones nobody wanted.

## What we can build

- **Search by meaning over your own collection.** A book, a support knowledge base or a recipe catalogue, where people ask in their own words and find the right passage.
- **Group without labels.** Just as the vowels gathered by themselves, customer messages or comments group by topic without anyone defining the categories first.
- **A visual map.** Draw the 27 letters on a plane, coloured by vowel and consonant, before and after training: the simplest picture of what a model learns.

## Open questions

- The embedding says what each token is. But how does the model combine the tokens of a sentence, knowing which ones matter for the next? → **attention**, the next page.
- What would happen to the vowels if the model had only 4 numbers per letter instead of 16? (The [scale](../scale/README.md) page trains smaller widths.)
