"""
What fine-tuning does: train microgpt on all names, then keep training it for 150 steps
two ways, on names that start with 'z' only, and on a half-and-half mix, and measure what
changed and what was lost.
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import lab

def share_starting_with(names, letter):
    return 100 * sum(n.startswith(letter) for n in names) / len(names)

ns = lab.load()
lab.train(ns, ns['docs'], 1000)
general = ns['docs'][-200:]
z_names = [d for d in ns['docs'][1000:-200] if d.startswith('z')]
print(f'{len(z_names)} names start with z in the data the base model did not train on')
base_samples = lab.sample(ns, 200)
base_loss = lab.mean([lab.doc_loss(ns, w).data for w in general])
print(f"{'base model':20} | names starting with z: {share_starting_with(base_samples, 'z'):5.1f}% | loss on general names {base_loss:.3f}")
base_weights = [p.data for p in ns['params']]
others = [d for d in ns['docs'][1000:-200] if not d.startswith('z')]
mix = [w for pair in zip(z_names, others) for w in pair]
for label, data in [('z names only', z_names), ('half z, half others', mix)]:
    for p, w in zip(ns['params'], base_weights):
        p.data = w # every run starts from the same base model
    lab.train(ns, data, 150)
    tuned_samples = lab.sample(ns, 200)
    tuned_loss = lab.mean([lab.doc_loss(ns, w).data for w in general])
    print(f"{label:20} | names starting with z: {share_starting_with(tuned_samples, 'z'):5.1f}% | loss on general names {tuned_loss:.3f}")
    print('   sample:', ' '.join(tuned_samples[:10]))
