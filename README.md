
# Product Lookup via GTIN

This Python program performs **product lookup via GTIN (Global Trade Item Number)**, integrating multiple APIs and tools to provide a **kid-friendly product description**. It uses OpenAI's GPT, Google Custom Search API, and Google Text-to-Speech (TTS). The program also handles audio conversion and playback seamlessly.

---

## Features

- **Product Search via Google Custom Search API:**
  - Searches for products by GTIN and retrieves the product name and link.

- **Kid-Friendly Descriptions:**
  - Uses OpenAI's GPT to generate humorous, simple, and engaging product descriptions.

- **Text-to-Speech (TTS):**
  - Converts descriptions into audio using Google TTS with customizable tones.

- **Audio Handling:**
  - Converts MP3 output to WAV using FFmpeg.
  - Plays waiting music and product descriptions using `aplay`.

- **Multi-Language Support:**
  - Dynamically loads prompts and templates for multiple languages.

---

## Setup

### **1. Clone the Repository**
```bash
git clone https://github.com/yourusername/product_lookup.git
cd product_lookup
```

### **2. Install Requirements**
Install Python dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### **3. Install External Tools**
Ensure the following tools are installed on your system:
- **FFmpeg** (for audio conversion):
  ```bash
  sudo apt install ffmpeg
  ```
- **Aplay** (for audio playback):
  ```bash
  sudo apt install alsa-utils
  ```

### **4. Set Up Environment Variables**
Create a `.secrets` file and a `.env` file in the project directory with the following variables:

#### `.secrets`:
```
OPENAI_API_KEY=<your_openai_api_key>
GOOGLE_API_KEY=<your_google_api_key>
GOOGLE_SEARCH_ID=<your_google_custom_search_id>
```

#### `.env`:
```
language=de
kidname=Levi
```

### **5. Add Prompt and Role Files**
Prepare YAML files for prompts and roles based on your preferred language:
- `roles/ProductAgent_<language>.yaml`
- `prompts/productSearch_<language>.yaml`

For example:
- `roles/ProductAgent_de.yaml`
- `prompts/productSearch_de.yaml`

---

## Usage

### Run the Program
```bash
python3 productSearch.py
```

### Input a GTIN
Enter a valid GTIN when prompted:
```
Enter GTIN (or 'exit' to quit): 1234567890123
```

### Exit the Program
Type `exit` to quit the program.

---

## Code Overview

### **Main Workflow**
1. **GTIN Input:** Prompts the user to enter a GTIN.
2. **Product Search:** Uses Google Custom Search API to find the product.
3. **Description Generation:** Uses OpenAI to generate a child-friendly description.
4. **Text-to-Speech:** Converts the description to speech using Google TTS.
5. **Audio Conversion:** Converts the MP3 file to WAV using FFmpeg.
6. **Playback:** Plays waiting music during the search and the final description.

### **Key Functions**
- **`search_gtin_with_google(gtin):`**
  - Searches Google for the product using GTIN.
  
- **`generate_creative_description(product_name, product_link, kidname):`**
  - Generates a kid-friendly description using OpenAI.

- **`convert_mp3_to_wav(mp3_file, wav_file):`**
  - Converts MP3 files to WAV for playback.

- **`play_with_aplay(file_path):`**
  - Plays audio files using `aplay`.

- **`load_prompt_templates(language):`**
  - Dynamically loads YAML templates for the specified language.

---

## Files and Directory Structure

```
product_lookup/
├── productSearch.py       # Main script
├── tts.py                 # Google TTS utility
├── .secrets               # API keys
├── .env                   # Language and kid's name settings
├── requirements.txt       # Python dependencies
├── prompts/               # Prompt YAML templates
│   ├── productSearch_en.yaml
│   ├── productSearch_de.yaml
├── roles/                 # Role YAML templates
│   ├── ProductAgent_en.yaml
│   ├── ProductAgent_de.yaml
├── outputs/               # Audio output directory
│   ├── product_description.mp3
│   ├── product_description.wav
└── waitingMusic.wav       # Waiting music file
```

---

## Example Output

### **Input:**
```
Enter GTIN (or 'exit' to quit): 1234567890123
```

### **Output (Console):**
```
Found Product: Bevola Kids 2 in 1 Shampoo & Shower Gel
Link: https://example.com/product

Generated Description:
Hello Levi, little sailor!
The product is called "Bevola Kids 2 in 1 Shampoo & Shower Gel."
A shampoo is like magic soap for your hair! When you wash your hair, you make it wet with water, add some shampoo, and it creates lots of foam that washes away dirt and makes your hair clean and soft.

"With bubbles in your hair, you’re ready for a clean adventure!"
```

### **Output (Audio):**
- Plays waiting music during the search.
- Plays the generated description as an audio file.

---

## Notes
- Ensure `waitingMusic.wav` exists in the project directory.
- Audio files are saved in the `outputs/` folder, named using the GTIN and language code.

---

## License
This project is licensed under the MIT License.

---

## Author
Created by [Manuel Achterberg](https://github.com/manuelachterberg)