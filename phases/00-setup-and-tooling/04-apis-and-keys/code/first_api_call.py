import json
import sys
import urllib.request

sys.path.insert(0, "languages/python")
from utils.secrets import get_openrouter_key, get_default_model


def call_with_sdk():
    """Call OpenRouter using the OpenAI-compatible SDK."""
    try:
        from openai import OpenAI
    except ImportError:
        print("Install the SDK: uv pip install openai")
        return

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=get_openrouter_key(),
    )
    model = get_default_model()
    response = client.chat.completions.create(
        model=model,
        max_tokens=256,
        messages=[{"role": "user", "content": "What is a neural network in one sentence?"}],
    )
    print(f"SDK response: {response.choices[0].message.content}")
    usage = response.usage
    print(f"Tokens used: {usage.prompt_tokens} in, {usage.completion_tokens} out")


def call_raw_http():
    """Call OpenRouter using raw HTTP (no SDK)."""
    api_key = get_openrouter_key()
    model = get_default_model()

    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    body = json.dumps({
        "model": model,
        "max_tokens": 256,
        "messages": [{"role": "user", "content": "What is a neural network in one sentence?"}],
    }).encode()

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read())
        print(f"Raw HTTP response: {result['choices'][0]['message']['content']}")
        usage = result["usage"]
        print(f"Tokens used: {usage['prompt_tokens']} in, {usage['completion_tokens']} out")


if __name__ == "__main__":
    print("=== OpenRouter API Calls ===\n")
    print(f"Model: {get_default_model()}\n")
    print("1. Using the OpenAI-compatible SDK:")
    call_with_sdk()
    print("\n2. Using raw HTTP:")
    call_raw_http()
