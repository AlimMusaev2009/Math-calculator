import tkinter as tk

root = tk.Tk()
root.geometry('350x450')
root.title('calculator')

# Метка для вывода (заменил lable на label для грамотности, но оставил ваше имя переменной)
lable = tk.Label(root, width=250, height=5, background="white", anchor="e", font=("Arial", 14))
lable.pack(padx=10, pady=10)

result = ""  # Здесь храним текущее выражение


def insert_value(value):
    global result
    # Список операторов
    operators = ["+", "-", "*", "/", "%"]

    # Если нажали "=", вызываем математику
    if value == "=":
        maths()
        return

    # ЛОГИКА ЗАМЕНЫ ОПЕРАТОРА:
    # Если текущий ввод заканчивается на оператор, и мы нажали оператор
    if len(result) > 0 and result[-1] in operators and value in operators:
        # Заменяем последний символ на новый
        result = result[:-1] + value
    else:
        # ЛОГИКА ЗАПРЕТА ОПЕРАТОРА В НАЧАЛЕ:
        # Если строка пустая и нажат оператор (кроме минуса для отрицательных чисел)
        if len(result) == 0 and value in operators:
            if value == "-":  # Разрешаем минус в начале
                result += value
            else:
                return  # Игнорируем нажатие
        else:
            result += value

    lable.config(text=result)
    print(result)


def maths():
    global result
    try:
        out = str(eval(result))
        lable.config(text=out)
        result = out

    except Exception:
        lable.config(text="Ошибка")
        result = ""


def init():
    # Создаем фреймы один раз
    frame_top = tk.Frame(root, width=350, height=100, background='black')
    frame_bottom_left = tk.Frame(root, width=300, height=350, background='gray')
    frame_bottom_right = tk.Frame(root, width=100, height=350, background='white')
    return [frame_top, frame_bottom_left, frame_bottom_right]


def gui():
    frames = init()

    # Упаковываем только нужные фреймы
    frames[1].pack(side="left", padx=10, pady=15)
    frames[2].pack(side="right", padx=10, pady=15)

    # Кнопки с цифрами
    col = 0
    row = 0
    for step in range(10):
        button = tk.Button(frames[1], text=step, width=8, height=4, command=lambda value=str(step): insert_value(value))
        button.grid(row=row, column=col)
        col += 1
        if col == 3:
            col = 0
            row += 1

    # Кнопки операций
    operations = ["+", "-", "*", "/", "="]
    for step in range(len(operations)):
        op = operations[step]
        button = tk.Button(frames[2], text=op, width=7, height=3, command=lambda value=op: insert_value(value))
        button.grid(row=step, column=1)


gui()
root.mainloop()