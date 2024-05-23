from openai import OpenAI
from dotenv import load_dotenv
from os import environ

# 1. ChatGPT API - https://platform.openai.com/docs/overview


if __name__ == "__main__":
    load_dotenv()
    print(environ.get("OPENAI_API_KEY"))
    client = OpenAI()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Your name is Frederick"},
        {"role": "user", "content": "Whats your name?"}
    ],
    max_tokens= 60
    )
    print(completion.choices[0].message)