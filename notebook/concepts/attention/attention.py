"""
What is attention: train microgpt, then watch where each of its 4 attention heads looks
while it reads names it has never seen.
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import lab

ns = lab.load(watch_attention=True)
lab.train(ns, ns['docs'], 1000)
unseen = ns['docs'][-300:] # training used the first 1000 names; these 300 were never seen

# Average share of attention each head gives to: the start token, the current letter, the letter just before
share = {h: {'start': [], 'current': [], 'previous': []} for h in range(ns['n_head'])}
for name in unseen:
    ns['ATTENTION'].clear()
    lab.doc_loss(ns, name)
    pos = {}
    for li, h, weights in ns['ATTENTION']:
        t = pos.get(h, 0)
        pos[h] = t + 1
        if t < 2:
            continue # from the 3rd position on, start, previous and current are three different tokens
        share[h]['start'].append(weights[0])
        share[h]['current'].append(weights[t])
        share[h]['previous'].append(weights[t - 1])
print('--- where each head looks, averaged over 300 unseen names ---')
for h in range(ns['n_head']):
    s = {k: 100 * lab.mean(v) for k, v in share[h].items()}
    print(f"head {h}: start {s['start']:4.0f}% | previous letter {s['previous']:4.0f}% | current letter {s['current']:4.0f}% | the rest {100 - sum(s.values()):4.0f}%")

name = 'isabella'
ns['ATTENTION'].clear()
lab.doc_loss(ns, name)
tokens = ['.'] + list(name)
print(f"\n--- head by head, reading '{name}' ('.' is the start token) ---")
for h in range(ns['n_head']):
    print(f'head {h}')
    rows = [w for li, hh, w in ns['ATTENTION'] if hh == h]
    for t, weights in enumerate(rows):
        top = max(range(len(weights)), key=lambda i: weights[i])
        print(f"  at '{tokens[t]}' (predicting the next letter) looks most at '{tokens[top]}' ({100 * weights[top]:.0f}%)")
