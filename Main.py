from datetime import date
from random import choice
from allPackage import *

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('rate', 170)
# print(voices)

api_weather = "6035ecb9ddbe4b9dc4d4fdd31a8325bf"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

for voice in voices:
    # print(voice, voice.id)
    engine.setProperty('voice', voice.id)
    # engine.say("Hello World!")

engine.setProperty('voice', voices[0].id)

# FEATURES


def Speak(text):
    print("  ")
    print(f": {text}")
    print("  ")
    engine.say(text)
    engine.runAndWait()


def Speak_assistant(text):
    x = gTTS(text)
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
        query = r.recognize_google(audio, language='en-in')
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
    query = term.replace("jarvis", "")
    query = query.replace("what is", "")
    query = query.replace("how to", "")
    query = query.replace("what is", "")
    query = query.replace("what do you mean by", "")
    query = query.replace("google search", "")
    writeab = str(query)
    Query = str(term)
    file = open("C:\\Users\\91963\\Desktop\\JARVIS\\Data.txt", "a")
    file.write(Query+"\n")
    file.close()
    pywhatkit.search(query)
    if 'how to' in Query:
        max_result = 1
        how_to_func = search_wikihow(query=query, max_results=max_result)
        assert len(how_to_func) == 1
        Speak(how_to_func[0].summary)
    else:
        search = wikipedia.summary(query, 2)
        Speak(f"According to your search {search}")
        Speak("This might also help you sir")
        url = "www."+query+".com"
        url = url.replace(" ", "")
        web.open(url, new=1)
    google_Crawler = GoogleImageCrawler(
        storage={'root_dir': r'C:\Users\91963\Desktop\JARVIS\DataBase\GooglePhotos'})
    google_Crawler.crawl(keyword=writeab, max_num=10)


def YoutubeSearch(term):
    term = term.replace("youtube search", "")
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

    volMin, volMax = volume.GetVolumeRange()[:2]

    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)

        lmList = []
        if results.multi_hand_landmarks:
            for handlandmark in results.multi_hand_landmarks:
                for id, lm in enumerate(handlandmark.landmark):
                    h, w, _ = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    lmList.append([id, cx, cy])
                mpDraw.draw_landmarks(
                    img, handlandmark, mpHands.HAND_CONNECTIONS)

        if lmList != []:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]

            cv2.circle(img, (x1, y1), 4, (255, 0, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 4, (255, 0, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

            length = hypot(x2-x1, y2-y1)

            vol = np.interp(length, [15, 220], [volMin, volMax])
            # print(vol,length)
            volume.SetMasterVolumeLevel(vol, None)
            # Hand range 15 - 220
            # Volume range -63.5 - 0.0

        cv2.imshow('Image', img)
        if cv2.waitKey(1) & 0xff == ord('q'):
            break


def currentTime():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    compare_time = now.strftime("12:00")
    if(current_time < compare_time):
        Speak(f"Good Morning Sir, it is {current_time}")
    else:
        Speak(f"Good Evening Sir, it is {current_time}")


def fetchLocation():
    g = geocoder.ip('me')
    geoLoc = Nominatim(user_agent="GetLoc")
    locname = geoLoc.reverse(g.latlng)
    Speak(locname.address)


def fetchWeather(query):
    lis = list(query.split(" "))
    length = len(lis)
    city_name = lis[length-1]
    print(city_name)
    complete_url = base_url + "appid=" + api_weather + \
        "&q=" + city_name + "&units=metric"
    response = requests.get(complete_url)
    x = response.json()
    if x["cod"] != "404":
        y = x["main"]
        current_temperature = y["temp"]
        z = x["weather"]
        weather_desc = z[0]["description"]
        final_weather = weather_desc + "y"
        Speak(
            f"The temprature in {city_name} is {current_temperature} centigrade and it is {final_weather}")
    else:
        print("City Not Found")

# TASK EXECUTION FUNCTION


def TaskExe():
    while True:
        query = TakeCommand()
        tag = any(word in query.lower() for word in quit_tags)

        if 'wake up' in query:
            currentTime()
            continue
        if not tag:
            Speak(choice(opening_text))
            if 'google search' in query:
                GoogleSearch(query)
            elif 'youtube search' in query:
                YoutubeSearch(query)
            elif 'hand gesture' in query:
                HandGesture()
            elif 'location' in query:
                fetchLocation()
            elif 'weather' in query:
                fetchWeather(query)
            else:
                Speak("Sorry Sir, I didn't get you")
        else:
            if 'get lost' in query:
                Speak('Alright, No need to be rude, I will leave you alone')
                exit()
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                Speak("Good Night Sir, Take care!")
            else:
                Speak(choice(closing_text))
            exit()


# FUNCTION CALLS
# Speak_start("C:\\Users\\91963\\Desktop\\JARVIS\\DataBase\\Voices\\Brian\\1.mp3")
# Speak_assistant("सुप्रभात सर, मैं आपकी कैसे मदद कर सकती हूँ?")
Speak("Welcome Back Sir, How can I help you?")
TaskExe()
