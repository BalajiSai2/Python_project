#pip install SpeechRecognition
import speech_recognition as sr
import webbrowser
import pyttsx3 #old speak
import musicLibary
import requests
#pip install openai
from openai import OpenAI
#pip install gtts
from gtts import gTTS #google text to speak #it help in gving poper sound and change the langauage
import pygame
# Graphics Rendering – Draw shapes, images, and animations.
# Sound and Music – Play and mix sound effects and background music.
# Event Handling – Detect keyboard, mouse, and joystick inputs.
# Game Loop Management – Runs smoothly at a controlled frame rate.
# Cross-Platform – Works on Windows, Mac, and Linux.
import os
# pip install pyaudio
#pip install pocketsphinx
# pocketsphinx is a lightweight speech recognition engine from 
# CMU Sphinx, designed for offline voice recognition. Unlike 
# cloud-based solutions like Google Speech Recognition, pocketsphinx 
# works locally, making it ideal for embedded systems, IoT, and privacy-sensitive 
# applications.

#pip install youtube-search-python
#pip install youtube_search
from youtube_search import YoutubeSearch

#intialization and object/instance creation
engine=pyttsx3.init()
newsapi="<your Key Here>"

def speak_old(text):
    engine.say(text) # Convert text to speech
    engine.runAndWait() # Wait for the speech to complete
    
def speak(text):
    #convert text to speech
    tts=gTTS(text) 
    tts.save('temp.mp3')
    
    #Intialize Pygame mixer
    pygame.mixer.init()
    
    #load the mp3 file
    pygame.mixer.music.load('temp.mp3')
    
    #play the mp3 file
    pygame.mixer.music.play()
    
    #keep the program running untill the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)#prevents high CPU usage while waiting.
        
    pygame.mixer.music.unload()#unload the music
    os.remove("temp.mp3")# deletes the temporary file to free up space

def aiProcess(command):
    #create instance by api key
    client=OpenAI(api_key="<Your Key Here>",)
    
    completion=client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":"You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},#system saying what type to get
            {"role":"user","content":command}#user say what to get
        ]
    )
    return completion.choices[0].message.content

#sucessful api give as jscon

# {
#   "id": "chatcmpl-123456",
#   "object": "chat.completion",
#   "created": 1700000000,
#   "model": "gpt-4o",
#   "choices": [
#     {
#       "index": 0,
#       "message": {
#         "role": "assistant",
#         "content": "Why don’t skeletons fight each other? They don’t have the guts!"
#       },
#       "finish_reason": "stop"
#     }
#   ],
#   "usage": {
#     "prompt_tokens": 10,
#     "completion_tokens": 15,
#     "total_tokens": 25
#   }
# }

def processCommand(c):
    if "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com")
    elif "open google" in c.lower():
        webbrowser.open("https://www.google.com")
    elif c.lower().startswith("play"):
        #song in musicLibrary module
        
        # song=c.lower().split(" ")[1]
        # link=musicLibary.music[song]
        # webbrowser.open(link)
        
        #direct song bt name opens the tabe related to search
        
        # song=c.lower().split(" ")[1:]
        # song="+".join(song)
        # search_url = f"https://www.youtube.com/results?search_query={song}"
        # webbrowser.open(search_url)
        
        #Dirct play the song in youbute
        
        song = " ".join(c.lower().split(" ")[1:])  # Extract song name
        results = YoutubeSearch(song, max_results=1).to_dict()  # Search YouTube

        if results:
            video_id = results[0]["id"]  # Get first video ID
            video_url = f"https://www.youtube.com/watch?v={video_id}"  # Build URL
            webbrowser.open(video_url)  # Open video directly

    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()

            # Extract the articles
            articles = data.get('articles', [])

            # Print the headlines
            for article in articles:
                speak(article['title'])
    else:
        # Let OpenAI handle the request
        output = aiProcess(c)
        speak(output)


if __name__=="__main__":
    speak("Initializing Jarvis....")
    while True:
        #Listen for the wake "Jarvis"
        #Obtain audio from the microphone
        r=sr.Recognizer()# Initialize the recognizer
        
        print("recognizing...")
        try:
            with sr.Microphone() as source:  # Open the microphone
                #Uses a with statement to automatically close the microphone after use
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)  # Capture audio
                word = r.recognize_google(audio)  # Convert speech to text
                # timeout=2 → Waits a maximum of 2 seconds for the user to start speaking.
                # phrase_time_limit=1 → Stops recording after 1 second of speech
                if(word.lower()=="jarvis"):
                    speak("Ya")
                    #Lsiten the Commands
                    with sr.Microphone() as source:
                        print("Jarvis Active...")
                        audio=r.listen(source)
                        # r.listen(source) will listen until you stop speaking or there is a long pause in your speech.
                        # There is no automatic timeout unless explicitly set
                        command=r.recognize_google(audio)
                        
                        processCommand(command)
        except Exception as e:
            print("Error;{0}".format(e))
            
# from youtube_search import YoutubeSearch
# import webbrowser

# def play_first_youtube_video(query):
#     results = YoutubeSearch(query, max_results=1).to_dict()
#     if results:
#         video_id = results[0]["id"]
#         webbrowser.open(f"https://www.youtube.com/watch?v={video_id}")

# # Example: Play the first result for "Python tutorial"
# play_first_youtube_video("Python tutorial")

                                 