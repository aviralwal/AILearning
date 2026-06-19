import os
from dotenv import load_dotenv
from openai import OpenAI
from richmd import printmd
import gradio as gr

#Loading API Secrets from env files
print("Loading env variables and configuration")
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

#Initializing Ollama and OpenRouter Clients
print("Defining OpenAI Client")
openai = OpenAI()

#Wrapping openai call within a function
system_message = "You are a helpful assistant"
def message_gpt(prompt):
    messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
    response = openai.chat.completions.create(model="gpt-4.1-mini", messages=messages)
    return response.choices[0].message.content

#Creating gradio interface with gpt
message_input = gr.Textbox(label="Your message:", info="Enter a message for GPT-4.1-mini", lines=7)
message_output = gr.Textbox(label="Response:", lines=8)

view = gr.Interface(
    fn=message_gpt,
    title="GPT", 
    inputs=[message_input], 
    outputs=[message_output], 
    examples=["hello", "howdy"], 
    flagging_mode="never"
    )
view.launch()
