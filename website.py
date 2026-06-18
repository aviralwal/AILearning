import os
from scraper import fetch_website_contents
from IPython.display import Markdown, display
from openai import OpenAI

OLLAMA_BASE_URL = "http://localhost:11434/v1"

chatmodel = "deepseek-r1:1.5b"

system_prompt = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.

"""

ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key='ollama')

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website}
    ]

def summarize(url):
    website = fetch_website_contents(url)
    response = ollama.chat.completions.create(
        model = chatmodel,
        messages = messages_for(website)
    )
    return response.choices[0].message.content

def display_summary(url):
    summary = summarize(url)
    print(summary)

display_summary("https://edwarddonner.com")
