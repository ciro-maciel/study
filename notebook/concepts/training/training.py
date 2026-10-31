"""
What is training: the loop of predicting, missing and adjusting, watched from step 1 to
step 1000, with names sampled before and after.
"""

import math
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import lab

ns = lab.load()
print(f"guessing at random among {ns['vocab_size']} tokens costs ln({ns['vocab_size']}) = {math.log(ns['vocab_size']):.2f}")
print('names before training:', ' '.join(lab.sample(ns, 8)))
history = lab.train(ns, ns['docs'], 1000)
print('--- average loss per 100 steps ---')
for i in range(0, 1000, 100):
    chunk = history[i:i + 100]
    print(f'steps {i + 1:4}-{i + 100:4}: {lab.mean(chunk):.2f} ' + '#' * round(20 * lab.mean(chunk) / 3.5))
unseen = ns['docs'][-200:]
print(f'loss on 200 names it never saw: {lab.mean([lab.doc_loss(ns, w).data for w in unseen]):.2f}')
print('names after training: ', ' '.join(lab.sample(ns, 8)))
