import requests

api_key = "" # To complete
model = "gpt-4o-mini"
prompt = "Here the prompt to send to chatgpt"
hearders = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}
parameters= {
    "model": model,
    "prompt": prompt,
    "max_tokens": 100
}
response = requests.post(f"https://api.openai.com/v1/completions", headers=hearders, json=parameters).json()