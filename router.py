import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display
from rich.console import Console
from rich.markdown import Markdown
from langchain_openai import ChatOpenAI
console=Console()

#Loading API Secrets from env files
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
openrouter_url = "https://openrouter.ai/api/v1"
ollama_url = "http://localhost:11434/v1"

# Defining print statement to print markdown in terminal
def printmd(text):
    markdown_text=text
    md = Markdown(markdown_text)
    console.print(md)

#Initializing Ollama and OpenRouter Clients
openai = OpenAI()
openrouter = OpenAI(base_url=openrouter_url, api_key=openrouter_api_key)
ollama = OpenAI(api_key="ollama", base_url=ollama_url)

#Prompts
easy_puzzle = [
    {"role": "user", "content":
        "You toss 2 coins. One of them is heads. What's the probability the other is tails? Answer with the probability only."},
]

tell_a_joke = [
    {"role": "user", "content": "Tell a joke for a student on the journey to becoming an expert in LLM Engineering"},
]

#Making API Calls using native libraries, routers and abstractions

#Using Ollama
#response = ollama.chat.completions.create(model="llama3.2", messages=easy_puzzle)

#Using Open Router
#response = openrouter.chat.completions.create(model="openrouter/free", messages=tell_a_joke)

#Using LangChain
#llm = ChatOpenAI(model="gpt-5-mini")
#response = llm.invoke(tell_a_joke)

#Using LiteLLM
from litellm import completion
response = completion(model="openai/gpt-4.1", messages=tell_a_joke)
reply = response.choices[0].message.content

#Printing token details - part of liteLLM Response
print(f"Input tokens: {response.usage.prompt_tokens}")
print(f"Output tokens: {response.usage.completion_tokens}")
print(f"Cached tokens: {response.usage.prompt_tokens_details.cached_tokens}")
print(f"Total tokens: {response.usage.total_tokens}")
print(f"Total cost: {response._hidden_params["response_cost"]*100:.4f} cents")

# Printing Markdown in console
#printmd(response.choices[0].message.content)
printmd(reply)

