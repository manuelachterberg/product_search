from openai import OpenAI
from datetime import datetime
import os
import yaml
from dotenv import load_dotenv
from googleapiclient.discovery import build
from tts import GoogleTTS
import subprocess


# Aktuelle Zeit und Datum
now = datetime.now()
kidname = "Levi"
output_file = "outputs/product_description.mp3"
output_wav = "outputs/product_description.wav"

script_dir = os.path.dirname(os.path.abspath(__file__))

def load_yaml(file_name):
    file_path = os.path.join(script_dir, file_name)
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
def load_env(file_name):
    file_path = os.path.join(script_dir, file_name)
    load_dotenv(file_path)

load_env(".secrets") # Load secrets
role = load_yaml("roles/ProductAgent.yaml")  # Load system role
prompt_template = load_yaml("prompts/productSearch.yaml")  # Load prompt

# Initialize the clients
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
google_api_key = (os.getenv("GOOGLE_API_KEY"))
google_search_id = (os.getenv("GOOGLE_SEARCH_ID"))

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
     # Initialize the TTS class
    tts = GoogleTTS()
    print("Product Lookup via GTIN")
    while True:
        gtin = input("Enter GTIN (or 'exit' to quit): ").strip()
        title, link = search_gtin_with_google(gtin)
        waitingMusic = play_with_aplay("waitingMusic.wav")
        if title and link:
            print(f"Gefundenes Produkt: {title}\nLink: {link}")
        else:
            print("Kein Produkt gefunden.")
        product_info = generate_creative_description(title, link, kidname)
        print("\n" + product_info + "\n")
        text_to_speak = product_info
        # Generate TTS audio
        tts.track_usage(text=text_to_speak, output_file=output_file, tone="excited")
        convert_mp3_to_wav(output_file, output_wav)
        waitingMusic.terminate()
        waitingMusic.wait()
        play_with_aplay(output_wav)
        
if __name__ == "__main__":
    main()

