from tts_elevenlabs import ElevenLabsTTS
import os
from dotenv import load_dotenv

# Load environment variables from .secrets file
load_dotenv(dotenv_path=".secrets")

# Get the API key from environment variables
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

def test_synthesize_speech():
    # Initialize the ElevenLabsTTS class
    tts = ElevenLabsTTS()

    # Define the text to be synthesized
    text = "Hallo, was geht? Ich bin ein Testtext. Wie kann ich Ihnen helfen? Ich bin ein Testtext."

    # Define the output file path
    output_file = "outputs/test_audio.mp3"

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Call the synthesize_speech method
    try:
        char_count = tts.synthesize_speech(text, output_file)
        print(f"Synthesized speech for {char_count} characters.")
        print(f"Audio saved to {output_file}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run the test function
if __name__ == "__main__":
    test_synthesize_speech()