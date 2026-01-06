
import urllib.request
import json
import ssl

KEY = "AIzaSyC8868bXJD3kPrslmDx4EseNnxILIIpEQI"
MODELS = ["gemini-1.5-flash", "gemini-1.5-flash-001", "gemini-pro", "gemini-1.0-pro"]
VERSIONS = ["v1beta", "v1"]

payload = json.dumps({"contents": [{"parts": [{"text": "Hello"}]}]}).encode()
headers = {'Content-Type': 'application/json'}

# Create SSL context to ignore potential cert issues in this restricted env if needed, 
# though standard verify is usually fine.
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print(f"Testing API Key: {KEY[:5]}...")

for version in VERSIONS:
    for model in MODELS:
        url = f"https://generativelanguage.googleapis.com/{version}/models/{model}:generateContent?key={KEY}"
        print(f"\nTrying: {version} / {model}")
        try:
            req = urllib.request.Request(url, data=payload, headers=headers)
            with urllib.request.urlopen(req, context=ctx) as res:
                if res.status == 200:
                    print(">>> SUCCESS! <<<")
                    print(res.read().decode()[:100])
                    # Exit after finding first working one
                else:
                    print(f"Status: {res.status}")
        except Exception as e:
            print(f"Failed: {e}")

