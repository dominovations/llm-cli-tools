
import os
import time
import json
import requests
from openai import OpenAI
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# Setup clients
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
claude_client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral:7b-instruct"

prompt = input("Enter your prompt for comparison: ")

def run_openai():
    print("\n🔷 OpenAI GPT-4")
    start = time.time()
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
    )
    end = time.time()
    text = response.choices[0].message.content
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    print(f"Response: {text}\n⏱️ Time: {round(end - start, 2)}s | Prompt Tokens: {prompt_tokens} | Completion Tokens: {completion_tokens}")

def run_claude():
    print("\n🟡 Claude (Opus)")
    start = time.time()
    response = claude_client.messages.create(
        model="claude-3-opus-20240229",# claude-3-sonnet-20240229,claude-3-haiku-20240307,claude-3-opus-20240229
        max_tokens=1024,
        temperature=0.7,
        messages=[{"role": "user", "content": prompt}]
    )
    end = time.time()
    text = response.content[0].text
    usage = response.usage
    print(f"Response: {text}\n⏱️ Time: {round(end - start, 2)}s | Input Tokens: {usage.input_tokens} | Output Tokens: {usage.output_tokens}")

def run_mistral():
    print("\n🟩 Mistral (via Ollama)")
    start = time.time()
    response = requests.post(OLLAMA_URL, json={
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    })
    end = time.time()
    if response.ok:
        data = response.json()
        text = data.get("response", "")
        eval_count = data.get("eval_count", "?")
        prompt_eval = data.get("prompt_eval_count", "?")
        print(f"Response: {text}\n⏱️ Time: {round(end - start, 2)}s | Prompt Tokens: {prompt_eval} | Response Tokens: {eval_count}")
    else:
        print("❌ Error from Mistral:", response.status_code, response.text)

run_openai()
run_claude()
run_mistral()
