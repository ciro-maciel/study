# Notes for coding agents

This repository holds small reference programs, one folder each, kept exactly as their authors published them, with a guide next to each.

## Layout

| Path | What it is |
| --- | --- |
| `<folder>/<file>` | The original reference code, unchanged |
| `<folder>/README.md`, `<folder>/README.pt-BR.md` | The guide, in English and Brazilian Portuguese |
| `papers/` | Scientific papers as PDFs, unchanged from arXiv, with a reading guide |
| `notebook/` | The study notebook: one concept per folder in `notebook/concepts/`, plus `log.md` and `predictions.md` |
| `NOTICE` | Who wrote each original and where it comes from |

## Rules that must hold

- Never edit an original file; experiments go in a copy next to it, which is not committed.
- Each guide names the source link, the revision it was copied from and the sha256 of the file.
- Every number a guide states (time, parameters, loss, outputs) comes from a real run, with the date and the machine next to it. Rerun before you change one.
- Every guide exists in English and Brazilian Portuguese; a change to one changes the other.

## Keeping the notebook

The notebook is written and kept by the agent; the person asks, runs and decides. Sources (`microgpt/`, `papers/`) are never edited.

- **Start every session** by reading `notebook/README.md` (the ladder), `grep "^## \[" notebook/log.md | tail -10` and `notebook/predictions.md`, so you continue from where the last session stopped.
- **A concept page** is a folder `notebook/concepts/<concept>/` with `README.md` and `README.pt-BR.md`, always these sections in this order: In one sentence · How it works · What the paper says (short quotes with section and page) · The experiment · Why it matters · What we can build · Open questions. It links back to the notebook and forward to the next concept.
- **Every experiment** runs in pure Python in under a minute, on frozen sample data kept next to it, so its numbers never drift. Every number on a page comes from a real run, with the date and the machine. Test each "things to try" before you write what it does.
- **A good answer in the chat becomes a page or part of one**, never only a reply.
- **Log** every page, question, audit, prediction and idea in `notebook/log.md`, as `## [YYYY-MM-DD] kind | subject` plus one or two lines.
- **Predictions** are checkable in one sentence, have a check date, and are never edited after they are written; only the grade column is filled in later.
- **Audit** when asked, or every five pages: stale claims, contradictions between pages, concepts mentioned without a page, pages nothing links to. Log the audit and fix what is mechanical.
- **What we can build** stays general: no internal names, customers or plans. This repository is public.

## Before you say it works

```bash
cd <folder> && python3 <file>
```
