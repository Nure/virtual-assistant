import os
import speech_recognition as sr
import webbrowser
import playsound
from gtts import gTTS

from datetime import datetime
import time
import random

# obtain audio from the microphone
r = sr.Recognizer()


def record_audio(question=False):
    with sr.Microphone() as source:
        if question:
            matchina_speaks(question)
        audio = r.listen(source)

        voice_data = ''
        # recognize speech using Google Speech Recognition
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            matchina_speaks('Sorry! I did not recognixe your voice')
        except sr.RequestError:
            matchina_speaks('Aplogize, my speech service is not functional')
        return voice_data


def matchina_speaks(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    rand = random.randint(1, 10000000)
    audio_file = 'audio-' + str(rand) + '.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)


def respond(voice_data):
    if 'name' in voice_data:
        matchina_speaks('My name is Matchina')

    if 'time' in voice_data or 'date' in voice_data:
        matchina_speaks(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

    if 'search' in voice_data:
        search = record_audio('what do you wnna search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        matchina_speaks('Here is what I found for ' + search)

    if 'location' in voice_data:
        location = record_audio('what is the location?')
        url = 'https://www.google.com/maps/place/' + location
        webbrowser.get().open(url)
        matchina_speaks('Here is the location of ' +
                        location + ' in google map')
    
    if 'music' in voice_data:
        music = record_audio('what music I should play for you?')
        url = 'https://www.youtube.com/results?search_query=' + music
        webbrowser.get().open(url)
        matchina_speaks('Here is your music for ' +
                        music + ' on Youtube, enjoy!')
    
    if any(item in voice_data for item in ('stop', 'thanks', 'thank you', 'exit')):
        matchina_speaks('Glad I could help, I am going off. Thank you!')
        exit()


time.sleep(1)
matchina_speaks("Hi, Matchina here, How can I help you")
while 1:
    voice_data = record_audio()
    respond(voice_data)
