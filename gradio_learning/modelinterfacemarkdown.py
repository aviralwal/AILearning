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
system_message = "You are a helpful assistant that responds in markdown without code blocks"

def message_gpt(prompt):
    messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
    response = openai.chat.completions.create(model="gpt-4.1-mini", messages=messages)
    return response.choices[0].message.content

def message_gpt5(prompt):
    messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}]
    response = openai.chat.completions.create(model="gpt-4.1-mini", messages=messages)
    return response.choices[0].message.content

def stream_gpt(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    stream = openai.chat.completions.create(
        model='gpt-4.1-mini',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

def stream_gpt5(prompt):
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
      ]
    stream = openai.chat.completions.create(
        model='gpt-5-mini',
        messages=messages,
        stream=True
    )
    result = ""
    for chunk in stream:
        result += chunk.choices[0].delta.content or ""
        yield result

#Creating gradio interface with gpt returning markdown
message_input = gr.Textbox(label="Your message:", info="Enter a message for GPT-4.1-mini", lines=7)
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=message_gpt,
    title="GPT", 
    inputs=[message_input], 
    outputs=[message_output], 
    examples=["Explain GTPs to a 5 year old", "Explain GPTs to a genius"], 
    flagging_mode="never"
    )
view.launch()

# Creating gradio interface with streaming
message_input = gr.Textbox(label="Your message:", info="Enter a message for GPT-4.1-mini", lines=7)
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=stream_gpt,
    title="GPT", 
    inputs=[message_input], 
    outputs=[message_output], 
    examples=[
        "Explain the Transformer architecture to a layperson",
        "Explain the Transformer architecture to an aspiring AI engineer",
        ], 
    flagging_mode="never"
    )
view.launch()

# Creating gradio interface where we use multiple inputs, a textbox and dropdown to enter text and relect which model to use for response.
def stream_model(prompt, model):
    if model=="GPT4":
        result = stream_gpt(prompt)
    elif model=="GPT5":
        result = stream_gpt5(prompt)
    else:
        raise ValueError("Unknown model")
    yield from result

message_input = gr.Textbox(label="Your message:", info="Enter a message for the LLM", lines=7)
model_selector = gr.Dropdown(["GPT4", "GPT5"], label="Select model", value="GPT4")
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=stream_model,
    title="LLMs", 
    inputs=[message_input, model_selector], 
    outputs=[message_output], 
    examples=[
            ["Explain the Transformer architecture to a layperson", "GPT4"],
            ["Explain the Transformer architecture to an aspiring AI engineer", "GPT5"]
        ], 
    flagging_mode="never"
    )
view.launch()
