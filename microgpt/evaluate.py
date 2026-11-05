"""
Did microgpt learn names, or memorize the ones it saw?

Runs microgpt.py exactly as it is (it trains on the first 1,000 names of the shuffled list),
then measures the average error per letter (the same loss the training prints) on:

- names it trained on, and names it never saw;
- two baselines on the same unseen names: guessing every letter at random, and a bigram
  (each letter predicted only from the one before), counted on the same 1,000 names.

The idea of measuring on held-out names against a simple baseline comes from microGPT-C
(https://github.com/vixhal-baraiya/microgpt-c).

    python3 evaluate.py
"""
import math
import runpy

g = runpy.run_path('microgpt.py')  # trains and prints its 20 names, unchanged
docs, uchars, BOS, vocab_size = g['docs'], g['uchars'], g['BOS'], g['vocab_size']
gpt, softmax, n_layer, block_size = g['gpt'], g['softmax'], g['n_layer'], g['block_size']

TRAIN = docs[:1000]          # what the 1,000 training steps saw (docs[step % len(docs)])
HELD_OUT = docs[1000:1500]   # 500 names the model never saw
SAMPLE = 500


def pairs(name):
    """(previous token, next token) for every position the training loss counts."""
    tokens = [BOS] + [uchars.index(ch) for ch in name] + [BOS]
    n = min(block_size, len(tokens) - 1)
    return [(tokens[i], tokens[i + 1]) for i in range(n)], tokens


def model_loss(names):
    total, count = 0.0, 0
    for name in names:
        steps, tokens = pairs(name)
        keys, values = [[] for _ in range(n_layer)], [[] for _ in range(n_layer)]
        for pos_id, (token_id, target_id) in enumerate(steps):
            probs = softmax(gpt(token_id, pos_id, keys, values))
            total += -math.log(probs[target_id].data)
            count += 1
    return total / count


# Bigram counted on the training names, with add-one smoothing so no letter has probability zero.
counts = [[1] * vocab_size for _ in range(vocab_size)]
for name in TRAIN:
    for a, b in pairs(name)[0]:
        counts[a][b] += 1


def bigram_loss(names):
    total, count = 0.0, 0
    for name in names:
        for a, b in pairs(name)[0]:
            total += -math.log(counts[a][b] / sum(counts[a]))
            count += 1
    return total / count


print('\n--- evaluation: average error per letter (lower is better) ---')
print(f'random guess, {vocab_size} options     {math.log(vocab_size):.4f}')
print(f'bigram, unseen names            {bigram_loss(HELD_OUT):.4f}')
print(f'microgpt, names it trained on   {model_loss(TRAIN[:SAMPLE]):.4f}')
print(f'microgpt, names it never saw    {model_loss(HELD_OUT):.4f}')
