"""
What a constitution does: microgpt writes names, a critic checks them against two written
principles, a reviser fixes the ones that break them, and the model is trained on its own
revised names. The same three steps as the supervised stage of Constitutional AI.
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import lab

PRINCIPLES = [
    ('at most 6 letters', lambda n: len(n) <= 6, lambda n: n[:6]),
    ("does not end in 'n'", lambda n: not n.endswith('n'), lambda n: n[:-1] + 'a' if n.endswith('n') else n),
]

def breaks(name):
    return [rule for rule, ok, _ in PRINCIPLES if not ok(name)]

def revise(name):
    for _, ok, fix in PRINCIPLES:
        if not ok(name):
            name = fix(name)
    return name

def report(names, moment):
    broken = sum(bool(breaks(n)) for n in names)
    distinct = len(set(names))
    print(f'{moment:23} | {100 * broken / len(names):5.1f}% break a principle | {distinct:3} different names out of {len(names)} | ' + ' '.join(names[:8]))

ns = lab.load()
lab.train(ns, ns['docs'], 1000)
drafts = lab.sample(ns, 300)
report(drafts, 'base model')
revised = [revise(n) for n in drafts if n]
examples = [(d, r) for d, r in zip(drafts, revised) if d != r][:5]
print('critique and revision:', '; '.join(f'{d} -> {r} ({", ".join(breaks(d))})' for d, r in examples))
lab.train(ns, revised, 300)
report(lab.sample(ns, 300), 'after its own revisions')
