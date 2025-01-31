import config
import time
from speech import speak, listen
import commands
import threading
import sys

# Флаг активности
is_active = False

def listen_for_commands():
    global is_active
    while is_active:
        print("Слушаю команды...")  # Отладочный вывод
        command = listen()  # Слушаем команды
        print(f"Слышал команду: {command}")  # Отладочный вывод

        if command:
            print(f"Команда: {command}")  # Отладочный вывод

            if 'время' in command:
                print("Распознана команда: время")  # Отладочный вывод
                commands.get_time()

            elif 'погода' in command:
                print("Распознана команда: погода")  # Отладочный вывод
                speak("Назовите город.")
                city = listen()
                if city:
                    commands.get_weather(city)

            elif 'выход' in command or 'стоп' in command:
                speak("До свидания!")
                is_active = False  # Завершаем программу
                sys.exit()

            elif 'будильник' in command:
                speak("На какое время установить будильник? Формат: часы и минуты.")
                alarm_time = listen()
                if alarm_time:
                    commands.set_alarm(alarm_time)

            elif 'ожидай' in command:
                speak("Ожидаю.")  # Подтверждаем, что ассистент в режиме ожидания
                is_active = False  # Ожидаем нового активационного слова
                return  # Завершаем только текущий цикл прослушивания команд

            elif 'подсказки' in command:
                print("Распознана команда: подсказки")  # Отладочный вывод
                commands.show_hints()

            else:
                speak("Извините, я не знаю такой команды.")

        else:
            print("Не удалось распознать команду, продолжаю ожидание...")

    print("Завершаю прослушивание команд...")

# Поток для прослушивания активационной фразы
def listen_for_activation():
    global is_active
    while True:
        print("Ожидаю активацию...")  # Отладочный вывод
        command = listen()  # Слушаем активационную фразу
        print(f"Слушаем для активации: {command}")  # Отладочный вывод

        if command:  # Проверяем, что команда распознана
            if config.KEY_PHRASE.lower() in command.lower():  # Если распознана активационная фраза
                print(f"Активирована фраза: {config.KEY_PHRASE}")
                speak(f"Я вас слушаю.")
                is_active = True  # Переключаем флаг на активное состояние
                print("Активировано! Перехожу к прослушиванию команд.")  # Вывод для отладки
                listen_for_commands()  # Перехожу к прослушиванию команд

        time.sleep(1)  # Повторное слушание через 1 секунду

def greet():
    """Приветствие ассистента"""
    speak(f"Здравствуйте, я {config.KEY_PHRASE}. Я готов помочь.")
    speak(f"Для получения помощи скажите 'Подсказки' после обращение ко мне командой {config.KEY_PHRASE}.")

def run_alarm_check():
    """Запуск проверки будильников в фоновом потоке"""
    from alarm import check_alarms
    threading.Thread(target=check_alarms, daemon=True).start()  # Запускаем проверку будильников в фоновом потоке

if __name__ == "__main__":
    greet()

    run_alarm_check()  # Запускаем фоновую проверку будильников

    # Запуск потока для активационной фразы
    listen_for_activation()  # Теперь этот поток сразу активирует прослушивание команд
