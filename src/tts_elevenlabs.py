import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime

class ElevenLabsTTS:
    def __init__(self, secrets_file=".secrets", usage_file="tts_usage.json"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.secrets_path = os.path.join(script_dir, secrets_file)
        self.usage_file = os.path.join(script_dir, usage_file)
        self.api_key = None
        self.load_env()

    def load_env(self):
        load_dotenv(self.secrets_path)
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables.")

    def synthesize_speech(self, text, output_file, voice_id="5Aahq892EEb6MdNwMM3p", model_id="eleven_multilingual_v2"):
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Define ElevenLabs API endpoint
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

        # Define headers and payload
        headers = {
            "Accept": "audio/mpeg",
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }
        payload = {
            "text": text,
            "model_id": model_id,
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.75
            }
        }

        # Make the API request
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            # Save the audio content to a file
            with open(output_file, "wb") as out:
                out.write(response.content)
                print(f"Audio content saved to '{output_file}'")
        else:
            raise RuntimeError(f"Error {response.status_code}: {response.text}")

        # Return the character count of the input text
        return len(text)

    def load_usage_data(self):
        if os.path.exists(self.usage_file):
            with open(self.usage_file, "r") as f:
                return json.load(f)
        return {"total_characters": 0, "last_updated": None}

    def save_usage_data(self, usage_data):
        with open(self.usage_file, "w") as f:
            json.dump(usage_data, f, indent=4)

    def track_usage(self, text, output_file, voice_id="5Aahq892EEb6MdNwMM3p", model_id="eleven_multilingual_v2"):
        """
        Tracks usage while synthesizing speech.
        Args:
            text (str): The text to synthesize.
            output_file (str): Path to save the output file.
            voice_id (str): The voice ID for synthesis.
            model_id (str): The model ID for synthesis.
        """
        # Ensure usage data is loaded
        usage_data = self.load_usage_data()

        # Debugging: Print the current usage data
        print(f"Loaded usage data: {usage_data}")

        # Synthesize speech and get character count
        char_count = self.synthesize_speech(
            text=text,
            output_file=output_file,
            voice_id=voice_id,
            model_id=model_id
        )

        # Update usage tracking
        if "total_characters" not in usage_data:
            usage_data["total_characters"] = 0  # Initialize if not present

        usage_data["total_characters"] += char_count
        usage_data["last_updated"] = datetime.now().isoformat()

        # Save the updated usage data
        self.save_usage_data(usage_data)

        # Print the updated character count
        print(f"Updated total character count: {usage_data['total_characters']}")

if __name__ == "__main__":
    tts = ElevenLabsTTS()
    text = "Hallo! Dies ist ein Test, um die API von ElevenLabs auf Deutsch zu nutzen."
    output_file = "output.mp3"

    tts.track_usage(text, output_file)