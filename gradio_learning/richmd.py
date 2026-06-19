from rich.console import Console
from rich.markdown import Markdown

console=Console()

def printmd(text):
    markdown_text=text
    md = Markdown(markdown_text)
    console.print(md)
