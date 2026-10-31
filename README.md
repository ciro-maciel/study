# Study by Ciro Cesar Maciel

**Learn how AI works by running the smallest real code that does it, with a guide next to it.**

By [Ciro Cesar Maciel](https://ciromaciel.click/?ref=oss-study), author of [*IA por dentro*](https://ciromaciel.click/books/ia-por-dentro?ref=oss-study), the book that explains how chat AIs work on the inside.

[Português](README.pt-BR.md)

Each folder keeps one piece of reference code, the kind a researcher wrote to show the whole idea in as few lines as possible, exactly as its author published it, and adds what the original leaves to you: what each part does, how to run it, what it printed when we ran it, and what to study next.

## Start here: a whole GPT in 199 lines

```bash
git clone https://github.com/ciro-maciel/study && cd study/microgpt
python3 microgpt.py
```

[`microgpt/`](microgpt/) is Andrej Karpathy's microgpt: a complete GPT, with training and generation, in pure Python. No PyTorch, no NumPy, no GPU; only `os`, `math` and `random`. It reads 32,033 names, learns 4,192 numbers and then invents names that were not on the list.

On a Mac, with Python 3.15, training took **42 seconds**. The error went from 3.37 on the first step to about 2.2 at the end, and the model came up with `kamon`, `karai`, `vialan`, `yeran`, `keylen` and `alerin`.

The [guide](microgpt/README.md) walks the file top to bottom: the tokenizer, the autograd that lets it learn, the attention, the optimizer, the training loop and the sampling.

## What is here

| Folder | What you learn | Original by | Time to run |
| --- | --- | --- | --- |
| [`microgpt/`](microgpt/) | How a GPT is built and trained, every step visible | Andrej Karpathy | under a minute |
| [`papers/`](papers/) | The three scientific papers behind Claude: the Transformer, the scaling laws and Constitutional AI, with how to read each one next to the code | Google, OpenAI and Anthropic researchers | reading |

More folders come as the books need them. A good next folder is a small, complete, runnable piece of code that explains one idea; see [CONTRIBUTING.md](CONTRIBUTING.md).

## Why this exists

Most explanations of AI stop at analogies or jump straight into frameworks that hide the mechanism. Reference code like microgpt shows the whole mechanism, but it is written for people who already know what they are reading. This repository sits in between: the real code, run for real, explained in plain words, in English and in Brazilian Portuguese.

It is also the lab behind the book series *O Novo Básico*: [*IA por dentro*](https://ciromaciel.click/books/ia-por-dentro?ref=oss-study) explains in words how a model is trained; here you train one.

## More from Ciro Cesar Maciel

I build software on my own, with a team of AI agents, and open what I can.

- **[Books](https://ciromaciel.click/books?ref=oss-study)**: *O Novo Básico*, what everyone needs to know about AI to work, in Brazilian Portuguese, from the first conversation with an AI to the job of deploying it inside companies.
- **Six free, open-source Mac apps**, MIT, signed and notarized by Apple: [Cleaner](https://github.com/ciro-maciel/cleaner), [Screenshots](https://github.com/ciro-maciel/screenshots), [Speech to Text](https://github.com/ciro-maciel/speech-to-text), [Assistant](https://github.com/ciro-maciel/voice-assistant), [Windows](https://github.com/ciro-maciel/windows) and [Text to Speech](https://github.com/ciro-maciel/text-to-speech).
- **[Free tools for the browser](https://ciromaciel.click/tools?ref=oss-study)**, and [Infrastructure](https://myinfrastructure.click/?ref=oss-study), the infrastructure AI agents already know how to run.

**Follow along.** [Follow @ciro-maciel](https://github.com/ciro-maciel) and star this repository to see each new folder, and watch how it is all made on [YouTube](https://www.youtube.com/@ciro-maciel) and at [ciromaciel.click](https://ciromaciel.click/?ref=oss-study).

## License

The guides in this repository are MIT ([LICENSE](LICENSE)). The reference code in each folder belongs to its author, credited at the top of its guide and in [NOTICE](NOTICE).
