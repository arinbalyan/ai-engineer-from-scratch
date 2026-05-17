import json
import sys
import urllib.request
import urllib.error

sys.path.insert(0, "languages/python")
from utils.secrets import get_huggingface_key


def call_with_sdk():
    """Call HuggingFace Inference API using the official SDK."""
    from huggingface_hub import InferenceClient

    client = InferenceClient(provider="novita", token=get_huggingface_key())
    response = client.chat_completion(
        model="deepseek-ai/DeepSeek-V4-Pro",
        messages=[{"role": "user", "content": "What is a neural network in one sentence?"}],
        max_tokens=256,
    )
    print(f"SDK response: {response.choices[0].message.content}")
    usage = response.usage
    print(f"Tokens used: {usage.prompt_tokens} in, {usage.completion_tokens} out")


def call_raw_http():
    """Call HuggingFace Inference API using raw HTTP (no SDK).
    
    Note: Provider-routed models (like DeepSeek-V4-Pro) require provider-specific
    endpoints. This example uses the standard Inference API with a smaller model.
    For production, use the SDK which handles provider routing automatically.
    """
    api_key = get_huggingface_key()
    # Use a model available on the standard Inference API
    model = "google/flan-t5-small"

    url = f"https://api-inference.huggingface.co/models/{model}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    body = json.dumps({
        "inputs": "What is a neural network?",
        "parameters": {"max_new_tokens": 128},
    }).encode()

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())
            if isinstance(result, list):
                print(f"Raw HTTP response: {result[0].get('generated_text', result[0])}")
            elif isinstance(result, dict):
                print(f"Raw HTTP response: {result.get('generated_text', result)}")
            else:
                print(f"Raw HTTP response: {result}")
    except urllib.error.HTTPError as e:
        # Model may be loading or unavailable on free tier - this is expected
        print(f"Raw HTTP: Model '{model}' returned {e.code} (common on free tier)")
        print(f"Tip: Use the SDK for automatic provider routing and retries.")


if __name__ == "__main__":
    print("=== HuggingFace Inference API Calls ===\n")
    print("Model: deepseek-ai/DeepSeek-V4-Pro\n")
    print("1. Using the HuggingFace SDK:")
    call_with_sdk()
    print("\n2. Using raw HTTP:")
    call_raw_http()
