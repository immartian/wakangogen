from pathlib import Path
from openai import OpenAI
import os
from hiranganaromaji import *


def audio(hirangana, speech_file_path):
    with client.audio.speech.with_streaming_response.create(
    model="tts-1",
        voice="alloy",
        input= hirangana,
        response_format="mp3"
    ) as response:
        with open(speech_file_path, 'wb') as f:
            for chunk in response.iter_bytes():
                f.write(chunk)

#load the api key from .env
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

raw = hirangana_kanji_romaji
for index, item in enumerate(raw):
    print(f"{index}: {item['hiragana']}")
    hiragana = raw[index]['hiragana']
    romaji = raw[index]['romaji']
    filename = f"{romaji}.mp3"
    speech_file_path = Path(__file__).parent / f"../static/speech/{filename}"
    print (speech_file_path)
    audio(hiragana, speech_file_path)


