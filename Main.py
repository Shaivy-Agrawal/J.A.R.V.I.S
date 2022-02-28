import pyttsx3
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np
import pywhatkit
import wikipedia
from pywikihow import WikiHow, search_wikihow
import os
import sys
from icrawler.builtin import GoogleImageCrawler
import webbrowser as web


engine = pyttsx3.init('sapi5');
voices = engine.getProperty('voices')
engine.setProperty('rate', 170)
# print(voices)

for voice in voices:
    # print(voice, voice.id)
    engine.setProperty('voice', voice.id)
    # engine.say("Hello World!")

engine.setProperty('voice', voices[0].id)

def Speak(audio):
    print("  ")
    print(f": {audio}")
    print("  ")
    engine.say(audio)
    engine.runAndWait()

def Speak_assistant(audio):
    x = gTTS(audio)
    # playsound(x)
    x.save('assistant.mp3')
    playsound('assistant.mp3')

def Speak_start(path):
    playsound(path)

def TakeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(": Listening ....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print(": Recognizing ...")
        query = r.recognize_google(audio,language='en-in')
        print(f"Your Command : {query}\n")
    except:
        return ""
    # da = open("Data.txt","rb")
    # da.write(f": {query}")
    # da.close
    return query.lower()

def TakeCommand_hindi():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(": Listening ....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print(": Recognizing ...")
        query = r.recognize_google(audio, language="hi")
        print(f": Your Command : {query}\n")
    except:
        return "none"
    return query.lower

def GoogleSearch(term):
    query=term.replace("jarvis","")
    query = query.replace("what is","")
    query=query.replace("how to","")
    query=query.replace("what is","")
    query=query.replace("what do you mean by","")
    query=query.replace("google search","")
    writeab = str(query)
    Query = str(term)
    file = open("C:\\Users\\91963\\Desktop\\JARVIS\\Data.txt","a")
    file.write(Query+"\n")
    file.close()
    pywhatkit.search(query)
    if 'how to' in Query:
        max_result = 1
        how_to_func = search_wikihow(query=query, max_results= max_result)
        assert len(how_to_func) == 1
        Speak(how_to_func[0].summary)
    else:
        search = wikipedia.summary(query,2)
        Speak(f"According to your search {search}")
        Speak("This might also help you sir")
        url="www."+query+".com"
        url = url.replace(" ","")
        web.open(url, new=1)
    google_Crawler = GoogleImageCrawler(storage = {'root_dir': r'C:\Users\91963\Desktop\JARVIS\DataBase\GooglePhotos'})
    google_Crawler.crawl(keyword = writeab, max_num = 10)

def YoutubeSearch(term):
    term = term.replace("youtube search","")
    result = "https://www.youtube.com/results?search_query=" + term
    web.open(result)
    Speak("This is what I found for you Sir")
    pywhatkit.playonyt(term)
    Speak("This may also help you Sir")

def HandGesture():
    cap = cv2.VideoCapture(0)

    mpHands = mp.solutions.hands
    hands = mpHands.Hands()
    mpDraw = mp.solutions.drawing_utils


    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    volMin,volMax = volume.GetVolumeRange()[:2]

    while True:
        success,img = cap.read()
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        lmList = []
        if results.multi_hand_landmarks:
            for handlandmark in results.multi_hand_landmarks:
                for id,lm in enumerate(handlandmark.landmark):
                    h,w,_ = img.shape
                    cx,cy = int(lm.x*w),int(lm.y*h)
                    lmList.append([id,cx,cy])
                mpDraw.draw_landmarks(img,handlandmark,mpHands.HAND_CONNECTIONS)

        if lmList != []:
            x1,y1 = lmList[4][1],lmList[4][2]
            x2,y2 = lmList[8][1],lmList[8][2]

            cv2.circle(img,(x1,y1),4,(255,0,0),cv2.FILLED)
            cv2.circle(img,(x2,y2),4,(255,0,0),cv2.FILLED)
            cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)

            length = hypot(x2-x1,y2-y1)

            vol = np.interp(length,[15,220],[volMin,volMax])
            # print(vol,length)
            volume.SetMasterVolumeLevel(vol, None)

            # Hand range 15 - 220
            # Volume range -63.5 - 0.0

        cv2.imshow('Image',img)
        if cv2.waitKey(1) & 0xff==ord('q'):
            break

def TaskExe():
    while True:
        query = TakeCommand()
        if 'google search' in query:
            GoogleSearch(query)
        elif 'youtube search' in query:
            YoutubeSearch(query)
        elif 'hand gesture' in query:
            HandGesture()
        elif 'bye' in query:
            exit()
        elif 'get lost' in query:
            exit()
        elif 'fuck off' in query:
            exit()
        else:
            print("none")



# Speak_start("C:\\Users\\91963\\Desktop\\JARVIS\\DataBase\\Voices\\Brian\\1.mp3")
Speak("Welcome Back Sir, How can I help you?")
# Speak_assistant("सुप्रभात सर, मैं आपकी कैसे मदद कर सकती हूँ?")
TaskExe()
