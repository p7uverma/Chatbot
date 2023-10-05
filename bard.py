# Official Packages
from bardapi import BardCookies, Bard
import io
from pygame import mixer
from dotenv import load_dotenv
import webbrowser
import os
import re

# My Own Pacakges
from packages import voice_input


# Load environment variables from the .env file
load_dotenv()

# Retrieve the token from the environment
Secure_1PSID = os.getenv("Secure_1PSID")
Secure_1PSIDCC = os.getenv("Secure_1PSIDCC")
Secure_1PSIDTS = os.getenv("Secure_1PSIDTS")

# creating a bard Dict for BardAPI
bard_dict = {
    "__Secure-1PSID": f"{Secure_1PSID}",
    "__Secure-1PSIDCC": f"{Secure_1PSIDCC}",
    "__Secure-1PSIDTS": f"{Secure_1PSIDTS}",
}

# Checking Token are on place
print(f"My tokens is: {bard_dict}\n")

# initializing bard from chat and pygame for audio
mixer.init()
bard = BardCookies(cookie_dict=bard_dict, language="english")
website_keywords = ["open", "please open", "navigate", "fire"]

if __name__ == "__main__":
    # query = input("Enter your query: ")
    # continous loop
    while True:
        query = voice_input.get_user_query()
        print(f"You said: {query}\n")
        if query == "error":
            continue

        if "exit" in query:
            audio = bard.speech(
                "I think, I need to go.."
            )  # Create an in-memory audio stream from the bytes
            audio_stream = io.BytesIO(audio["audio"])

            # Load the MP3 audio into Pygame mixer
            mixer.music.load(audio_stream)

            # Play the audio
            mixer.music.play()

            # Wait for the audio to finish playing
            while mixer.music.get_busy():
                pass
            exit()

        for keyword in website_keywords:
            if keyword in query:
                url = query.split(keyword, 1)[-1].strip()
                if url:
                    if not url.startswith("http://") or not url.startswith("https://"):
                        url = "http://" + url
                    pattern = r'[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                    match = re.search(pattern, url)
                    if match == None:
                        url = url + ".com"
                    url = url.replace(" ", "")
                    webbrowser.open(url)
            break
        continue

        reply = bard.get_answer(query)["content"]
        audio = bard.speech(reply)

        # Create an in-memory audio stream from the bytes
        audio_stream = io.BytesIO(audio["audio"])

        # Load the MP3 audio into Pygame mixer
        mixer.music.load(audio_stream)

        # Play the audio
        mixer.music.play()

        # Wait for the audio to finish playing
        print(reply)
        while mixer.music.get_busy():
            pass
