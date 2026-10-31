"""
What is a gradient: microgpt's own autograd (class Value) on a tiny formula, checked
against the slow way of measuring a slope, and then on the real model.
"""

import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import lab

ns = lab.load()
Value = ns['Value']

print('--- 1. a tiny formula: f = a * b + b ** 2 ---')
a, b = Value(2.0), Value(-3.0)
f = a * b + b ** 2
f.backward()
print(f'f = {f.data}')
print(f'autograd says: df/da = {a.grad}, df/db = {b.grad}')
h = 1e-6
fa = lambda x, y: x * y + y ** 2
print(f'nudging by {h}: df/da = {(fa(2 + h, -3) - fa(2, -3)) / h:.4f}, df/db = {(fa(2, -3 + h) - fa(2, -3)) / h:.4f}')

print('\n--- 2. the real model, one word ---')
word = 'emma'
loss = lab.doc_loss(ns, word)
loss.backward()
params = ns['params']
grads = [p.grad for p in params]
biggest = max(range(len(params)), key=lambda i: abs(grads[i]))
print(f"loss on '{word}' before: {loss.data:.4f}")
others = ns['docs'][-200:]
others_before = lab.mean([lab.doc_loss(ns, w).data for w in others])
nonzero = sum(g != 0 for g in grads)
print(f'{nonzero} of {len(params)} parameters got a gradient other than zero; the largest is {grads[biggest]:+.4f}')
print(f'loss on 200 other names before: {others_before:.4f}')
for step_size in [0.01, 0.1, 1.0, 10.0]:
    for p, g in zip(params, grads):
        p.data -= step_size * g
    after = lab.doc_loss(ns, word).data
    others_after = lab.mean([lab.doc_loss(ns, w).data for w in others])
    for p, g in zip(params, grads):
        p.data += step_size * g
    print(f"step against the gradient, size {step_size:<4}: '{word}' {after:.4f} ({after - loss.data:+.4f}) | other names {others_after:.4f} ({others_after - others_before:+.4f})")
