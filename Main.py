import os
from dotenv import load_dotenv
import speech_recognition as sr
import pyttsx3
import requests
import datetime

# загрузка переменных окружения из .env файла
load_dotenv()

# получение API ключа из переменных окружения
api_key = os.getenv("OPENWEATHER_API_KEY")

# инициализация голосового движка
engine = pyttsx3.init()

# настройка параметров голоса
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Используем первый доступный голос
engine.setProperty('rate', 200)  # Скорость речи

# функции для синтеза и распознавания речи
def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Слушаю...")
        audio = recognizer.listen(source)
    try:
        command = recognizer.recognize_google(audio, language='ru-RU')
        print(f"Вы сказали: {command}")
        return command.lower()
    except sr.UnknownValueError:
        speak("Извините, я не понял, что вы сказали.")
        return ""
    except sr.RequestError:
        speak("Ошибка сервиса распознавания речи.")
        return ""

# голосовые команды
def get_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    speak(f"Сейчас {current_time}")

def get_weather(city):
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        main = data["main"]
        weather_description = data["weather"][0]["description"]
        temperature = main["temp"]
        speak(f"В городе {city} сейчас {temperature} градусов Цельсия, {weather_description}.")
    else:
        speak("Город не найден.")

def greet():
    speak("Запуск. Выбери команду: время или погода. Для отключения произнеси - выход")

# основной цикл
if __name__ == "__main__":
    greet()
    while True:
        command = listen()
        if 'время' in command:
            get_time()
        elif 'погода' in command:
            speak("Назовите город.")
            city = listen()
            if city:
                get_weather(city)
        elif 'выход' in command or 'стоп' in command:
            speak("До свидания!")
            break
        else:
            speak("Извините, я не знаю такой команды.")
