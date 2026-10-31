# Log

One entry per event, newest last. Every entry starts with `## [YYYY-MM-DD] kind | subject`, so `grep "^## \[" log.md | tail -5` lists the last five. Kinds: `page`, `question`, `audit`, `prediction`, `idea`.

## [2026-10-31] page | notebook
Created the notebook: the ladder of nine concepts, this log and the predictions file.

## [2026-10-31] page | token
First page. Experiment `tokens.py`: a 300-merge BPE tokenizer trained on the repository README makes the same text cost 43% more tokens in Portuguese than in English; with 1,000 merges it memorizes the text and the gap reaches 216%.

## [2026-10-31] prediction | tokenizer gap
Claude's first prediction, to check on 2027-10-31.
