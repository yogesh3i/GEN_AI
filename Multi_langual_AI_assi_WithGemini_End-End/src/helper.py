import speech_recognition as sr 
import google.generativeai as genai 
from dotenv import load_dotenv 
import os 
from gtts import gTTS

# load the env 
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

 
def voice_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...") 
        audio = r.listen(source) 

        try:
            text = r.recognize_google(audio)
            print("You said:", text)
            return text 
        except sr.UnknownValueError:
            print("Sorry, I did not understand the audio.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

def llm_model(user_text):
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("models/gemini-1.5-pro-001")
    response = model.generate_content(user_text) 
    result = response.text
    return result

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("output.mp3")
