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

## Things to try

Change one line, run again, compare. Edit a copy (`cp microgpt.py experiment.py`) so the original stays intact.

- `temperature = 0.5` → `1.0`: stranger names. → `0.1`: safe, repetitive ones.
- `num_steps = 1000` → `3000`: lower error, more convincing names, three times the wait.
- `n_embd = 16` → `32`: a wider model; see how the parameter count and the time grow.
- Replace `input.txt` with your own list, one item per line (cities, product names, words in your language) and change nothing else.

## Study next

1. [`micrograd`](https://github.com/karpathy/micrograd): only the autograd, explained.
2. [`nn-zero-to-hero`](https://github.com/karpathy/nn-zero-to-hero): the video course, from zero to GPT.
3. [`nanoGPT`](https://github.com/karpathy/nanoGPT): the same GPT in PyTorch, at real scale.
4. [`nanochat`](https://github.com/karpathy/nanochat): a whole ChatGPT, end to end.

And the book, in Brazilian Portuguese: [*IA por dentro*](https://ciromaciel.click/books/ia-por-dentro?ref=oss-study), on why the answer comes out in pieces, where what the model knows comes from and how it is trained.
