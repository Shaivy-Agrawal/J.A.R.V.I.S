import pywhatkit
import wikipedia
from pywikihow import RandomHowTo, search_wikihow
import os
import speech_recognition as sr
import webbrowser as web
import bs4
import pyttsx3
from time import sleep
import requests
from icrawler.builtin import GoogleImageCrawler

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

def Speak(audio):
    print("  ")
    print(f": {audio}")
    print("  ")
    engine.say(audio)
    engine.runAndWait()


def GoogleSearch(term):
    query=term.replace("jarvis","")
    query = query.replace("what is","")
    query=query.replace("how to","")
    query=query.replace("what is","")
    query=query.replace("what do you mean by","")
    writeab = str(query)
    file = open("C:\\Users\\91963\\Desktop\\JARVIS\\Data.txt","a")
    file.write(writeab)
    file.close()
    Query = str(term)
    pywhatkit.search(Query)
    if 'how to' in Query:
        max_result = 1
        how_to_func = search_wikihow(query=Query, max_results= max_result)
        assert len(how_to_func) == 1
        how_to_func[0].print()
        Speak(how_to_func[0].summary)
    else:
        search = wikipedia.summary(Query,2)
        Speak(f"According to your search {search}")
    google_Crawler = GoogleImageCrawler(storage = {'root_dir': r'C:\Users\91963\Desktop\JARVIS\Images'})
    google_Crawler.crawl(keyword = writeab, max_num = 2)

def YoutubeSearch(term):
    result = "https://www.youtube.com/results?search_query=" + term
    web.open(result)
    Speak("This is what I found for you Sir")
    pywhatkit.playonyt(term)
    Speak("This may also help you Sir")
