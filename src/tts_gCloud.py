import json
import os
from google.cloud import texttospeech
from dotenv import load_dotenv
from datetime import datetime

class GoogleTTS:
    def __init__(self, secrets_file=".secrets", usage_file="tts_usage.json"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.secrets_path = os.path.join(script_dir, secrets_file)
        self.usage_file = os.path.join(script_dir, usage_file)
        self.client = None
        self.load_env()
        self.initialize_client()

    def load_env(self):
        load_dotenv(self.secrets_path)

    def initialize_client(self):
        tts_key = os.getenv("TTS_KEY_PATH")
        if not tts_key:
            raise ValueError("TTS_KEY_PATH not found in environment variables.")
        self.client = texttospeech.TextToSpeechClient.from_service_account_file(tts_key)

    def synthesize_speech(self, text, output_file, voice_name="de-DE-Wavenet-C", language_code="de-DE", tone="default"):
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Generate SSML if an excited tone is requested
        if tone == "excited":
            ssml_text = f"""
            <speak>
                <voice name="{voice_name}">
                    <express-as style="excited">
                        {text}
                    </express-as>
                </voice>
            </speak>
            """
            synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)
        else:
            # Use plain text if no special tone is needed
            synthesis_input = texttospeech.SynthesisInput(text=text)

        # Configure the voice
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            name=voice_name,
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )
        # Configure the audio with pitch and speed adjustments
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=0.9,  # Slightly slower
            pitch=5.0           # Higher pitch for excitement
        )

        # Request the synthesis
        response = self.client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        # Save the audio content to a file
        with open(output_file, "wb") as out:
            out.write(response.audio_content)
            print(f"Audio content saved to '{output_file}'")

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

    def track_usage(self, text, output_file, voice_name="de-DE-Wavenet-C", language_code="de-DE", tone="excited"):
        usage_data = self.load_usage_data()
        print(f"Total characters used so far: {usage_data['total_characters']}")

        # Synthesize speech and get character count
        char_count = self.synthesize_speech(text, output_file, voice_name, language_code)

        # Update usage tracking
        usage_data["total_characters"] += char_count
        usage_data["last_updated"] = datetime.now().isoformat()
        self.save_usage_data(usage_data)

        print(f"Updated total character count: {usage_data['total_characters']}")
