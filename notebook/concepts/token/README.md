# Token

[Português](README.pt-BR.md) · [Notebook](../../README.md) · Next: embedding (not written yet)

**In one sentence:** a token is the piece of text a model sees as one unit; it reads neither letters nor words, but a sequence of numbers, and each number is a piece.

## How it works

A language model only does arithmetic. Before anything else, text has to become numbers, and the **tokenizer** is the part that does it, both ways: text to numbers going in, numbers to text coming out.

There are two ways to cut text, and this repository has both:

- **One letter, one token.** This is what [microgpt](../../../microgpt/microgpt.py) does on lines 24 to 26: it gathers every letter that appears in the names, sorts them, and each letter's position in that list becomes its number. That is 26 letters plus one special token (`BOS`) marking where a name starts and ends: 27 in all. Simple, but every word becomes many tokens, and the model must learn from scratch that "t" and "h" together often make "th".
- **Pieces that repeat.** This is what real models do, with a technique called **byte-pair encoding** (BPE). Start with the 256 possible bytes, find the pair of neighbours that appears most often, glue the two into a new token and repeat. After a few hundred merges, the common parts of a language become a single token: "the ", "ing", "ção".

That is why a model like Claude does not see "attention" as one word: it sees one to a few pieces, depending on what its tokenizer learned.

## What the paper says

In the [Transformer paper](../../../papers/2017-attention-is-all-you-need.pdf), two short passages:

> "we use learned embeddings to convert the input tokens and output tokens to vectors of dimension d_model"
> (section 3.4, page 5)

So after the tokenizer, each number becomes a learned list of numbers, the **embedding**. That is the notebook's next concept.

> "Sentences were encoded using byte-pair encoding [3], which has a shared source-target vocabulary of about 37000 tokens."
> (section 5.1, page 7)

The original Transformer already used BPE, with a vocabulary of about 37 thousand tokens.

## The experiment

```bash
cd notebook/concepts/token
python3 tokens.py
```

[`tokens.py`](tokens.py) is a BPE tokenizer in pure Python, with 300 merges, trained on this repository's README, frozen on 31 October 2026 in [`sample.en.md`](sample.en.md) and [`sample.pt.md`](sample.pt.md): the same text in English and in Portuguese. It runs in under a second.

What it printed on a Mac with Python 3.15, on 31 October 2026:

**1. One letter, one token:** `attention` becomes 9 tokens.

**2. BPE trained on the English text.** The first pieces it learned: `e␣`, `th`, `s␣`, `,␣`, `in`, `t␣`. The longest are whole links, such as `](https://ciromaciel.click/?ref=oss-study)`, because they repeat a lot in that text: **a tokenizer learns what repeats, not what makes sense.**

| Text | Tokens | Pieces |
| --- | --- | --- |
| `the code` | 3 | `the␣` · `co` · `de` |
| `microgpt` | 1 | `microgpt` |
| `attention` | 4 | `a` · `tt` · `ent` · `ion` |
| `atenção` | 7 | `at` · `en` · `<c3>` · `<a7>` · `<c3>` · `<a3>` · `o` |

"ç" and "ã" take two bytes each. A tokenizer that has only seen English never glued those bytes together, so each accented letter becomes two tokens that are not even letters on their own.

**3. The same text, two languages, two tokenizers:**

| Trained on | English | Portuguese | Portuguese costs |
| --- | --- | --- | --- |
| English | 1,535 tokens | 2,199 tokens | **43% more** |
| Portuguese | 2,176 tokens | 1,606 tokens | 26% less |

Both texts are almost the same length (4,092 and 4,174 characters). What changes is the language the tokenizer learned from.

**Things to try:**
- `MERGES = 300` → `30`: few merges, short pieces. `microgpt` becomes 6 tokens (`m · ic · ro · g · p · t`) and Portuguese costs only 13% more.
- `MERGES = 300` → `1000`: the tokenizer **memorizes the text**. With little text and too many merges, the whole opening of the README becomes a single token, and Portuguese now costs 216% more. It is the same problem a model has when it memorizes its examples instead of learning: perfect on what it has seen, poor on everything else.
- Replace `'atenção'` in the word list with your name, or a technical word from your work.

## Why it matters

- **Price.** Models are billed per token, going in and coming out. The same request can cost more in Portuguese than in English, depending on the model's tokenizer.
- **Memory.** The context limit ("how much the model holds at once") is counted in tokens, not pages.
- **The answer comes out in pieces.** The model generates **one token at a time**: it picks the next piece, appends it to the text and repeats. That is why the answer appears bit by bit on screen, and it is the question on the cover of *IA por dentro*.
- **Odd mistakes.** Counting the letters of a word is hard for a model because it does not see the letters, it sees the pieces.

The measurement in experiment 3 holds for this small tokenizer, trained on one text. The tokenizers of large models learn from far more text and many languages, so the real gap is different. The mechanism is the same, and the real gap is measured by counting the tokens of the same text in both languages on the model you use.

## What we can build

- **Measure before choosing an agent's language.** An AI agent sends the same instructions with every request. Counting the tokens of those instructions in Portuguese and in English, on the model it uses, says whether they should be written in English, with only the conversation with the person in Portuguese.
- **A free tool: "what your text costs".** Paste a text, see its pieces in colour and how many tokens it costs. It teaches the concept in ten seconds.
- **The book's hands-on appendix.** The chapters "Uma palavra de cada vez" and "A matéria-prima: dados e tokens" of [*IA por dentro*](https://ciromaciel.click/books/ia-por-dentro?ref=oss-study) explain it in words; this experiment is their do-it-yourself.

## Open questions

- If a token is just a number, how does the model know that "cat" and "dog" are closer to each other than to "screw"? → **embedding**, the next page.
- How many tokens are in Claude's vocabulary, and how much more does Portuguese cost on it? Measure with the API's token counter.
