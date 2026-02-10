import requests
import json
import time

def test_api():
    url = "http://localhost:8000/chat"
    payload = {
        "message": "Hello MemGraph!"
    }
    
    print(f"Testing API at {url}...")
    try:
        start = time.time()
        response = requests.post(url, json=payload)
        end = time.time()
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Latency: {(end-start)*1000:.2f}ms")
            print("Response:", json.dumps(data, indent=2))
        else:
            print(f"❌ Failed: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_api()
