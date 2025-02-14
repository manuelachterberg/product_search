from datetime import datetime
import os
import yaml
from dotenv import load_dotenv
from googleapiclient.discovery import build
from tts_elevenlabs import ElevenLabsTTS
import subprocess
from evdev import InputDevice, categorize, ecodes
import re
from rgb_led import RGBLEDController
import time
from pydub import AudioSegment
from openai import OpenAI
from io import BytesIO
from elevenlabs import stream
import threading
from itertools import tee

# Aktuelle Zeit und Datum
now = datetime.now()
kidname = ""
kidname_short = ""
output_mp3 = "outputs/product_description.mp3"
output_wav = "outputs/product_description.wav"
script_dir = os.path.dirname(os.path.abspath(__file__))
tts = ElevenLabsTTS()
led = RGBLEDController(red_pin=22, green_pin=23, blue_pin=8, active_high=True)  # Initialize the LED controller
current_process = None
time_of_day = "Morgen"


def load_yaml(file_name):
    file_path = os.path.join(script_dir, file_name)
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def load_env(file_name):
    file_path = os.path.join(script_dir, file_name)
    load_dotenv(file_path)

def load_prompt_templates(language="en"):
    # Construct the filenames dynamically based on the language
    role_file = script_dir + f"/roles/ProductAgent_{language}.yaml"
    prompt_file = script_dir + f"/prompts/productSearch_{language}.yaml"

    # Check if the role file exists
    if not os.path.exists(role_file):
        raise FileNotFoundError(f"Role file for language '{language}' not found: {role_file}")
    
    # Check if the prompt file exists
    if not os.path.exists(prompt_file):
        raise FileNotFoundError(f"Prompt file for language '{language}' not found: {prompt_file}")
    
    # Load the YAML files
    role_template = load_yaml(role_file)
    prompt_template = load_yaml(prompt_file)
    
    return role_template, prompt_template

def play_audio_stream(text, waiting_music_process, voice_id="5Aahq892EEb6MdNwMM3p", model_id="eleven_multilingual_v2", output_file="output_audio.mp3"):

    def terminate_waiting_music():
        """Terminate the waiting music process after 5 seconds."""
        if waiting_music_process and waiting_music_process.poll() is None:
            print(f"Waiting for 5 seconds before terminating waiting music process with PID {waiting_music_process.pid}")
            time.sleep(5)  # Wait for 5 seconds
            print(f"Terminating waiting music process with PID {waiting_music_process.pid}")
            waiting_music_process.terminate()
            waiting_music_process.wait()  # Ensure the process is cleaned up
            print("Waiting music process terminated.")

    # Start the waiting music termination in a separate thread
    if waiting_music_process and waiting_music_process.poll() is None:
        threading.Thread(target=terminate_waiting_music, daemon=True).start()

    # Stream the audio content
    print("Starting audio stream...")
    audio_stream = tts.synthesize_speech_stream(text, voice_id, model_id)

    if audio_stream:
        # Duplicate the generator to allow playback and saving simultaneously
        audio_stream_for_playback, audio_stream_for_saving = tee(audio_stream)

        # Save the streamed audio to a file
        with open(output_file, "wb") as file:
            for chunk in audio_stream_for_saving:
                if isinstance(chunk, bytes):
                    file.write(chunk)  # Save each chunk to the file
                else:
                    print(f"Unexpected chunk type: {type(chunk)}")

        # Play the audio stream locally
        stream(audio_stream_for_playback)

        print(f"Audio stream finished and saved to {output_file}.")
    else:
        print("Error: Audio stream is None.")

# Load environment variables
load_env(".secrets") # Load secrets
load_env(".env") # Load env
kidname = os.getenv("kidname")
kidname_short = os.getenv("kidname_short")
language = os.getenv("language")
role, prompt_template = load_prompt_templates(language)
scanner_device = os.getenv("scannerdevice")
waiting_music = script_dir + f"/assets/waitingMusic.wav"

# Initialize the clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
google_api_key = os.getenv("GOOGLE_API_KEY")
google_search_id = os.getenv("GOOGLE_SEARCH_ID")

def read_barcode():
    """
    Reads barcodes from the scanner using evdev and yields scanned input.
    """
    device = InputDevice(scanner_device)
    print(f"Listening for barcode input from {device.name}...")

    barcode = ""
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            if key_event.keystate == 1:  # Key down event
                key = key_event.keycode
                if key == "KEY_ENTER":  # End of barcode
                    # Use regex to filter only numeric characters before yielding
                    numeric_barcode = re.sub(r"[^\d]", "", barcode)
                    yield numeric_barcode
                    barcode = ""
                elif "KEY_" in key:
                    barcode += key.replace("KEY_", "")  # Append character

def generate_creative_description(product_name, product_link, kidname="Levi"):
    # prompt = "Erstelle eine komplette Nachrichtensendung mit den folgenden Elementen:\n\n"
    current_date = datetime.now().strftime("%Y-%m-%d")

    day_period = get_day_period()
    prompt = f"Es ist aktuell {day_period}, am , {current_date}.\n\n"
    prompt_template_string = prompt_template["content"]
    prompt += prompt_template_string.replace("{product_name}", product_name).replace("{product_link}", product_link).replace("{kid_name}", kidname)
    print(prompt)
        
    # ChatGPT Aufruf
    response = client.chat.completions.create(
        model="gpt-4",  # Adjust model as necessary
        messages=[
            {"role": "system", "content": role["content"]},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.1
    )

    return response.choices[0].message.content.strip()

def generate_greeting(kidname="Levi"):
    # prompt = "Erstelle eine komplette Nachrichtensendung mit den folgenden Elementen:\n\n"
    current_date = datetime.now().strftime("%Y-%m-%d")

    day_period = get_day_period()
    prompt = f"Es ist aktuell {day_period}, am , {current_date}.\n\n"
    prompt_template_string = prompt_template["greeting"]
    prompt += prompt_template_string.replace("{kid_name}", kidname)
    print(prompt)
        
    # ChatGPT Aufruf
    response = client.chat.completions.create(
        model="gpt-4",  # Adjust model as necessary
        messages=[
            {"role": "system", "content": role["content"]},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.1
    )

    return response.choices[0].message.content.strip()

def generate_no_prouduct_found_response(kidname="Levi"):
    text = prompt_template["notfound"].replace("{kid_name}", kidname)
    print(text)
    return text

def search_gtin_with_google(gtin):
    # Google API-Client erstellen
    service = build("customsearch", "v1", developerKey=google_api_key)
    
    # Suche nach der GTIN
    result = service.cse().list(q=gtin, cx=google_search_id).execute()
    
    # Ersten Treffer zurückgeben
    if "items" in result:
        return result["items"][0]["title"], result["items"][0]["link"]
    return None, None

def get_day_period():
    """
    Bestimmt die Tageszeit basierend auf der aktuellen Uhrzeit.
    """
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Morgen" 
    elif 12 <= hour < 17:
        return "Nachmittag"  
    elif 17 <= hour < 22:
        return "Abend"  
    else:
        return "Nacht" 

def convert_mp3_to_wav(mp3_file, wav_file):
    subprocess.run(["ffmpeg", "-y", "-i", mp3_file, wav_file], check=True)

def play_with_aplay(file_path):
    global current_process  # Use a global variable to track the running process
    try:
        # If a process is already running, terminate it
        if current_process and current_process.poll() is None:  # Check if the process is still running
            print(f"Terminating previous 'aplay' process with PID {current_process.pid}")
            current_process.terminate()
            current_process.wait()  # Ensure the process is cleaned up
            print("Previous 'aplay' process terminated.")

        # Start a new process
        current_process = subprocess.Popen(["aplay", file_path])
        print(f"Started new 'aplay' process with PID {current_process.pid}")
        return current_process  # Return the process handle so it can be managed later
    except FileNotFoundError:
        print("Error: 'aplay' is not installed or not found in PATH.")
        return None

def handle_gtin(gtin, script_dir, language, kidname, waiting_music):
    led.set_color(1, 1, 0)  # Orange
    gtin = gtin.strip()
    print(f"Scanned GTIN: {gtin}")
    waiting_music_process = None  # Initialize waiting_music_process to None
    answer = None  # Initialize answer to None
    if gtin:
        output_mp3 = os.path.join(script_dir, f"outputs/{gtin}_{language}.mp3")
        output_wav = os.path.join(script_dir, f"outputs/{gtin}_{language}.wav")
        if not os.path.exists(output_wav):
            print(f"File {gtin}_{language}.wav not found in output folder")
            title, link = search_gtin_with_google(gtin)  # Search GTIN with google search API
            waiting_music_process = play_with_aplay(waiting_music)  # Play waiting music
            if title and link:  # if product is found
                led.set_color(0, 1, 0)  # Green
                print(f"Gefundenes Produkt: {title}\nLink: {link}")
                product_info = generate_creative_description(title, link, kidname)  # create a nice description using OpenAI API
                print("\n" + product_info + "\n")
                text_to_speak = product_info
                play_audio_stream(text_to_speak, waiting_music_process, output_file=output_mp3)  # Stream and play the audio content
                #tts.track_usage(text=text_to_speak, output_file=output_mp3)  # TTS the text and track character usage for the api
                convert_mp3_to_wav(output_mp3, output_wav)  # convert mp3 to wav
            else:
                led.set_color(1, 0, 0)  # Red
                print("Kein Produkt gefunden.")
                #product_info = generate_no_prouduct_found_response(kidname) # Deprecated. For generating a new product not found message
                play_with_aplay(os.path.join(script_dir, f"outputs/notfound.wav"))
        else:
            led.set_color(0, 1, 0)  # Green
            print(f"File {gtin}_{language}.wav found in output folder")
            answer = play_with_aplay(output_wav)  # play the response text
        while answer and answer.poll() is None:
            print("Playback in progress...")
            time.sleep(1)

        # Playback finished
        print("Playback finished.")
        return True  # Indicate that the GTIN was handled
    return False  # Indicate that the GTIN was not handled

def main():
    print("Violet ON")
    led.set_color(1, 1, 0)  # Violet
    time_of_day = get_day_period()
    print("Product Lookup via GTIN")
    output_mp3 = os.path.join(script_dir, f"outputs/{time_of_day}_{language}.mp3")
    output_wav = os.path.join(script_dir, f"outputs/{time_of_day}_{language}.wav")
    if not os.path.exists(output_wav): # if the greeting for that time of day is not already generated then generate it
        text_to_speak = generate_greeting(kidname=kidname) # promt chatGPT to generate a greeting
        tts.track_usage(text=text_to_speak, output_file=output_mp3)  # TTS the text and track character usage for the api
        convert_mp3_to_wav(output_mp3, output_wav)  # convert mp3 to wav
    
    play_with_aplay(output_wav)

    while True:  # always loop the product search
        led.set_color(0, 0, 1)  # Blue
        print("Waiting for scanner input...")
        # Start barcode scanning
        barcode_generator = read_barcode()
        for gtin in barcode_generator:
            if handle_gtin(gtin, script_dir, language, kidname, waiting_music):
                break  # Move break the for loop iterating through gtins
            print("Continuing the scanning process...")
        print("Starting from the beginning")

if __name__ == "__main__":
    main()

