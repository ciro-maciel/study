# Agents

[Português](README.pt-BR.md) · [Notebook](../../README.md) · Previous: [constitution](../constitution/README.md) · End of the ladder

**In one sentence:** an agent is a language model inside a loop: instead of only answering, it can ask a program to run a tool, read the result and decide the next step, until the task is done.

## How it works

Everything the earlier pages showed ends in a model that generates text, one token at a time. On its own it cannot count the names in a spreadsheet, open a website or send an email. What it can do is **write a request** in an agreed format.

The agent loop has four steps:

1. **The person asks** for something.
2. **The model decides.** Either it answers directly, or it writes a tool request: the tool's name and its arguments (`tool_use`).
3. **The program runs it.** The model does not run the tool: the program around it does, and it can refuse, ask for confirmation or log everything. The result goes back into the conversation (`tool_result`).
4. **Repeat** until the model answers in text, asking for nothing more.

It is exactly the shape of Claude's API: the model returns a `tool_use` block, the program replies with a `tool_result` block, and the conversation goes on.

## Where it comes from

The ladder so far stood on the three papers in [`papers/`](../../../papers/README.md). Agents have no founding paper among them: it is a way of **using** the model, not of building it. What makes the loop possible is the earlier pages together: [training](../training/README.md) gives the model its knowledge, [fine-tuning](../fine-tuning/README.md) teaches it the format for asking for a tool, and the [constitution](../constitution/README.md) helps decide when a request is acceptable.

## The experiment

```bash
cd notebook/concepts/agents
python3 agent.py
```

[`agent.py`](agent.py) builds the whole loop with two tools over microgpt's 32,033 names: `count_names` (counts the names that start with a prefix) and `longest_name` (returns the longest). One important piece of honesty: **the model here is a stand-in**, a function (`decide()`) that follows a fixed plan, so the loop runs offline and at no cost. The messages have the same shape as Claude's; swapping `decide()` for a call to a real model changes nothing else in the program. On a Mac with Python 3.15, on 31 October 2026, it took under a second.

```
user: How many names start with 'ka', and which is the longest?
model asks for a tool: {"name": "count_names", "input": {"prefix": "ka"}}
the program runs it and answers: 1254
model asks for a tool: {"name": "longest_name", "input": {"prefix": "ka"}}
the program runs it and answers: "kamsiyochukwu"
model: 1254 names start with 'ka'; the longest is kamsiyochukwu.
6 messages, 2 tool calls
```

What the experiment shows:

- **The model counts nothing.** The numbers (1,254 and "kamsiyochukwu") come from the program. The model only decides what to ask for and how to put the answers together. That is why an agent gets right the counts a model alone would miss: remember it [does not even see the letters](../token/README.md).
- **The program is the one that runs.** Between the request and the execution there is a line of code that can say no. That is where an agent's safety and permissions live.
- **The final answer comes from the history.** On the third turn, the model answers by reading the two results already in the conversation.

**Things to try:** add a third tool to `TOOLS` (for example, the list of names with a prefix) and a third step in `decide()` that uses it.

## Why it matters

- **It is where AI leaves text and goes to work.** Querying a system, filling a form, editing a file: all of it is a model asking for tools in a loop.
- **It separates what the model knows from what it does.** Knowledge comes from training; action comes from the tools someone chose to give it. An agent is as useful and as safe as its tools and the rules of its loop.
- **It changes what is worth building.** Instead of a better model, what is missing is often the right tool and a well-kept loop.

## What we can build

- **Small, honest tools.** Each tool does one thing, with a clear name and description, and returns a checkable result, like the two in this experiment. That is what lets the model get it right.
- **The loop with a real model.** The natural next step for this notebook is to swap `decide()` for a call to Claude, with the same two tools, and compare: does the real model choose the same tools as the stand-in? That spends tokens, so it calls for a decision first.
- **Agents with a constitution.** Join this page with the previous one: the agent loop, with a list of principles the program checks before running each tool.

## Open questions

- The stand-in knows the right order of tools because someone wrote the plan. Would a real model, given only the descriptions in `TOOLS`, arrive at the same plan?
- Where is the line between what the program must check before running and what it can leave to the model?

This is the last page of the ladder. The next ones are born from the open questions of all of them.
