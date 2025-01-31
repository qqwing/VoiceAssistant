import datetime
import requests
import os
from dotenv import load_dotenv
from speech import speak
import hints

# Загрузка API ключа из .env файла
load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

def show_hints():
    """Выводит все доступные команды"""
    hint_text = hints.get_hints()  # получение всех команд
    speak(f"Вот все доступные команды:\n{hint_text}")

def get_time():
    """Сообщает текущее время"""
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    speak(f"Сейчас {current_time}")


def get_weather(city):
    """Получает и озвучивает погоду в указанном городе"""
    if not api_key:
        speak("Ошибка: API ключ для погоды не найден.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] != "404":
            temperature = data["main"]["temp"]
            description = data["weather"][0]["description"]
            speak(f"В городе {city} сейчас {temperature} градусов Цельсия, {description}.")
        else:
            speak("Город не найден.")
    except requests.exceptions.RequestException:
        speak("Ошибка при запросе к сервису погоды.")


from alarm import add_alarm
def set_alarm(time_str):
    """Устанавливает будильник"""
    add_alarm(time_str)
