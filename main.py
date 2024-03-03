import speech_recognition as sr
import os
import pyttsx3
from openai import OpenAI
from config import apikey
import datetime

chatStr = ""
def chatbot(query):
    global chatStr
    #print(chatStr)
    client = OpenAI(api_key=apikey)
    chatStr += f"Tanny: {query}\n assistant: "
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {
            "role": "system",
            "content": "You are a very good technical and emotional assistant, you provide me with lots of alternative options and solve my problems"
        },
        {
            "role": "user",
            "content": query
        }
        ],
        temperature=1,
        max_tokens=250,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    say(response.choices[0].message.content)
    chatStr += f"{response.choices[0].message.content}\n"
    return response.choices[0].message.content

def ai(prompt):
    client = OpenAI(api_key=apikey)
    text = f"AI response of promt : {prompt} \n ******** \n\n"

    response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {
        "role": "system",
        "content": "You are a very good technical and emotional assistant, you provide me with lots of alternative options and solve my problems"
      },
      {
        "role": "user",
        "content": prompt
      }
    ],
    temperature=1,
    max_tokens=250,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )

    print(response.choices[0].message.content)
    text += response.choices[0].message.content
    if not os.path.exists("Openai"):
        os.makedirs("Openai")

    with open(f"Openai/{''.join(prompt.split('can you write')[1:30])}.txt", "w", encoding='utf-8') as f:
        f.write(text)

def say(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r= sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 0.5
        audio = r.listen(source)  
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query
        except sr.UnknownValueError:
            print("Sorry, I didn't get that. Could you say it again please?")
            return "Sorry, I didn't get that."
    

if __name__ == '__main__':
    print("Python")
    say("Hello, I am Tanmay's Assistant")
    
    while True:
        print("Running...")
        query = takeCommand()
        operation = False
        sites = [["youtube", "https://www.youtube.com"],["wikipedia", "https://www.wikipedia.com"],["github" , "https://www.github.com"],
                 ["google", "https://www.google.com"],["facebook", "https://www.facebook.com"],["instagram", "https://www.instagram.com"]]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f" , Opening {site[0]} sir...")
                os.system(f"start chrome {site[1]}")
                operation = True
                

        if "the time" in  query.lower():
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            say(f"Sir, the time is {strTime}")

        elif "can you write".lower() in query.lower():
            ai(prompt = query)
        
        elif "exit" in query.lower():
            say("Goodbye sir, have a nice day")
            break

        else:
            if(operation == False):
                chatbot(query)