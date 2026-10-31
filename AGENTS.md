# Notes for coding agents

This repository holds small reference programs, one folder each, kept exactly as their authors published them, with a guide next to each.

## Layout

| Path | What it is |
| --- | --- |
| `<folder>/<file>` | The original reference code, unchanged |
| `<folder>/README.md`, `<folder>/README.pt-BR.md` | The guide, in English and Brazilian Portuguese |
| `papers/` | Scientific papers as PDFs, unchanged from arXiv, with a reading guide |
| `brain/` | The shared brain: `leaps/`, `patterns/`, `frontier/`, `books/` and `log.md` |
| `notebook/` | The study notebook: one concept per folder in `notebook/concepts/`, plus `log.md` and `predictions.md` |
| `NOTICE` | Who wrote each original and where it comes from |

## Rules that must hold

- Never edit an original file; experiments go in a copy next to it, which is not committed.
- Each guide names the source link, the revision it was copied from and the sha256 of the file.
- Every number a guide states (time, parameters, loss, outputs) comes from a real run, with the date and the machine next to it. Rerun before you change one.
- Every guide exists in English and Brazilian Portuguese; a change to one changes the other.

## Keeping the brain

The brain is kept by the agent from what the person brings (a video, a paper, a book, an idea); the person decides what is worth building. It is the main thing in this repository.

- **Start every brain session** by reading `brain/README.md`, `brain/patterns/README.md`, `brain/frontier/README.md` and `grep "^## \[" brain/log.md | tail -10`.
- **When something comes in**, update every leap page it touches, revisit the patterns, and say in the log and in the reply whether each frontier hypothesis got stronger or weaker, and why. A source never stays only as a summary: it changes the pages it touches.
- **A leap page** (`brain/leaps/<leap>.md` and `.pt-BR.md`) has: in one sentence · what existed before · the leap (a dated table) · the analysis (what became cheap, the open layer, the interface for people, what it connected, the bad side) · sources · links to patterns and frontier.
- **A book** gets `brain/books/<book>/` with the full text when it is in the public domain, unchanged, and a reading page with the passages that matter, each with its exact location (book and chapter), and how it reads the leaps.
- **Every statement of fact has a source** you could read. Check each date against it before writing. Opinion and hypothesis are marked as such.
- **The bad side of each leap goes in with the good.**
- **A frontier hypothesis** says which patterns point to it, what can be seen, what would refute it and what we can build. It is never deleted: when refuted, it gets the date and the reason.

## Keeping the notebook

The notebook is written and kept by the agent; the person asks, runs and decides. Sources (`microgpt/`, `papers/`) are never edited.

- **Start every session** by reading `notebook/README.md` (the ladder), `grep "^## \[" notebook/log.md | tail -10` and `notebook/predictions.md`, so you continue from where the last session stopped.
- **A concept page** is a folder `notebook/concepts/<concept>/` with `README.md` and `README.pt-BR.md`, always these sections in this order: In one sentence · How it works · What the paper says (short quotes with section and page) · The experiment · Why it matters · What we can build · Open questions. It links back to the notebook and forward to the next concept.
- **Every experiment** runs in pure Python on a laptop, ideally in under a minute, and the page states how long it took. It runs on fixed data, so its numbers never drift: microgpt's names (pinned by microgpt itself) through `notebook/lab.py`, or a frozen sample kept next to it. Every number on a page comes from a real run, with the date and the machine. Test each "things to try" before you write what it does.
- **`notebook/lab.py`** is how experiments use microgpt: it loads the original file without editing it, with in-memory overrides. If you change `lab.py`, check that `lab.train(ns, ns["docs"], 1000)` followed by `lab.sample(ns, 20)` still gives the original run's names (`kamon ann karai ...`) and final loss 2.6497.
- **A good answer in the chat becomes a page or part of one**, never only a reply.
- **Log** every page, question, audit, prediction and idea in `notebook/log.md`, as `## [YYYY-MM-DD] kind | subject` plus one or two lines.
- **Predictions** are checkable in one sentence, have a check date, and are never edited after they are written; only the grade column is filled in later.
- **Audit** when asked, or every five pages: stale claims, contradictions between pages, concepts mentioned without a page, pages nothing links to. Log the audit and fix what is mechanical.
- **What we can build** stays general: no internal names, customers or plans. This repository is public.

## Before you say it works

```bash
cd <folder> && python3 <file>
```
