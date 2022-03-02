# import pywhatkit
# import wikipedia
# from pywikihow import RandomHowTo, search_wikihow
# import os
# import speech_recognition as sr
# import webbrowser as web
# import bs4
# import pyttsx3
# from time import sleep
# import requests
# from icrawler.builtin import GoogleImageCrawler
#
# engine = pyttsx3.init('sapi5');
# voices = engine.getProperty('voices')
# engine.setProperty('rate', 170)
# # print(voices)
#
# for voice in voices:
#     # print(voice, voice.id)
#     engine.setProperty('voice', voice.id)
#     # engine.say("Hello World!")
#
# engine.setProperty('voice', voices[1].id)
#
# def Speak(audio):
#     print("  ")
#     print(f": {audio}")
#     print("  ")
#     engine.say(audio)
#     engine.runAndWait()
#
#
# def GoogleSearch(term):
#     query=term.replace("jarvis","")
#     query = query.replace("what is","")
#     query=query.replace("how to","")
#     query=query.replace("what is","")
#     query=query.replace("what do you mean by","")
#     writeab = str(query)
#     file = open("C:\\Users\\91963\\Desktop\\JARVIS\\Data.txt","a")
#     file.write(writeab)
#     file.close()
#     Query = str(term)
#     pywhatkit.search(Query)
#     if 'how to' in Query:
#         max_result = 1
#         how_to_func = search_wikihow(query=Query, max_results= max_result)
#         assert len(how_to_func) == 1
#         how_to_func[0].print()
#         Speak(how_to_func[0].summary)
#     else:
#         search = wikipedia.summary(Query,2)
#         Speak(f"According to your search {search}")
#     google_Crawler = GoogleImageCrawler(storage = {'root_dir': r'C:\Users\91963\Desktop\JARVIS\Images'})
#     google_Crawler.crawl(keyword = writeab, max_num = 2)
#
# def YoutubeSearch(term):
#     result = "https://www.youtube.com/results?search_query=" + term
#     web.open(result)
#     Speak("This is what I found for you Sir")
#     pywhatkit.playonyt(term)
#     Speak("This may also help you Sir")
# Speak("Welcome Back Sir, How can I help you?")
# Function which returns last word
def lastWord(string):

    # taking empty string
    newstring = ""

    # calculating length of string
    length = len(string)

    # traversing from last
    for i in range(length-1, 0, -1):

        # if space is occurred then return
        if(string[i] == " "):

            # return reverse of newstring
            return newstring[::-1]
        else:
            newstring = newstring + string[i]


string = "Learn algorithms at geeksforgeeks"
print(lastWord(string))
