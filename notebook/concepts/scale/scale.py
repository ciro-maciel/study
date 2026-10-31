"""
What scale does: the same microgpt at three widths, same 1000 steps, measured on names
none of them saw.
"""

import time
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import lab

ns0 = lab.load()
unseen = ns0['docs'][-200:]
print('--- same data, same steps, three sizes ---')
for width in [4, 8, 16]:
    start = time.time()
    ns = lab.load(n_embd=width)
    lab.train(ns, ns['docs'], 1000)
    loss = lab.mean([lab.doc_loss(ns, w).data for w in unseen])
    print(f"width {width:2} | {len(ns['params']):5} parameters | loss on unseen names {loss:.3f} | {time.time() - start:4.0f} s")
