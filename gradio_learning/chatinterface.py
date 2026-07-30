import os
from dotenv import load_dotenv
from openai import OpenAI
from richmd import printmd
import gradio as gr

#Loading API Secrets from env files
print("Loading env variables and configuration")
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

#Initializing OpenAI Client
print("Defining OpenAI Client")
openai = OpenAI()
MODEL="gpt-4.1-mini"

#System prompt
system_message = "You are a helpful assistant"

# A basic chat fallback function which reponds to chat as is without any context/prompt modification
def chat(message, history):
    history = [{"role":h["role"], "content":h["content"]} for h in history] #Command to remove all the metadata from response
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages)
    return response.choices[0].message.content

gr.ChatInterface(fn=chat, type="messages").launch()
