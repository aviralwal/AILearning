import os
import requests
from dotenv import load_dotenv
from openai import OpenAI
from IPython.display import Markdown, display
from richmd import printmd
from langchain_openai import ChatOpenAI

#Loading API Secrets from env files
print("Loading env variables and configuration")
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
openrouter_url = "https://openrouter.ai/api/v1"
ollama_url = "http://localhost:11434/v1"

#Initializing Ollama and OpenRouter Clients
print("Defining OpenAI Client")
openai = OpenAI()

#Prompts - 2 chat agents will be talking to each other with different tones. Using ChatGPT models for now
print("Defining gpt models and prompts")
gpt1_model = "gpt-4.1-mini"
gpt2_model = "gpt-5-mini"

gpt1_system = "You are a chatbot who is very argumentative; \
you disagree with anything in the conversation and you challenge everything, in a snarky way."

gpt2_system = "You are a very polite, courteous chatbot. You try to agree with \
everything the other person says, or find common ground. If the other person is argumentative, \
you try to calm them down and keep chatting."

#Defining functions to call each model api call based on previous conversation
print("Defining call gpt function")
def call_gpt1():
    messages = [{"role": "system", "content": gpt1_system}]
    for gpt1, gpt2 in zip(gpt1_messages, gpt2_messages):
        messages.append({"role": "assistant", "content": gpt1})
        messages.append({"role": "user", "content": gpt2})
    response = openai.chat.completions.create(model=gpt1_model, messages=messages)
    return response.choices[0].message.content

def call_gpt2():
    messages = [{"role": "system", "content": gpt2_system}]
    for gpt1, gpt2_message in zip(gpt1_messages, gpt2_messages):
        messages.append({"role": "user", "content": gpt1})
        messages.append({"role": "assistant", "content": gpt2_message})
    messages.append({"role": "user", "content": gpt1_messages[-1]})
    response = openai.chat.completions.create(model=gpt2_model, messages=messages)
    return response.choices[0].message.content


# Making a loop call so that each model will be called one by one 5 times with each having output of other model. THis is simultating chatting of 2 models

gpt1_messages = ["Hi there"]
gpt2_messages = ["Hi"]

printmd(f"### GPT1:\n{gpt1_messages[0]}\n")
printmd(f"### GPT2:\n{gpt2_messages[0]}\n")

for i in range(5):
    gpt1_next = call_gpt1()
    printmd(f"### GPT:\n{gpt1_next}\n")
    gpt1_messages.append(gpt1_next)

    gpt2_next = call_gpt2()
    printmd(f"### Claude:\n{gpt2_next}\n")
    gpt2_messages.append(gpt2_next)

