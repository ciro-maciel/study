"""
What an agent is: the loop around a model that lets it use tools. The model here is a
stand-in that follows a fixed plan, so the loop runs offline; the messages have the same
shape as Claude's tool use (tool_use, tool_result). Swap decide() for a real model call
and nothing else changes.
"""

import json
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import lab

ns = lab.load()
NAMES = ns['docs']

TOOLS = {
    'count_names': {
        'description': 'Counts the names in the dataset that start with a prefix.',
        'run': lambda args: sum(n.startswith(args['prefix']) for n in NAMES),
    },
    'longest_name': {
        'description': 'Returns the longest name in the dataset that starts with a prefix.',
        'run': lambda args: max((n for n in NAMES if n.startswith(args['prefix'])), key=len),
    },
}

def decide(messages):
    """Stand-in for the model: reads the conversation and returns its next message."""
    results = [m for m in messages if m['type'] == 'tool_result']
    if len(results) == 0:
        return {'type': 'tool_use', 'name': 'count_names', 'input': {'prefix': 'ka'}}
    if len(results) == 1:
        return {'type': 'tool_use', 'name': 'longest_name', 'input': {'prefix': 'ka'}}
    return {'type': 'text', 'text': f"{results[0]['content']} names start with 'ka'; the longest is {results[1]['content']}."}

messages = [{'type': 'user', 'text': "How many names start with 'ka', and which is the longest?"}]
print('user:', messages[0]['text'])
while True:
    reply = decide(messages)
    messages.append(reply)
    if reply['type'] == 'text':
        print('model:', reply['text'])
        break
    print('model asks for a tool:', json.dumps({'name': reply['name'], 'input': reply['input']}))
    result = TOOLS[reply['name']]['run'](reply['input'])
    messages.append({'type': 'tool_result', 'content': result})
    print('the program runs it and answers:', json.dumps(result))
print(f"{len(messages)} messages, {sum(m['type'] == 'tool_use' for m in messages)} tool calls")
