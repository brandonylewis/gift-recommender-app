import urllib.request
import json
import os

API_KEY = "AIzaSyC8868bXJD3kPrslmDx4EseNnxILIIpEQI"
URL = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

try:
    with urllib.request.urlopen(URL) as response:
        data = json.loads(response.read().decode())
        print("Available Models:")
        for model in data.get('models', []):
            if 'generateContent' in model.get('supportedGenerationMethods', []):
                print(f"- {model['name']}")
except Exception as e:
    print(f"Error listing models: {e}")
