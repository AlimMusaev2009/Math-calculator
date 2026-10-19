import tkinter as tk

root = tk.Tk()
root.geometry('350x450')
root.title('calculator')

lable = tk.Label(root, width=250, height=5, background="white", anchor="e", font=("Arial", 14))
lable.pack(padx=10, pady=10)

result = ""


def insert_value(value):
    global result
    operators = ["+", "-", "*", "/", "%"]
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


# --- Пункт 6: 5 функций ---
def summy(a, b):
    return a + b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError
    return a / b


def diff(a, b):
    return a - b


def result_math(expr):
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i].isdigit() or expr[i] == '.':
            num = ""
            while i < len(expr) and (expr[i].isdigit() or expr[i] == '.'):
                num += expr[i]
                i += 1
            tokens.append(float(num))
        elif expr[i] in "+-*/%":
            tokens.append(expr[i])
            i += 1
        else:
            i += 1

    if not tokens:
        return 0

    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def consume():
        nonlocal pos
        val = tokens[pos]
        pos += 1
        return val

    def parse_factor():
        if peek() == "-":
            consume()
            return -parse_factor()
        val = consume()
        if isinstance(val, float):
            return val
        raise ValueError("Ожидалось число")

    def parse_term():
        left = parse_factor()
        while peek() in ("*", "/", "%"):
            op = consume()
            right = parse_factor()
            if op == "*":
                left = multiply(left, right)
            elif op == "/":
                left = divide(left, right)
            elif op == "%":
                left = left % right
        return left

    def parse_expr():
        left = parse_term()
        while peek() in ("+", "-"):
            op = consume()
            right = parse_term()
            if op == "+":
                left = summy(left, right)
            else:
                left = diff(left, right)
        return left

    return parse_expr()


def maths():
    global result
    try:
        res = result_math(result)

        if res == int(res):
            out = str(int(res))
        else:
            out = str(res)

        lable.config(text=out)
        result = out

    except Exception:
        lable.config(text="Ошибка")
        result = ""


def init():
    frame_top = tk.Frame(root, width=350, height=100, background='black')
    frame_bottom_left = tk.Frame(root, width=300, height=350, background='gray')
    frame_bottom_right = tk.Frame(root, width=100, height=350, background='white')
    return [frame_top, frame_bottom_left, frame_bottom_right]


def gui():
    frames = init()

    frames[1].pack(side="left", padx=10, pady=15)
    frames[2].pack(side="right", padx=10, pady=15)

    col = 0
    row = 0
    for step in range(10):
        button = tk.Button(frames[1], text=step, width=8, height=4, command=lambda value=str(step): insert_value(value))
        button.grid(row=row, column=col)
        col += 1
        if col == 3:
            col = 0
            row += 1

    operations = ["+", "-", "*", "/", "="]
    for step in range(len(operations)):
        op = operations[step]
        button = tk.Button(frames[2], text=op, width=7, height=3, command=lambda value=op: insert_value(value))
        button.grid(row=step, column=1)


gui()
root.mainloop()
