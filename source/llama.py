import ollama
from tqdm.auto import tqdm

client = ollama.Client(host='http://localhost:11434')



if __name__ == '__main__':

    response = ollama.chat(model='mistral', messages=[
    {
        'role': 'user',
        'content': 'Why is the sky blue?',
    },
    ])
    print(response['message']['content'])