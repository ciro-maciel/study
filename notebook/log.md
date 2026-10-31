# Log

One entry per event, newest last. Every entry starts with `## [YYYY-MM-DD] kind | subject`, so `grep "^## \[" log.md | tail -5` lists the last five. Kinds: `page`, `question`, `audit`, `prediction`, `idea`.

## [2026-10-31] page | notebook
Created the notebook: the ladder of nine concepts, this log and the predictions file.

## [2026-10-31] page | token
First page. Experiment `tokens.py`: a 300-merge BPE tokenizer trained on the repository README makes the same text cost 43% more tokens in Portuguese than in English; with 1,000 merges it memorizes the text and the gap reaches 216%.

## [2026-10-31] prediction | tokenizer gap
Claude's first prediction, to check on 2027-10-31.

## [2026-10-31] question | tokenizer gap on Claude
Measured with the API's token counter: the token page's samples cost 1,581 tokens in English and 1,837 in Portuguese on Claude Opus 5.5 and Claude Haiku 5.5 (identical counts), 16% more. Added as experiment 4 of the token page.

## [2026-10-31] prediction | tokenizer gap baseline
Prediction #1 ("at most 20% more") already holds today. It was made before measuring. Lesson on record in predictions.md: measure before you predict.

## [2026-10-31] page | lab
`lab.py` loads microgpt without editing it, with in-memory overrides and an attention hook. Checked: it reproduces the original run exactly (same 20 names, final loss 2.6497).

## [2026-10-31] page | embedding
After training, vowels end up alike (+0.53) and opposite to consonants (-0.29); before, all near 0.

## [2026-10-31] page | attention
The 4 heads learn different habits on 300 unseen names; "isabella" read head by head.

## [2026-10-31] page | gradient
Autograd matches the numerical slope (-3, -4). On the model, step 0.1 lowers the loss on one word; step 10 makes it explode to 24.

## [2026-10-31] page | training
Loss from 3.30 (random) to 2.28 in 1,000 steps; 2.34 on 200 unseen names.

## [2026-10-31] page | scale
Same steps, widths 4, 8, 16 and 32, measured on unseen names.

## [2026-10-31] page | fine-tuning
150 steps on "z" names: 100% "z" names, but loss on ordinary names 3.58, worse than guessing. Half-and-half mix: 92% and 2.50.

## [2026-10-31] page | constitution
Two written principles, a rule-based critic and reviser: violations 40% to 0%, distinct names 266 to 77; with 60 steps, 2% and 128.

## [2026-10-31] page | agents
The tool loop in Claude's message shape with a stand-in model; the program does the counting.

## [2026-10-31] idea | real model in the agent loop
Swap `decide()` in agents/agent.py for a call to Claude with the same two tools and compare its plan with the stand-in's. Spends tokens; needs Ciro's OK.
