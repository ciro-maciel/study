# Notes for coding agents

This repository holds small reference programs, one folder each, kept exactly as their authors published them, with a guide next to each.

## Layout

| Path | What it is |
| --- | --- |
| `<folder>/<file>` | The original reference code, unchanged |
| `<folder>/README.md`, `<folder>/README.pt-BR.md` | The guide, in English and Brazilian Portuguese |
| `NOTICE` | Who wrote each original and where it comes from |

## Rules that must hold

- Never edit an original file; experiments go in a copy next to it, which is not committed.
- Each guide names the source link, the revision it was copied from and the sha256 of the file.
- Every number a guide states (time, parameters, loss, outputs) comes from a real run, with the date and the machine next to it. Rerun before you change one.
- Every guide exists in English and Brazilian Portuguese; a change to one changes the other.

## Before you say it works

```bash
cd <folder> && python3 <file>
```
