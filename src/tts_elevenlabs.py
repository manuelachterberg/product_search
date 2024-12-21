import os
import json
from datetime import datetime
from pydub import AudioSegment
from io import BytesIO
from dotenv import load_dotenv
from elevenlabs import stream
from elevenlabs.client import ElevenLabs

class ElevenLabsTTS:
    def __init__(self, secrets_file=".secrets", usage_file="tts_usage.json"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.secrets_path = os.path.join(script_dir, secrets_file)
        self.usage_file = os.path.join(script_dir, usage_file)
        self.api_key = None
        self.client = None
        self.load_env()

    def load_env(self):
        load_dotenv(self.secrets_path)
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY not found in environment variables.")
        self.client = ElevenLabs(api_key=self.api_key)

    def synthesize_speech_stream(self, text, voice_id="5Aahq892EEb6MdNwMM3p", model_id="eleven_multilingual_v2"):
        audio_stream = self.client.text_to_speech.convert_as_stream(
            text=text,
            voice_id=voice_id,
            model_id=model_id
        )
        return audio_stream

    def synthesize_speech(self, text, output_file, voice_id="5Aahq892EEb6MdNwMM3p", model_id="eleven_multilingual_v2", volume_increase_db=1):
        audio_data = BytesIO()
        for chunk in self.synthesize_speech_stream(text, voice_id, model_id):
            if isinstance(chunk, bytes):
                audio_data.write(chunk)
        audio_data.seek(0)

        audio = AudioSegment.from_file(audio_data, format="mp3")
        louder_audio = audio + volume_increase_db
        louder_audio.export(output_file, format="mp3")
        print(f"Louder audio content saved to '{output_file}'")

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
        usage_data = self.load_usage_data()
        print(f"Loaded usage data: {usage_data}")

        char_count = self.synthesize_speech(
            text=text,
            output_file=output_file,
            voice_id=voice_id,
            model_id=model_id
        )

        usage_data["total_characters"] += char_count
        usage_data["last_updated"] = datetime.now().isoformat()
        self.save_usage_data(usage_data)

        print(f"Updated usage data: {usage_data}")
        return char_count

if __name__ == "__main__":
    tts = ElevenLabsTTS()
    text = "Hallo! Dies ist ein Test, um die API von ElevenLabs auf Deutsch zu nutzen."
    output_file = "output.mp3"
    tts.track_usage(text, output_file)