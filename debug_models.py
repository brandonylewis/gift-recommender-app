import urllib.request
import json

API_KEY = "AIzaSyC8868bXJD3kPrslmDx4EseNnxILIIpEQI"
URL = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

try:
    print(f"Querying: {URL}")
    with urllib.request.urlopen(URL) as response:
        raw_data = response.read().decode()
        print("Got response, saving to models.json...")
        with open("models.json", "w", encoding="utf-8") as f:
            f.write(raw_data)
        print("Done.")
except Exception as e:
    print(f"Error: {e}")
