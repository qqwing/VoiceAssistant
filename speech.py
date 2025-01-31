import speech_recognition as sr
import pyttsx3

# Инициализация голосового движка
engine = pyttsx3.init()

# Настройка параметров голоса
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Используем первый доступный голос
engine.setProperty('rate', 200)  # Скорость речи

def speak(text):
    """Озвучивание текста"""
    engine.say(text)
    engine.runAndWait()

import config  # Импортируем файл с конфигурацией

import speech_recognition as sr

recognizer = sr.Recognizer()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Улучшение качества распознавания
        print("Слушаю...")  # Отладочный вывод
        audio = recognizer.listen(source)  # Запись звука

        try:
            command = recognizer.recognize_google(audio, language="ru-RU")  # Распознавание речи
            print(f"Распознано: {command}")  # Отладочный вывод
            return command.lower()
        except sr.UnknownValueError:
            print("Не удалось распознать речь.")  # Отладка
            return None
        except sr.RequestError:
            print("Ошибка подключения к сервису распознавания.")  # Отладка
            return None
