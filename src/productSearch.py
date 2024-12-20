from openai import OpenAI
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


# Aktuelle Zeit und Datum
now = datetime.now()
kidname = ""
output_mp3 = "outputs/product_description.mp3"
output_wav = "outputs/product_description.wav"
script_dir = os.path.dirname(os.path.abspath(__file__))
tts = ElevenLabsTTS()
led = RGBLEDController(red_pin=22, green_pin=23, blue_pin=8, active_high=True)  # Initialize the LED controller


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

load_env(".secrets") # Load secrets
load_env(".env") # Load env
kidname = (os.getenv("kidname"))
language = (os.getenv("language"))
#voice_model = f"{language}-Wavenet-C" # set Google TTS Voice Model
role, prompt_template = load_prompt_templates(language)
scanner_device = (os.getenv("scannerdevice"))
waiting_music = script_dir + f"/assets/waitingMusic.wav"

# Initialize the clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
google_api_key = (os.getenv("GOOGLE_API_KEY"))
google_search_id = (os.getenv("GOOGLE_SEARCH_ID"))

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
    try:
        # Start aplay in the background
        process = subprocess.Popen(["aplay", file_path])
        return process  # Return the process handle so it can be terminated later
    except FileNotFoundError:
        print("Error: 'aplay' is not installed or not found in PATH.")
        return None

def main():
    print("Green ON")
    led.set_color(1, 0, 0)  # Red
     # Initialize the TTS class
    print("Product Lookup via GTIN")
    text_to_speak = generate_greeting(kidname=kidname)
    output_mp3 = os.path.join(script_dir, f"outputs/greeting_{kidname}.mp3")
    output_wav = os.path.join(script_dir, "outputs/greeting_{kidname}.wav")
    tts.track_usage(text=text_to_speak, output_file=output_mp3)  # TTS the text and track character usage for the api
    convert_mp3_to_wav(output_mp3, output_wav) # convert mp3 to wav
    play_with_aplay(output_wav) # play the response text


    while True: # always loop the product search
        led.set_color(0, 0, 1)  # Blue
        print("Waiting for scanner input...")
        # Start barcode scanning
        barcode_generator = read_barcode()
        #gtin = input("Enter GTIN (or 'exit' to quit): ").strip() # Promt User for entering a GTIN
        for gtin in barcode_generator:
            led.set_color(1, 1, 0)  # Orange
            gtin = gtin.strip()
            print(f"Scanned GTIN: {gtin}")
            if gtin:
                output_mp3 = os.path.join(script_dir, f"outputs/{gtin}_{language}.mp3")
                output_wav = os.path.join(script_dir, f"outputs/{gtin}_{language}.wav")
                if not os.path.exists(output_wav):
                    print(f"File {gtin}_{language}.wav not found in output folder")
                    title, link = search_gtin_with_google(gtin) # Search GTIN with google search API
                    waitingMusic = play_with_aplay(waiting_music) # Play waiting music
                    if title and link: # if product is found
                        led.set_color(0, 1, 0)  # Green
                        print(f"Gefundenes Produkt: {title}\nLink: {link}")
                        product_info = generate_creative_description(title, link, kidname) # create a nice description using OpenAI API
                        print("\n" + product_info + "\n")
                    else:
                        led.set_color(1, 0, 0)  # Red
                        print("Kein Produkt gefunden.")
                        product_info = generate_no_prouduct_found_response(kidname)
                    text_to_speak = product_info
                    tts.track_usage(text=text_to_speak, output_file=output_mp3)  # TTS the text and track character usage for the api
                    convert_mp3_to_wav(output_mp3, output_wav) # convert mp3 to wav
                    waitingMusic.terminate() # stop waiting music
                    waitingMusic.wait() # wait until process stopped
                else:
                    led.set_color(0, 1, 0)  # Green
                    print(f"File {gtin}_{language}.wav found in output folder")
                answer = play_with_aplay(output_wav) # play the response text
                # Poll until the process finishes
                while answer.poll() is None:
                    print("Playback in progress...")
                    time.sleep(1)

                # Playback finished
                print("Playback finished.")
                break  # Move break the for loop iterating through gtins
            print("Continuing the scanning process...")
            continue  # Move to the next GTIN in the generator
        print("Starting from the beginning")
        
if __name__ == "__main__":
    main()

