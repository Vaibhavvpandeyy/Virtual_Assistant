# --- 1. IMPORTING LIBRARIES ---
# We import all the 'toolkits' we need for our program to work.

import speech_recognition as sr  # This library lets us listen to voice from the microphone and turn it into text.
import webbrowser                # This library lets us open web pages in a browser (like Chrome, Safari, etc.).
import pyttsx3                   # This library lets us turn text into spoken audio.
import os                        # This library lets us interact with the operating system (e.g., run commands, get environment variables).
import musiclib                  # This is likely a custom file you created (musiclib.py) that has a dictionary of songs.
import google.generativeai as genai # This is the official library from Google to use their Gemini AI models.
from dotenv import load_dotenv   # This function helps us load "secret" variables (like API keys) from a file named .env

# --- 2. SETUP AND CONFIGURATION ---

# Load variables from the .env file (this is where your GEMINI_API_KEY should be stored)
load_dotenv()

# We use 'try...except' to gracefully handle errors.
try:
    # Configure the Gemini library with your secret API key.
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

    # Create an instance of the Gemini AI model we want to talk to.
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    # print("Gemini model loaded successfully.") # A good test line to uncomment if you have problems.

except Exception as e:
    # If anything goes wrong (e.S., wrong API key, no internet), print an error message.
    print(f"Error configuring Gemini: {e}")
    gemini_model = None # Set the model to 'None' so we know it's not working.

# Create the main object for recognizing speech.
recognizer = sr.Recognizer()

# Initialize the text-to-speech (TTS) engine.
# "nsss" is a voice engine identifier, often used on macOS. Windows might use "sapi5".
engine = pyttsx3.init("nsss")


# --- 3. DEFINING HELPER FUNCTIONS ---
# Functions are reusable blocks of code.

def speak(text):
    """This function takes any text and speaks it out loud."""
    engine.say(text)      # Tell the engine what text to say.
    engine.runAndWait() # Tell the engine to "run" (speak) and "wait" until it's finished.

def ask_gemini(prompt):
    """This function sends a question (prompt) to the Gemini AI and returns its answer."""
    
    # First, check if the Gemini model was loaded correctly.
    if not gemini_model:
        return "Sorry, the AI model is not configured correctly."
    
    try:
        # Let the user know in the terminal that the AI is working.
        print(f"Analysing promt: {prompt}")
        
        # Send the user's prompt to the AI and get a response.
        response = gemini_model.generate_content(prompt)
        
        # Return only the text part of the AI's response.
        return response.text
    
    except Exception as e:
        # If the AI request fails, tell the user.
        print(f"An error occurred with Gemini: {e}")
        return "Sorry, I couldn't get an answer from the AI."

def processcommand(c):
    """This function figures out what to do based on the command 'c'."""
    
    # We use .lower() to make the command case-insensitive (so "Open YouTube" works just like "open youtube").
    if("open youtube" in c.lower()):
        speak("opening youtube")
        print("opening youtube")
        webbrowser.open("https://www.youtube.com") # Opens YouTube in the default browser.
        
    elif("open google" in c.lower()):
        speak("opening google")
        webbrowser.open("https://www.google.com") # Opens Google in the default browser.
    
    elif c.lower().startswith("play"):
        # This assumes the command is "play [songname]"
        song = c.lower().split(" ")[1]  # Get the second word from the command (the song name)
        link = musiclib.music[song]     # Look up the song in your 'musiclib' dictionary to get its link.
        print(f"playing {song}")
        speak(f"playing {song}")
        webbrowser.open(link)           # Open the song's link.
        
    else:
        # If the command isn't one of the above, we assume it's a question for the AI.
        
        # This line tries to get the question part of the command.
        # It splits the command at the *first space* and takes everything *after* it.
        # NOTE: This will crash if the command is only one word (e.g., "hello").
        question = c.split(" ", 1)[1] 
        
        speak("Let me think...")
        answer = ask_gemini(question)   # Send the question to our Gemini function.
        print(f"Answer: {answer}")
        
        # This line also makes the computer speak, but it's a macOS-specific command.
        # It's better to *only* use the 'speak(answer)' line below.
        os.system(f"say{answer}")
        
        # Use our 'speak' function to say the AI's answer.
        speak(answer)

# --- 4. MAIN PROGRAM EXECUTION ---

# This 'if' statement is a standard in Python.
# It means "run the code below only if this script is being run directly."
if __name__ == "__main__":
    speak("initialising baahubali ")
    print("Initialising Bahubali! ")
    
    # Another macOS-specific 'say' command.
    os.system(f"say {"initialising baahubali"}")
    
    # Start an infinite loop to keep the assistant listening.
    while True:
        # Create a new recognizer object (this isn't strictly necessary, but it works).
        r = sr.Recognizer()
        
        print("recognising...")    
        try:
            # Use the 'with' keyword to automatically open and close the microphone.
            with sr.Microphone() as source:
                # Listen for the first bit of audio (this acts as the "wake word")
                audio = recognizer.listen(source)    
                # Convert the audio to text.
                word = recognizer.recognize_google(audio)    
                print(word) # Print what it heard.

                # As soon as it hears *anything*, it assumes it's "awake" and asks for a command.
                print("Yes how can i help?! ")
                os.system(f"say {"Yes! how can i help"}")

                # Open the microphone again to listen for the *actual command*.
                with sr.Microphone() as source:
                    print("Bahubali Active! ")
                    audio = recognizer.listen(source)
                    # Convert the command audio to text.
                    command = recognizer.recognize_google(audio)
                    
                    # Send the text command to our processing function.
                    processcommand(command)
                    
                    # This 'break' statement will STOP the 'while True' loop.
                    # This means your assistant will listen for one command and then shut down.
                    # If you want it to keep listening, you should remove this 'break' line.
                    break 
            
        except Exception as e:
            # Catch any errors during listening (e.g., couldn't understand, no internet).
            print("Bahubali error..".format(e))
