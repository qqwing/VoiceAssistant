import time
import threading
from datetime import datetime
from speech import speak

alarms = []  # Список будильников

def add_alarm(alarm_time):
    """Добавляет новый будильник"""
    alarms.append(alarm_time)
    speak(f"Будильник установлен на {alarm_time}")

def check_alarms():
    """Проверяет список будильников и запускает их"""
    while True:
        now = datetime.now().strftime("%H:%M")
        if now in alarms:
            speak("Будильник! Время вставать!")
            alarms.remove(now)  # Удаляем будильник после срабатывания
        time.sleep(30)  # Проверка каждую минуту

# Запуск фонового потока для проверки будильников
threading.Thread(target=check_alarms, daemon=True).start()
