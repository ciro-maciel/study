"""
One name, from letters to the model's guesses.

Runs microgpt.py exactly as it is (it trains for 1,000 steps), then follows the name "emma"
through the trained model, one position at a time: the token that goes in, and the three
letters the model finds most likely next, with the probability it gave the right one.

The idea of following a single tiny example from start to end comes from NamiGPT
(https://github.com/aa1143/NamiGPT).

    python3 trace.py            # or: python3 trace.py anna
"""
import sys
import runpy

NAME = sys.argv[1] if len(sys.argv) > 1 else 'emma'
sys.argv = ['microgpt.py']
g = runpy.run_path('microgpt.py')
uchars, BOS, n_layer, gpt, softmax = g['uchars'], g['BOS'], g['n_layer'], g['gpt'], g['softmax']

show = lambda t: '<BOS>' if t == BOS else uchars[t]
tokens = [BOS] + [uchars.index(ch) for ch in NAME] + [BOS]
print(f'\n--- "{NAME}" as tokens: {tokens} ---')
keys, values = [[] for _ in range(n_layer)], [[] for _ in range(n_layer)]
for pos, (now, nxt) in enumerate(zip(tokens, tokens[1:])):
    probs = [p.data for p in softmax(gpt(now, pos, keys, values))]
    top = sorted(range(len(probs)), key=lambda i: -probs[i])[:3]
    guesses = ', '.join(f'{show(i)} {probs[i]:.0%}' for i in top)
    print(f'after {show(now):>5}  model guesses: {guesses:<28}  right answer {show(nxt)}: {probs[nxt]:.0%}')
