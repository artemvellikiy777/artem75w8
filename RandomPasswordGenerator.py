import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os
from datetime import datetime

# ========== Конфигурация ==========
HISTORY_FILE = "history.json"
MIN_LENGTH = 4
MAX_LENGTH = 50

# ========== Работа с историей ==========
def load_history():
    """Загружает историю паролей из JSON файла"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_history(history):
    """Сохраняет историю паролей в JSON файл"""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=4)
    except IOError:
        messagebox.showerror("Ошибка", "Не удалось сохранить историю!")

def add_to_history(password, settings):
    """Добавляет новый пароль в историю"""
    history = load_history()
    history.append({
        "password": password,
        "length": settings["length"],
        "use_digits": settings["use_digits"],
        "use_letters": settings["use_letters"],
        "use_symbols": settings["use_symbols"],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_history(history)
    return history

# ========== Генерация пароля ==========
def generate_password():
    """Генерирует пароль на основе выбранных параметров"""
    try:
        # Получаем длину пароля
        length = int(length_var.get())
        
        # Проверка длины
        if length < MIN_LENGTH:
            messagebox.showwarning(
                "Предупреждение",
                f"Длина пароля не может быть меньше {MIN_LENGTH} символов!"
            )
            length_var.set(MIN_LENGTH)
            return
        if length > MAX_LENGTH:
            messagebox.showwarning(
                "Предупреждение",
                f"Длина пароля не может быть больше {MAX_LENGTH} символов!"
            )
            length_var.set(MAX_LENGTH)
            return
        
        # Получаем настройки
        use_digits = digits_var.get()
        use_letters = letters_var.get()
        use_symbols = symbols_var.get()
        
        # Проверяем, что выбран хотя бы один тип символов
        if not (use_digits or use_letters or use_symbols):
            messagebox.showwarning(
                "Предупреждение",
                "Выберите хотя бы один тип символов!"
            )
            return
        
        # Формируем пул символов
        characters = ""
        if use_digits:
            characters += string.digits  # 0-9
        if use_letters:
            characters += string.ascii_letters  # a-z A-Z
        if use_symbols:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Генерируем пароль
        password = ''.join(random.choice(characters) for _ in range(length))
        
        # Отображаем пароль
        password_var.set(password)
        
        # Сохраняем в историю
        settings = {
            "length": length,
            "use_digits": use_digits,
            "use_letters": use_letters,
            "use_symbols": use_symbols
        }
        history = add_to_history(password, settings)
        update_history_table(history)
        
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите корректное число!")

def update_history_table(history):
    """Обновляет таблицу истории"""
    # Очищаем таблицу
    for row in history_table.get_children():
        history_table.delete(row)
    
    # Добавляем записи (показываем последние 10)
    for entry in reversed(history[-10:]):
        history_table.insert("", "end", values=(
            entry["password"],
            entry["length"],
            "✅" if entry["use_digits"] else "❌",
            "✅" if entry["use_letters"] else "❌",
            "✅" if entry["use_symbols"] else "❌",
            entry["date"]
        ))

def copy_to_clipboard():
    """Копирует сгенерированный пароль в буфер обмена"""
    password = password_var.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")
    else:
        messagebox.showwarning("Предупреждение", "Нет пароля для копирования!")

def clear_history():
    """Очищает историю паролей"""
    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю?"):
        save_history([])
        update_history_table([])
        messagebox.showinfo("Успех", "История очищена!")

# ========== Создание GUI ==========
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("750x600")
root.resizable(False, False)
root.configure(bg="#f5f5f5")

# Переменные
length_var = tk.IntVar(value=12)
digits_var = tk.BooleanVar(value=True)
letters_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)
password_var = tk.StringVar()

# ========== Верхняя панель (настройки) ==========
main_frame = tk.Frame(root, bg="#f5f5f5")
main_frame.pack(pady=10, padx=20, fill="both", expand=True)

# Заголовок
title_label = tk.Label(
    main_frame,
    text="🔐 Генератор случайных паролей",
    font=("Arial", 18, "bold"),
    bg="#f5f5f5",
    fg="#333333"
)
title_label.grid(row=0, column=0, columnspan=3, pady=10)

# Ползунок длины пароля
length_frame = tk.LabelFrame(main_frame, text="Длина пароля", font=("Arial", 10, "bold"), bg="#f5f5f5")
length_frame.grid(row=1, column=0, columnspan=3, pady=10, padx=5, sticky="ew")

length_scale = tk.Scale(
    length_frame,
    from_=MIN_LENGTH,
    to=MAX_LENGTH,
    orient=tk.HORIZONTAL,
    variable=length_var,
    length=400,
    bg="#f5f5f5"
)
length_scale.pack(pady=10)

length_label = tk.Label(
    length_frame,
    textvariable=length_var,
    font=("Arial", 12, "bold"),
    bg="#f5f5f5",
    fg="#4CAF50"
)
length_label.pack()

# Чекбоксы
options_frame = tk.LabelFrame(main_frame, text="Параметры пароля", font=("Arial", 10, "bold"), bg="#f5f5f5")
options_frame.grid(row=2, column=0, columnspan=3, pady=10, padx=5, sticky="ew")

digits_check = tk.Checkbutton(
    options_frame,
    text="Цифры (0-9)",
    variable=digits_var,
    bg="#f5f5f5",
    font=("Arial", 10)
)
digits_check.pack(side=tk.LEFT, padx=20, pady=10)

letters_check = tk.Checkbutton(
    options_frame,
    text="Буквы (A-Z, a-z)",
    variable=letters_var,
    bg="#f5f5f5",
    font=("Arial", 10)
)
letters_check.pack(side=tk.LEFT, padx=20, pady=10)

symbols_check = tk.Checkbutton(
    options_frame,
    text="Спецсимволы (!@#...)",
    variable=symbols_var,
    bg="#f5f5f5",
    font=("Arial", 10)
)
symbols_check.pack(side=tk.LEFT, padx=20, pady=10)

# Кнопка генерации
generate_button = tk.Button(
    main_frame,
    text="🎲 Сгенерировать пароль",
    command=generate_password,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 12, "bold"),
    relief="raised",
    bd=2,
    cursor="hand2"
)
generate_button.grid(row=3, column=0, columnspan=3, pady=15)

# Поле вывода пароля
password_frame = tk.Frame(main_frame, bg="#f5f5f5")
password_frame.grid(row=4, column=0, columnspan=3, pady=10)

password_entry = tk.Entry(
    password_frame,
    textvariable=password_var,
    font=("Courier", 14, "bold"),
    width=35,
    justify="center",
    relief="solid",
    bd=1
)
password_entry.pack(side=tk.LEFT, padx=5)

copy_button = tk.Button(
    password_frame,
    text="📋 Копировать",
    command=copy_to_clipboard,
    bg="#2196F3",
    fg="white",
    font=("Arial", 10, "bold"),
    cursor="hand2"
)
copy_button.pack(side=tk.LEFT, padx=5)

# ========== Нижняя панель (история) ==========
history_frame = tk.LabelFrame(root, text="История паролей (последние 10)", font=("Arial", 10, "bold"), bg="#f5f5f5")
history_frame.pack(pady=10, padx=20, fill="both", expand=True)

# Таблица истории
columns = ("Пароль", "Длина", "Цифры", "Буквы", "Символы", "Дата")
history_table = ttk.Treeview(history_frame, columns=columns, show="headings", height=6)

# Настройка столбцов
history_table.heading("Пароль", text="Пароль")
history_table.heading("Длина", text="Длина")
history_table.heading("Цифры", text="Цифры")
history_table.heading("Буквы", text="Буквы")
history_table.heading("Символы", text="Символы")
history_table.heading("Дата", text="Дата")

history_table.column("Пароль", width=200)
history_table.column("Длина", width=60)
history_table.column("Цифры", width=60)
history_table.column("Буквы", width=60)
history_table.column("Символы", width=60)
history_table.column("Дата", width=150)

scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=history_table.yview)
history_table.configure(yscrollcommand=scrollbar.set)

history_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Кнопка очистки истории
clear_button = tk.Button(
    history_frame,
    text="🗑 Очистить историю",
    command=clear_history,
    bg="#f44336",
    fg="white",
    font=("Arial", 9, "bold"),
    cursor="hand2"
)
clear_button.pack(pady=5)

# Загрузка истории при запуске
history = load_history()
update_history_table(history)

# Запуск приложения
root.mainloop()