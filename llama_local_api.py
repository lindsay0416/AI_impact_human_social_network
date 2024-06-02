# import ollama

# response = ollama.chat(model='llama3', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sea blue?',
#   },
# ])
# print(response['message']['content'])


import ollama

stream = ollama.chat(
    model='llama3',
    messages=[{'role': 'user', 'content': 'Why are cats jump so high?'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)