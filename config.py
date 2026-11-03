from dotenv import load_dotenv
from langchain_ollama import ChatOllama


load_dotenv()

def get_model():
    return ChatOllama(
        model="qwen3:4b-instruct",
        temperature=0,
        num_ctx=4096,
    )