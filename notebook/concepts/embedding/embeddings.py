"""
What is an embedding: train microgpt, then look at the list of 16 numbers it learned for
each letter. Nobody tells the model what a vowel is; see whether it finds out.
"""

import itertools
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import lab

VOWELS = 'aeiou'

def letter_vectors(ns):
    return {c: [v.data for v in ns['state_dict']['wte'][i]] for i, c in enumerate(ns['uchars'])}

def report(ns, moment):
    vecs = letter_vectors(ns)
    consonants = [c for c in ns['uchars'] if c not in VOWELS]
    vv = lab.mean([lab.cosine(vecs[a], vecs[b]) for a, b in itertools.combinations(VOWELS, 2)])
    vc = lab.mean([lab.cosine(vecs[a], vecs[b]) for a in VOWELS for b in consonants])
    cc = lab.mean([lab.cosine(vecs[a], vecs[b]) for a, b in itertools.combinations(consonants, 2)])
    print(f'--- {moment} training ---')
    print(f'similarity vowel-vowel {vv:+.2f} | vowel-consonant {vc:+.2f} | consonant-consonant {cc:+.2f}')
    for letter in 'aekn':
        nearest = sorted((c for c in ns['uchars'] if c != letter), key=lambda c: -lab.cosine(vecs[letter], vecs[c]))
        print(f"nearest to '{letter}': {' '.join(nearest[:4])}")
    print('the 16 numbers of a:', ' '.join(f'{x:+.2f}' for x in vecs['a']))

ns = lab.load()
report(ns, 'before')
lab.train(ns, ns['docs'], 1000)
report(ns, 'after')
