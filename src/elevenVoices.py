import requests
import json

# Replace with your ElevenLabs API key
API_KEY = "sk_602419aa8fe50c1aa9a4afeeb3d1ebd3a3a82f1405d97871"  # Replace this with your actual API Key

# Endpoint URL for getting shared voices
url = "https://api.elevenlabs.io/v1/shared-voices"

# Define headers
headers = {
    "Accept": "application/json",
    "xi-api-key": API_KEY
}

# Define query parameters
params = {
    "page_size": 30,
    "gender": "female",
    "language": "de"
}

# Fetch shared voices
response = requests.get(url, headers=headers, params=params)

# Check response status
if response.status_code == 200:
    # Pretty-print the JSON response
    voices = response.json()
    print("Delivered JSON Data:")
    print(json.dumps(voices, indent=4, ensure_ascii=False))
else:
    print(f"Error: {response.status_code} - {response.text}")