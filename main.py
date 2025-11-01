import speech_recognition as sr
import webbrowser
import pyttsx3
import os
import musiclib
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

try:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    print(f"Error configuring Gemini: {e}")
    gemini_model = None

recognizer = sr.Recognizer()
engine = pyttsx3.init("nsss")

def speak(text):
    engine.say(text)
    engine.runAndWait()

def ask_gemini(prompt):
    if not gemini_model:
        return "Sorry, the AI model is not configured correctly."
    
    try:
        print(f"Analysing promt: {prompt}")
        response = gemini_model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        print(f"An error occurred with Gemini: {e}")
        return "Sorry, I couldn't get an answer from the AI."

def processcommand(c):
    if("open youtube" in c.lower()):
        speak("opening youtube")
        print("opening youtube")
        webbrowser.open("https://www.youtube.com")
        
    elif("open google" in c.lower()):
        speak("opening google")
        webbrowser.open("https://www.google.com")
    
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musiclib.music[song]
        print(f"playing {song}")
        speak(f"playing {song}")
        webbrowser.open(link)
        
    else:
        question = c.split(" ", 1)[1]
        
        speak("Let me think...")
        answer = ask_gemini(question)
        print(f"Answer: {answer}")
        
        os.system(f"say{answer}")
        
        speak(answer)

if __name__ == "__main__":
    speak("initialising Igris ")
    print("Initialising Igris! ")
    
    os.system(f"say {"initialising Igris"}")
    
    while True:
        r = sr.Recognizer()
        
        print("recognising...")
        try:
            with sr.Microphone() as source:
                audio = recognizer.listen(source)
                word = recognizer.recognize_google(audio)
                print(word)

                print("Yes how can i help?! ")
                os.system(f"say {"Yes! how can i help"}")

                with sr.Microphone() as source:
                    print("Igris Active! ")
                    audio = recognizer.listen(source)
                    command = recognizer.recognize_google(audio)
                    
                    processcommand(command)
                    
                    break
            
        except Exception as e:
            print("Igris error..".format(e))
