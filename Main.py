import threading
import time
from GUImanager import start, getData, root

previous_data = None


def check_data():
    global previous_data
    current_data = getData()

    if current_data != previous_data:
        print("Получены новые данные:", current_data)
        previous_data = current_data

    root.after(2000, check_data)


def console_input():

    while True:
        command = input("\nВведите команду: ").strip()

        if command.lower() == "exit":
            print("Выход из программы...")
            root.quit()
            break

        else:
            print("Неизвестная команда. Доступные команды: data, exit")


threading.Thread(target=console_input(), daemon=True).start()

check_data()
start()