# microgpt: a whole GPT in 199 lines

[Português](README.pt-BR.md)

A complete GPT, from text to generation, in **199 lines of pure Python**. It imports only `os`, `math` and `random`: no PyTorch, no NumPy, no GPU. The file opens with: "This file is the complete algorithm. Everything else is just efficiency."

- **Author:** Andrej Karpathy
- **Original:** <https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95>
- **Copied from revision:** `14fb038816c7aae0bb9342c2dbf1a51dd134a5ff`, on 31 October 2026, unchanged
- **sha256:** `d47d88c2fd432c8ebdc1048beab7f7eb64ea7e0e664e11b812d72a6d95ebccee`

## Run it

```bash
python3 microgpt.py
```

The first run downloads `input.txt`: 32,033 first names, from the author's `makemore` repository. Then it trains for 1,000 steps, printing the error at each one, and finally invents 20 names that were not on the list.

What we saw on a Mac with Python 3.15, on 31 October 2026:

| | |
| --- | --- |
| Parameters | 4,192 |
| Training time | 42 seconds |
| Error (loss), first step | 3.37 |
| Error (loss), last steps | about 2.2 |
| Some invented names | `kamon`, `karai`, `vialan`, `yeran`, `keylen`, `alerin` |

The error is noisy from step to step because each step looks at a single name; watch the trend, not each line. The file fixes the random seed (`random.seed(42)`), so with the same Python you should get the same names we did.

## Did it learn, or memorize?

The 1,000 training steps see only the first 1,000 names of the shuffled list (`docs[step % len(docs)]`), so the other 31,033 are names the model never saw. [`evaluate.py`](evaluate.py) runs `microgpt.py` unchanged and then measures the average error per letter, the same loss the training prints:

```bash
python3 evaluate.py
```

What we measured on a Mac (Apple M4 Pro, Python 3.15.2) on 5 November 2026, in 64 seconds:

| Average error per letter (lower is better) | |
| --- | --- |
| Guessing each letter at random (27 options) | 3.30 |
| Bigram: each letter from the one before, counted on the same 1,000 names, on 500 unseen names | 2.52 |
| microgpt, on 500 names it trained on | 2.35 |
| microgpt, on 500 names it never saw | 2.39 |

The error on new names is almost the same as on the names it trained on: it learned how names are built, it did not memorize the list. And it beats the bigram, which only knows the previous letter. That gap is what attention buys.

## One name, step by step

[`trace.py`](trace.py) runs `microgpt.py` unchanged and then follows a single name through the trained model: the token that goes in at each position, the three letters the model finds most likely next, and the probability it gave the right one. On the same Mac, on 5 November 2026, in 43 seconds:

```
--- "emma" as tokens: [26, 4, 12, 12, 0, 26] ---
after <BOS>  model guesses: a 14%, k 9%, j 8%             right answer e: 5%
after     e  model guesses: l 28%, r 12%, n 12%           right answer m: 6%
after     m  model guesses: i 22%, a 22%, e 18%           right answer m: 1%
after     m  model guesses: i 25%, a 23%, e 17%           right answer a: 23%
after     a  model guesses: n 30%, <BOS> 17%, r 10%       right answer <BOS>: 17%
```

Read it line by line. `<BOS>` (token 26) marks where a name starts and ends. At the start the model bets on the letters names often begin with. After `em` it expects a vowel, so a second `m` gets 1%. After `emm` the right `a` is one of its top three. After the final `a` it gives 17% to the name ending there. Every one of the 1,000 training steps is this same walk, with the error of each right answer pushed down a little. Try your own: `python3 trace.py anna`.

## What is inside, in file order

| Part | What it does |
| --- | --- |
| **Dataset** | Reads the list of names, one per line, and shuffles it |
| **Tokenizer** | Each letter becomes a number; one extra number (`BOS`) marks where a name starts and ends |
| **Autograd** (`class Value`) | Every arithmetic operation remembers where it came from, so the program can later walk backwards and find how much each number contributed to the error. It is the author's `micrograd`, built in |
| **Parameters** | The numbers the model learns: 1 layer, width 16, a context of 16 letters, 4 attention heads |
| **Model** | GPT-2 with small swaps: `rmsnorm` instead of `layernorm`, no biases, `ReLU` instead of `GeLU` |
| **Adam** | The optimizer that nudges every parameter after each step |
| **Training** | 1,000 steps: take a name, predict each next letter, measure the error, adjust |
| **Inference** | Generates names letter by letter; the `temperature` (0.5) sets how much it risks |

## How fast, and why

The same algorithm runs very differently depending on what runs it. [`microgpt.mjs`](microgpt.mjs) is `microgpt.py` translated line by line into JavaScript: the same `Value`, the same model, the same Adam, the same 1,000 steps. Only the random generator changes, so its names come in another order; that is why the table compares time per letter read.

```bash
python3 speed.py      # runs microgpt.py unchanged and times it
node microgpt.mjs
bun microgpt.mjs
```

What we measured on a Mac (Apple M4 Pro) on 6 November 2026, the median of three runs each:

| Runs it | Training | Letters read | Per letter | Against Python |
| --- | --- | --- | --- | --- |
| Python 3.15.2 (CPython) | 43.3 s | 7,170 | 6,042 µs | 1× |
| Node 26.13 (V8) | 5.9 s | 7,116 | 834 µs | 7.2× faster |
| Bun 1.4 (JavaScriptCore) | 3.3 s | 7,116 | 457 µs | 13.2× faster |

Python's time is the whole run (`speed.py` cannot reach inside the file it keeps unchanged); timing only the training loop in a copy gave 42.0 s of 42.1 s, so the difference is small. The runs repeat: every run of each one ended on the same error (2.6497 in Python, 2.2999 in JavaScript).

Where the difference comes from: the arithmetic is the same, number by number, so the gap is in how each machine executes it. CPython reads the program and executes it instruction by instruction, every time; V8 and JavaScriptCore notice the code that repeats (here, the millions of `Value` operations) and compile it into the processor's own instructions while it runs. That is a just-in-time compiler, and in this program it is worth 7 to 13 times.

None of the three does what real models do: every number here is still its own object, one at a time. The next step in speed, doing whole matrices at once, on a GPU, is what PyTorch is for; it is not measured here.

## Things to try

Change one line, run again, compare. Edit a copy (`cp microgpt.py experiment.py`) so the original stays intact.

- `temperature = 0.5` → `1.0`: stranger names. → `0.1`: safe, repetitive ones.
- `num_steps = 1000` → `3000`: lower error, more convincing names, three times the wait.
- `n_embd = 16` → `32`: a wider model; see how the parameter count and the time grow.
- Replace `input.txt` with your own list, one item per line (cities, product names, words in your language) and change nothing else.

## Learned from

- [microGPT-C](https://github.com/vixhal-baraiya/microgpt-c): measuring on names the model never saw, against a simple baseline (`evaluate.py`).
- [NamiGPT](https://github.com/aa1143/NamiGPT): following one tiny example from the first token to the last guess (`trace.py`).
- [microgpt-efficiency](https://github.com/chanjoongx/microgpt-efficiency): measuring the same algorithm in more than one implementation to show where speed comes from (`speed.py`, `microgpt.mjs`).

## Study next

1. [`micrograd`](https://github.com/karpathy/micrograd): only the autograd, explained.
2. [`nn-zero-to-hero`](https://github.com/karpathy/nn-zero-to-hero): the video course, from zero to GPT.
3. [`nanoGPT`](https://github.com/karpathy/nanoGPT): the same GPT in PyTorch, at real scale.
4. [`nanochat`](https://github.com/karpathy/nanochat): a whole ChatGPT, end to end.

And the book, in Brazilian Portuguese: [*IA por dentro*](https://ciromaciel.click/books/ia-por-dentro?ref=oss-study), on why the answer comes out in pieces, where what the model knows comes from and how it is trained.
