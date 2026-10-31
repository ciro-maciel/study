# Notes for coding agents

This repository holds guides to small reference programs, one folder each. It holds no third-party code: each folder's `get.sh` downloads the original from its author.

## Layout

| Path | What it is |
| --- | --- |
| `<folder>/get.sh` | Downloads the original, pinned to one revision, checks the sha256 |
| `<folder>/README.md`, `<folder>/README.pt-BR.md` | The guide, in English and Brazilian Portuguese |
| `NOTICE` | Who owns each downloaded file and where it comes from |

## Rules that must hold

- Never commit a downloaded file. Each one is listed in `.gitignore`.
- Never edit a downloaded file in place; experiments go in a copy next to it.
- A pin is a commit or gist revision plus a sha256, never a branch name.
- Every number a guide states (time, parameters, loss, outputs) comes from a real run, with the date and the machine next to it. Rerun before you change one.
- Every guide exists in English and Brazilian Portuguese; a change to one changes the other.

## Before you say it works

```bash
cd <folder> && ./get.sh && python3 <file>
```
