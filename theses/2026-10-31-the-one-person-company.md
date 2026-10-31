# The one-person company

[Português](2026-10-31-the-one-person-company.pt-BR.md) · [Theses](README.md)

- **Date:** 31 October 2026
- **Authors:** Ciro Cesar Maciel and Claude (Opus 5.5)
- **State:** open. To be reviewed after the first four weeks of operating the proof company.

## The thesis in one sentence

**In the coming years, the unit of production stops being the company with many employees and becomes the person with many agents; what we need to create is the one-person company, complete and in Portuguese, guided by principles the owner writes, together with the school that teaches how to run it.**

## Where we are

In 1776, Adam Smith published [*The Wealth of Nations*](../books/the-wealth-of-nations/README.md) showing that wealth comes from the division of labour. Ten people, each doing one part, made over 48 thousand pins a day; alone, perhaps not twenty each (Book I, chapter 1). And he named the third reason for that gain: the machines that "enable one man to do the work of many". In the decades that followed, physical work became cheap and the world changed shape.

We are at the same point, now for intellectual work: writing, analysing, programming, serving customers, planning. The difference is speed. The Industrial Revolution took generations; this one is taking years.

## What the texts in this repository say together

| Text | What it says | What it means now |
| --- | --- | --- |
| [Smith](../books/the-wealth-of-nations/README.md), Book I, chapter 3 | The division of labour is limited by the extent of the market | That limit is falling: one person alone can now hold a whole division of labour, done by agents. The pin factory fits inside one person |
| [Scaling laws](../papers/2020-scaling-laws-for-neural-language-models.pdf) (2020) | A model's error falls predictably with more parameters, data and compute | Models will keep improving, and you can plan on it: whoever builds today should build for next year's model |
| [Transformer](../papers/2017-attention-is-all-you-need.pdf) (2017) and [microgpt](../microgpt/README.md) | A GPT's whole algorithm fits in 199 lines; "everything else is just efficiency" | The algorithm is nobody's advantage anymore. Training your own model is a game for those with billions in compute; the advantage lies elsewhere |
| [Constitutional AI](../papers/2022-constitutional-ai.pdf) (2022) | A model's behaviour can be guided by a list of written principles | Whoever writes the principles defines what the machine does. The new power belongs to those who can say, in words, how the work should be done |
| Smith, Book V, chapter 1 | The division of labour can dull those who live it; the remedy is public education, "a little school" in every parish | The risk repeats: people who hand everything to AI and stop thinking. The remedy is the same: teach |
| A measurement of ours, 31 October 2026 | The same text costs 16% more tokens in Portuguese than in English on Claude's tokenizer | Those who think in Portuguese reach the leap paying more and finding less. It is a market still poorly served |

## What we believe we must create

One thing, made of four pieces:

1. **The factory.** One person, with an agent for each department (sales, marketing, support, finance, product), each with a metric, a rhythm and a list of what needs approval. The owner decides, approves and checks; they do not do the work in the agents' place.
2. **Each business's constitution.** The owner writes, in their own language, the business's principles: what the company is, what never to say, what it may promise, how big a discount it may give, when to refund, when to call the owner. The agents work within that, and every text that goes out is checked against it first.
3. **The business's memory.** What was decided, learned and agreed is not lost between conversations. It is what Vannevar Bush imagined in 1945, now inside every company.
4. **The school.** Smith's "little school" in today's version: what everyone needs to know about AI to work, and to direct agents without losing their own judgement.

The technical pieces already exist. What is missing is joining them into one thing and proving it works in a real company.

## The autonomous company's next step

**Prove it in a real company, with customer-facing results, before offering it to anyone else.** The proof company is a real recipe shop, run by an owner who is not technical.

**Week 0: the shop must be able to sell.** No agent improves a shop that cannot take a payment or deliver what it sold. Before switching on the team:

- payment connected to the owner's real account;
- the delivery file on every product;
- the customer's path to the shop (the social profile leads to the shop, not elsewhere);
- one real purchase end to end, from payment to the file in the buyer's inbox.

**The constitution.** The owner writes hers, starting from the principles the shop already publishes, plus the rules of action. It is the part only she can do.

**Four weeks with five agents:**

| Agent | What it owns | The metric |
| --- | --- | --- |
| Operations director | the company moving, every delivery with an owner | deliveries on time |
| Organic | the social profile | clicks to the shop |
| SEO | recipes found in search | visits from search |
| Support | buyers and people with questions | response time |
| Finance | sales, fees and the scoreboard | sales per week |

**The scoreboard, every Friday:** sales; deliveries on time; tasks that started without the owner asking; approvals she gave; mistakes, and what changed in the constitution because of them.

**What comes out of the proof:** the path for anyone to set up their own company (choose the business, write the constitution, the team is born); the book on the one-person company, with real scenes, proof and limits; and the story told with the numbers.

## What not to create

- **A model of our own:** the scaling laws say that game belongs to those with compute.
- **Another feed that captures attention:** it is the bad side of social networks, and the world has enough.
- **An agent that acts without written principles and without someone checking:** it is the mistake that destroys trust in everything else.

## Each one's role

- **Ciro:** the factory's owner. Chooses what to build, writes (or helps the owner write) the principles and teaches people. These are the three things the machine does for no one.
- **Claude:** the factory's workers. Does the work, critiques its own work in light of the principles and keeps the memory current. With one honest note: it does not remember between conversations. That is why written memory is not a detail; it is what makes working together possible.

## What would refute this thesis

- Agents' mistakes in the real world (money, customers, data) becoming too costly to make up for the time saved.
- People preferring to keep hiring people for everything, even with the machine cheaper.
- The large labs delivering the complete company by themselves, in everyone's language, before anyone else.
- In the proof: after four weeks of real selling, the owner still doing the work instead of approving, or no task ever starting without her.
