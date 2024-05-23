import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display # type: ignore
from IPython.display import Markdown # type: ignore


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


if __name__ == '__main__':
  model = genai.GenerativeModel('gemini-pro')
  response = model.generate_content("What is the meaning of life?")
  print(response.text)