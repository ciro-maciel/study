"""
What is a token: a byte-pair encoding (BPE) tokenizer in pure Python, no dependencies.
It trains on sample.en.md and sample.pt.md, the same text in English and in Portuguese
(this repository's README, frozen on 31 October 2026 so the numbers in the guide hold),
so you can see how words turn into pieces and why the language a tokenizer learned from
changes what a text costs.
"""

import os

HERE = os.path.dirname(os.path.abspath(__file__))
MERGES = 300 # how many new tokens the tokenizer learns on top of the 256 bytes

def read(name):
    with open(os.path.join(HERE, name), encoding='utf-8') as f:
        return f.read()

# Step 1: the microgpt way, one token per letter
def char_tokens(text):
    vocab = sorted(set(text))
    return [vocab.index(c) for c in text], vocab

# Step 2: the way real models do it. Start from the UTF-8 bytes (256 possible tokens),
# then repeatedly glue the most frequent pair of neighbours into one new token.
def most_frequent_pair(ids):
    counts = {}
    for pair in zip(ids, ids[1:]):
        counts[pair] = counts.get(pair, 0) + 1
    return max(counts, key=counts.get)

def merge(ids, pair, new_id):
    out, i = [], 0
    while i < len(ids):
        if i < len(ids) - 1 and (ids[i], ids[i + 1]) == pair:
            out.append(new_id)
            i += 2
        else:
            out.append(ids[i])
            i += 1
    return out

def train(text, merges):
    ids = list(text.encode('utf-8'))
    rules = {}
    pieces = {i: bytes([i]) for i in range(256)}
    for k in range(merges):
        pair = most_frequent_pair(ids)
        new_id = 256 + k
        ids = merge(ids, pair, new_id)
        rules[pair] = new_id
        pieces[new_id] = pieces[pair[0]] + pieces[pair[1]]
    return rules, pieces

def encode(text, rules):
    ids = list(text.encode('utf-8'))
    for pair, new_id in rules.items(): # rules are applied in the order they were learned
        ids = merge(ids, pair, new_id)
    return ids

def show(ids, pieces):
    # a piece that is only part of a letter (like one of the two bytes of "ç") is shown as hex
    def label(b):
        try:
            return b.decode('utf-8')
        except UnicodeDecodeError:
            return '<' + b.hex() + '>'
    return ' | '.join(label(pieces[i]) for i in ids)

en, pt = read('sample.en.md'), read('sample.pt.md')

print('--- 1. one token per letter (microgpt) ---')
ids, vocab = char_tokens('attention')
print(f"'attention' -> {ids}  ({len(ids)} tokens, vocabulary of {len(vocab)})")

print('\n--- 2. byte-pair encoding, trained on the English README ---')
rules, pieces = train(en, MERGES)
learned = [pieces[256 + k].decode('utf-8', errors='replace') for k in range(MERGES)]
print('first 12 pieces it learned:', [repr(p) for p in learned[:12]])
print('some long pieces it learned:', [repr(p) for p in sorted(learned, key=len)[-6:]])
for word in ['the code', 'microgpt', 'attention', 'atenção']:
    ids = encode(word, rules)
    print(f"{word!r:12} -> {len(ids):2} tokens: {show(ids, pieces)}")

print('\n--- 3. the same text, two languages, two tokenizers ---')
for trained_on, corpus in [('English', en), ('Portuguese', pt)]:
    rules, _ = train(corpus, MERGES)
    n_en, n_pt = len(encode(en, rules)), len(encode(pt, rules))
    print(f"trained on {trained_on:10}: English {n_en:5} tokens, Portuguese {n_pt:5} tokens,"
          f" Portuguese costs {100 * (n_pt - n_en) / n_en:+.0f}%")
print(f"(characters: English {len(en)}, Portuguese {len(pt)})")
