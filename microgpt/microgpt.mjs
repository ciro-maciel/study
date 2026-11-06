// microgpt.py, translated line by line into JavaScript, to measure where speed comes from (see SPEED.md).
// Same algorithm, same model (1 layer, 16 wide, 4 heads, context 16, 4,192 parameters), same Adam, same
// 1,000 steps. One difference: Python's random generator is replaced by a seeded one written here, so the
// names come in another order and the final loss differs a little. Runs on Node 22+ and on Bun:
//     node microgpt.mjs      bun microgpt.mjs
// Translated by Ciro Cesar Maciel from Andrej Karpathy's microgpt.py: the algorithm and its structure are his (see NOTICE).

import { readFileSync } from 'node:fs'

// A seeded generator (mulberry32) and Box-Muller for the bell curve: random.seed, random.gauss, shuffle, choices
let seed = 42 >>> 0
const random = () => {
    seed = (seed + 0x6d2b79f5) >>> 0
    let t = seed
    t = Math.imul(t ^ (t >>> 15), t | 1)
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61)
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
}
const gauss = (mean, std) => mean + std * Math.sqrt(-2 * Math.log(1 - random())) * Math.cos(2 * Math.PI * random())
const shuffle = list => {
    for (let i = list.length - 1; i > 0; i--) {
        const j = Math.floor(random() * (i + 1))
        ;[list[i], list[j]] = [list[j], list[i]]
    }
}
const choice = weights => {
    let r = random() * weights.reduce((a, b) => a + b, 0)
    for (let i = 0; i < weights.length; i++) if ((r -= weights[i]) <= 0) return i
    return weights.length - 1
}

// The dataset: the same input.txt, one name per line
const docs = readFileSync(new URL('./input.txt', import.meta.url), 'utf8').split('\n').map(l => l.trim()).filter(Boolean)
shuffle(docs)
console.log(`num docs: ${docs.length}`)

// The tokenizer: one id per character, plus BOS
const uchars = [...new Set(docs.join(''))].sort()
const BOS = uchars.length
const vocabSize = uchars.length + 1
console.log(`vocab size: ${vocabSize}`)

// Autograd: every number remembers its children and the local derivative towards each
class Value {
    constructor(data, children = [], localGrads = []) {
        this.data = data
        this.grad = 0
        this.children = children
        this.localGrads = localGrads
    }
    add(other) {
        other = other instanceof Value ? other : new Value(other)
        return new Value(this.data + other.data, [this, other], [1, 1])
    }
    mul(other) {
        other = other instanceof Value ? other : new Value(other)
        return new Value(this.data * other.data, [this, other], [other.data, this.data])
    }
    pow(other) { return new Value(this.data ** other, [this], [other * this.data ** (other - 1)]) }
    log() { return new Value(Math.log(this.data), [this], [1 / this.data]) }
    exp() { return new Value(Math.exp(this.data), [this], [Math.exp(this.data)]) }
    relu() { return new Value(Math.max(0, this.data), [this], [this.data > 0 ? 1 : 0]) }
    neg() { return this.mul(-1) }
    sub(other) { return this.add(other instanceof Value ? other.neg() : -other) }
    div(other) { return this.mul(other instanceof Value ? other.pow(-1) : 1 / other) }

    backward() {
        const topo = []
        const visited = new Set()
        const buildTopo = v => {
            if (visited.has(v)) return
            visited.add(v)
            for (const child of v.children) buildTopo(child)
            topo.push(v)
        }
        buildTopo(this)
        this.grad = 1
        for (let i = topo.length - 1; i >= 0; i--) {
            const v = topo[i]
            for (let c = 0; c < v.children.length; c++) v.children[c].grad += v.localGrads[c] * v.grad
        }
    }
}
// Python's sum() starts at 0, so the first addition is 0 + value: it creates one more node, and so does this
const sum = values => values.reduce((a, b) => (a instanceof Value ? a.add(b) : b.add(a)), 0)

// The parameters
const nLayer = 1
const nEmbd = 16
const blockSize = 16
const nHead = 4
const headDim = nEmbd / nHead
const matrix = (nout, nin, std = 0.08) => Array.from({ length: nout }, () => Array.from({ length: nin }, () => new Value(gauss(0, std))))
const state = { wte: matrix(vocabSize, nEmbd), wpe: matrix(blockSize, nEmbd), lm_head: matrix(vocabSize, nEmbd) }
for (let i = 0; i < nLayer; i++) {
    state[`layer${i}.attn_wq`] = matrix(nEmbd, nEmbd)
    state[`layer${i}.attn_wk`] = matrix(nEmbd, nEmbd)
    state[`layer${i}.attn_wv`] = matrix(nEmbd, nEmbd)
    state[`layer${i}.attn_wo`] = matrix(nEmbd, nEmbd)
    state[`layer${i}.mlp_fc1`] = matrix(4 * nEmbd, nEmbd)
    state[`layer${i}.mlp_fc2`] = matrix(nEmbd, 4 * nEmbd)
}
const params = Object.values(state).flatMap(mat => mat.flat())
console.log(`num params: ${params.length}`)

// The model
const linear = (x, w) => w.map(wo => sum(wo.map((wi, i) => wi.mul(x[i]))))
const softmax = logits => {
    const maxVal = Math.max(...logits.map(v => v.data))
    const exps = logits.map(v => v.sub(maxVal).exp())
    const total = sum(exps)
    return exps.map(e => e.div(total))
}
const rmsnorm = x => {
    const ms = sum(x.map(xi => xi.mul(xi))).div(x.length)
    const scale = ms.add(1e-5).pow(-0.5)
    return x.map(xi => xi.mul(scale))
}

function gpt(tokenId, posId, keys, values) {
    let x = state.wte[tokenId].map((t, i) => t.add(state.wpe[posId][i]))
    x = rmsnorm(x)
    for (let li = 0; li < nLayer; li++) {
        // 1) Multi-head attention
        let residual = x
        x = rmsnorm(x)
        const q = linear(x, state[`layer${li}.attn_wq`])
        const k = linear(x, state[`layer${li}.attn_wk`])
        const v = linear(x, state[`layer${li}.attn_wv`])
        keys[li].push(k)
        values[li].push(v)
        const xAttn = []
        for (let h = 0; h < nHead; h++) {
            const hs = h * headDim
            const qh = q.slice(hs, hs + headDim)
            const kh = keys[li].map(ki => ki.slice(hs, hs + headDim))
            const vh = values[li].map(vi => vi.slice(hs, hs + headDim))
            const attnLogits = kh.map(kt => sum(qh.map((qj, j) => qj.mul(kt[j]))).div(headDim ** 0.5))
            const attnWeights = softmax(attnLogits)
            for (let j = 0; j < headDim; j++) xAttn.push(sum(vh.map((vt, t) => attnWeights[t].mul(vt[j]))))
        }
        x = linear(xAttn, state[`layer${li}.attn_wo`]).map((a, i) => a.add(residual[i]))
        // 2) MLP
        residual = x
        x = rmsnorm(x)
        x = linear(x, state[`layer${li}.mlp_fc1`]).map(xi => xi.relu())
        x = linear(x, state[`layer${li}.mlp_fc2`]).map((a, i) => a.add(residual[i]))
    }
    return linear(x, state.lm_head)
}

// Adam
const learningRate = 0.01, beta1 = 0.85, beta2 = 0.99, epsAdam = 1e-8
const m = new Array(params.length).fill(0)
const v = new Array(params.length).fill(0)

// Training, timed. `positions` counts the letters the model read, so runs with names of other lengths compare fairly.
const numSteps = 1000
let positions = 0
const started = performance.now()
for (let step = 0; step < numSteps; step++) {
    const doc = docs[step % docs.length]
    const tokens = [BOS, ...[...doc].map(ch => uchars.indexOf(ch)), BOS]
    const n = Math.min(blockSize, tokens.length - 1)
    positions += n

    const keys = Array.from({ length: nLayer }, () => [])
    const values = Array.from({ length: nLayer }, () => [])
    const losses = []
    for (let posId = 0; posId < n; posId++) {
        const probs = softmax(gpt(tokens[posId], posId, keys, values))
        losses.push(probs[tokens[posId + 1]].log().neg())
    }
    const loss = sum(losses).mul(1 / n)

    loss.backward()

    const lrT = learningRate * (1 - step / numSteps)
    for (let i = 0; i < params.length; i++) {
        const p = params[i]
        m[i] = beta1 * m[i] + (1 - beta1) * p.grad
        v[i] = beta2 * v[i] + (1 - beta2) * p.grad ** 2
        const mHat = m[i] / (1 - beta1 ** (step + 1))
        const vHat = v[i] / (1 - beta2 ** (step + 1))
        p.data -= (lrT * mHat) / (vHat ** 0.5 + epsAdam)
        p.grad = 0
    }
    if (step + 1 === numSteps) console.log(`step ${step + 1} / ${numSteps} | loss ${loss.data.toFixed(4)}`)
}
const seconds = (performance.now() - started) / 1000
const runtime = typeof Bun !== 'undefined' ? `Bun ${Bun.version}` : `Node ${process.version}`
console.log(`${runtime}: ${seconds.toFixed(2)} s for ${positions} letters, ${((seconds * 1e6) / positions).toFixed(0)} µs per letter`)

// Inference
const temperature = 0.5
console.log('--- inference (new, hallucinated names) ---')
for (let sample = 0; sample < 20; sample++) {
    const keys = Array.from({ length: nLayer }, () => [])
    const values = Array.from({ length: nLayer }, () => [])
    let tokenId = BOS
    const out = []
    for (let posId = 0; posId < blockSize; posId++) {
        const probs = softmax(gpt(tokenId, posId, keys, values).map(l => l.div(temperature)))
        tokenId = choice(probs.map(p => p.data))
        if (tokenId === BOS) break
        out.push(uchars[tokenId])
    }
    console.log(`sample ${String(sample + 1).padStart(2)}: ${out.join('')}`)
}
