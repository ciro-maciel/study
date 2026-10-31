"""
The notebook's lab: loads microgpt.py as published, changes in memory only what an
experiment needs (a hyperparameter, a hook), and gives back the pieces to play with.
The file on disk is never modified. train() and sample() follow microgpt's own training
loop and inference, rewritten to return numbers instead of printing them.
"""

import contextlib
import io
import math
import os
import random
import re

HERE = os.path.dirname(os.path.abspath(__file__))
MICROGPT_DIR = os.path.join(HERE, '..', 'microgpt')
MICROGPT = os.path.join(MICROGPT_DIR, 'microgpt.py')
TRAINING_STARTS = '# Repeat in sequence'
ATTENTION_LINE = 'attn_weights = softmax(attn_logits)'

def load(watch_attention=False, **overrides):
    """Runs microgpt up to (not including) its training loop and returns its namespace.
    overrides replace top-level assignments, e.g. load(n_embd=8)."""
    with open(MICROGPT, encoding='utf-8') as f:
        source = f.read().split(TRAINING_STARTS)[0]
    for name, value in overrides.items():
        source, count = re.subn(rf'^{name} = [^#\n]+', f'{name} = {value!r} ', source, flags=re.M)
        assert count == 1, f'{name} is not a top-level setting of microgpt'
    if watch_attention:
        source = source.replace(ATTENTION_LINE, ATTENTION_LINE + '; ATTENTION.append((li, h, [w.data for w in attn_weights]))')
    ns = {'__name__': 'microgpt', 'ATTENTION': []}
    cwd = os.getcwd()
    os.chdir(MICROGPT_DIR) # input.txt is downloaded and cached next to microgpt.py
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(source, MICROGPT, 'exec'), ns)
    finally:
        os.chdir(cwd)
    return ns

def tokens_of(ns, word):
    return [ns['BOS']] + [ns['uchars'].index(ch) for ch in word] + [ns['BOS']]

def doc_loss(ns, word):
    """Average loss of the model on one word, as a Value (so it can be backpropagated)."""
    tokens = tokens_of(ns, word)
    n = min(ns['block_size'], len(tokens) - 1)
    keys, values = [[] for _ in range(ns['n_layer'])], [[] for _ in range(ns['n_layer'])]
    losses = []
    for pos_id in range(n):
        logits = ns['gpt'](tokens[pos_id], pos_id, keys, values)
        probs = ns['softmax'](logits)
        losses.append(-probs[tokens[pos_id + 1]].log())
    return (1 / n) * sum(losses)

def train(ns, docs, num_steps, learning_rate=0.01, beta1=0.85, beta2=0.99, eps=1e-8):
    """microgpt's training loop: one word per step, Adam, linear learning-rate decay.
    Returns the loss of every step. Can be called again to keep training (fine-tuning)."""
    params = ns['params']
    m, v = [0.0] * len(params), [0.0] * len(params)
    history = []
    for step in range(num_steps):
        loss = doc_loss(ns, docs[step % len(docs)])
        loss.backward()
        lr_t = learning_rate * (1 - step / num_steps)
        for i, p in enumerate(params):
            m[i] = beta1 * m[i] + (1 - beta1) * p.grad
            v[i] = beta2 * v[i] + (1 - beta2) * p.grad ** 2
            m_hat = m[i] / (1 - beta1 ** (step + 1))
            v_hat = v[i] / (1 - beta2 ** (step + 1))
            p.data -= lr_t * m_hat / (v_hat ** 0.5 + eps)
            p.grad = 0
        history.append(loss.data)
    return history

def sample(ns, count=20, temperature=0.5):
    """microgpt's inference: generate count names, letter by letter."""
    names = []
    for _ in range(count):
        keys, values = [[] for _ in range(ns['n_layer'])], [[] for _ in range(ns['n_layer'])]
        token_id, letters = ns['BOS'], []
        for pos_id in range(ns['block_size']):
            logits = ns['gpt'](token_id, pos_id, keys, values)
            probs = ns['softmax']([l / temperature for l in logits])
            token_id = random.choices(range(ns['vocab_size']), weights=[p.data for p in probs])[0]
            if token_id == ns['BOS']:
                break
            letters.append(ns['uchars'][token_id])
        names.append(''.join(letters))
    return names

def mean(xs):
    return sum(xs) / len(xs)

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    return dot / (math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b)))
