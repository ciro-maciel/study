"""
How fast is microgpt, and where does speed come from?

Runs microgpt.py exactly as it is and times the whole run, then counts the letters the 1,000
training steps read, so it compares fairly with microgpt.mjs, the same algorithm translated line
by line into JavaScript (its names come in another order, so it reads a few letters fewer):

    python3 speed.py
    node microgpt.mjs
    bun microgpt.mjs

The idea of measuring the same algorithm in several implementations comes from
microgpt-efficiency (https://github.com/chanjoongx/microgpt-efficiency).
"""
import runpy
import sys
import time

started = time.perf_counter()
g = runpy.run_path('microgpt.py')  # trains and prints its 20 names, unchanged
seconds = time.perf_counter() - started

docs, block_size = g['docs'], g['block_size']
letters = sum(min(block_size, len(doc) + 1) for doc in docs[:1000])  # docs[step % len(docs)], 1,000 steps
print(f"\nPython {sys.version.split()[0]}: {seconds:.2f} s for {letters} letters, {seconds * 1e6 / letters:.0f} µs per letter")
