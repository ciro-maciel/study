# Contributing

Thanks for helping. The bar here is "someone who has never seen this code runs it and understands it".

## A new folder

A good folder takes one small, complete piece of code that explains one idea and runs on a laptop in minutes. It has:

- `get.sh`, which downloads the original from its author, pinned to one revision (a commit or gist revision, never a branch), and refuses to keep it unless the sha256 matches. The original is never committed;
- `README.md` in English and `README.pt-BR.md` in Brazilian Portuguese, with the same content: what it is, the author and the link, how to run it, a table of what we saw when we ran it (with the date and the machine), what each part of the file does, things to try and what to study next;
- an entry in `.gitignore` for the downloaded file and an entry in `NOTICE`.

Tell us in the pull request which machine you ran it on and paste what it printed.

## A better explanation

If a sentence in a guide is wrong or unclear, a pull request that fixes it in both languages is the most useful contribution you can make.

## Before you open the pull request

```bash
cd <folder> && ./get.sh && python3 <file>
```

It must run from a fresh clone, with nothing else installed beyond what the guide says.
