import keyboard
import pyperclip

def print_clipboard_content():
    # Получаем текст из буфера обмена
    clipboard_content = pyperclip.paste()
    # Печатаем содержимое буфера обмена
    print(clipboard_content)

# Назначаем комбинацию клавиш CTRL+P на функцию печати
keyboard.add_hotkey('ctrl+p', print_clipboard_content)

# Запускаем бесконечный цикл, чтобы программа продолжала работать
keyboard.wait('esc')  # Завершить программу можно нажатием клавиши ESC
