import os
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
from richmd import printmd

load_dotenv(override=True)

#Defining a sample function
def shout(text):
    print(f"Shout has been called with input {text}")
    return text.upper()

#Launching Gradio interface without auth
#gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch()

#Launching Gradio interface with auth - Only for example
#gr.Interface(fn=shout, inputs="textbox", outputs="textbox", flagging_mode="never").launch(auth=("aviral", "passphrase"))

# We can define input and output files along with labels, info, sizes. Gardio supports multiple types of io fields. 
# Adding a little more:

message_input = gr.Textbox(label="Your message:", info="Enter a message to be shouted", lines=7)
message_output = gr.Textbox(label="Response:", lines=8)

view = gr.Interface(
    fn=shout,
    title="Shout",
    inputs=[message_input],
    outputs=[message_output],
    examples=["hello", "howdy"],
    flagging_mode="never"
    )
view.launch()
