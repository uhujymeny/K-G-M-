import customtkinter as ctk
from tkinter import simpledialog, messagebox, filedialog
import os
import datetime
import shutil
import re
import webbrowser
from cryptography.fernet import Fernet
from PIL import Image, ImageTk, ImageDraw

# Настройка цветовой темы Material Design 3
ctk.set_appearance_mode("light")

# Цвета
COLORS = {
    "primary": "#6750A4",
    "on_primary": "#FFFFFF",
    "primary_container": "#EADDFF",
    "on_primary_container": "#21005D",
    "secondary": "#625B71",
    "on_secondary": "#FFFFFF",
    "secondary_container": "#E8DEF8",
    "surface": "#FFFBFE",
    "on_surface": "#1C1B1F",
    "surface_variant": "#E7E0EC",
    "outline": "#79747E",
    "outline_variant": "#CAC4D0",
    "background": "#FEF7FF",
    "on_background": "#1C1B1F",
    "error": "#B3261E",
    "on_error": "#FFFFFF",
}

# Шрифты
FONT_FAMILY = None
FONT_NORMAL = None
FONT_BOLD = None
FONT_SMALL = None
FONT_LARGE = None

def setup_fonts():
#Настройка шрифтов
    global FONT_FAMILY, FONT_NORMAL, FONT_BOLD, FONT_SMALL, FONT_LARGE
    FONT_FAMILY = "Arial"
    FONT_NORMAL = (FONT_FAMILY, 14)
    FONT_BOLD = (FONT_FAMILY, 14, "bold")
    FONT_SMALL = (FONT_FAMILY, 12)
    FONT_LARGE = (FONT_FAMILY, 20, "bold")

def load_logo():
    """Загрузка логотипа"""
    logo_paths = [
        "kgm_logo.png",
        "./kgm_logo.png",
        os.path.join(os.path.dirname(__file__), "kgm_logo.png"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "kgm_logo.png")
    ]
    
    for path in logo_paths:
        if os.path.exists(path):
            try:
                image = Image.open(path)
                image = image.resize((40, 40), Image.LANCZOS)
                return ctk.CTkImage(light_image=image, dark_image=image, size=(40, 40))
            except Exception as e:
                print(f"Ошибка загрузки логотипа: {e}")
                break
    

    try:
        # Создаем простой фиолетовый круг как заглушку логотипа
        img = Image.new('RGBA', (40, 40), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse((5, 5, 35, 35), fill=(103, 80, 164, 255))  # Фиолетовый цвет
        draw.text((12, 10), "KGM", fill=(255, 255, 255, 255))  # Белый текст
        return ctk.CTkImage(light_image=img, dark_image=img, size=(40, 40))
    except:
        return None

def show_login_window():
#Старт окно имени
    login_window = ctk.CTkToplevel()
    login_window.title("Вход")
    login_window.geometry("400x300")
    login_window.configure(fg_color=COLORS["background"])
    login_window.resizable(False, False)
   
    login_window.update_idletasks()
    x = (login_window.winfo_screenwidth() - 400) // 2
    y = (login_window.winfo_screenheight() - 300) // 2
    login_window.geometry(f"+{x}+{y}")
    
    ctk.CTkLabel(
        login_window,
        text="💬 Вход в мессенджер",
        text_color=COLORS["primary"],
        font=FONT_LARGE
    ).pack(pady=(40, 10))

    name_entry = ctk.CTkEntry(
        login_window,
        width=250,
        height=45,
        fg_color=COLORS["surface"],
        border_color=COLORS["outline"],
        text_color=COLORS["on_surface"],
        placeholder_text="Введите ваше имя",
        corner_radius=12,
        font=FONT_NORMAL
    )
    name_entry.pack(pady=20)
    name_entry.focus_set()
    
    login_button = ctk.CTkButton(
        login_window,
        text="🚀 Войти",
        width=180,
        height=45,
        fg_color=COLORS["primary"],
        hover_color="#7C67B8",
        text_color=COLORS["on_primary"],
        corner_radius=60,
        font=FONT_BOLD,
        command=lambda: finish_login(login_window, name_entry.get().strip())
    )
    login_button.pack(pady=5)
    
    ctk.CTkButton(
        login_window,
        text="👤 Войти как гость",
        width=180,
        height=40,
        fg_color=COLORS["primary_container"],
        hover_color="#D5C5F5",
        text_color=COLORS["on_primary_container"],
        corner_radius=60,
        font=FONT_NORMAL,
        command=lambda: finish_login(login_window, "Гость")
    ).pack()
    
# Обработка Enter
    name_entry.bind("<Return>", lambda e: finish_login(login_window, name_entry.get().strip()))
    login_window.grab_set()
    login_window.wait_window()
    
    return login_window._result if hasattr(login_window, '_result') else "Гость"

def finish_login(window, username):
    window._result = username or "Гость"
    window.destroy()

#Интерфейс

def create_styled_button(master, text, command, **kwargs):
    base_params = {
        "master": master,
        "text": text,
        "command": command,
        "fg_color": COLORS["primary"],
        "hover_color": "#7C67B8",
        "text_color": COLORS["on_primary"],
        "border_color": COLORS["outline"],
        "border_width": 1,
        "corner_radius": 6,
        "font": FONT_NORMAL
    }
    base_params.update(kwargs)
    return ctk.CTkButton(**base_params)

def create_styled_frame(master, **kwargs):
    return ctk.CTkFrame(
        master,
        fg_color=COLORS["surface"],
        border_color=COLORS["outline_variant"],
        border_width=1,
        corner_radius=8,
        **kwargs
    )

def create_styled_entry(master, **kwargs):
    return ctk.CTkEntry(
        master,
        fg_color=COLORS["surface"],
        border_color=COLORS["outline"],
        text_color=COLORS["on_surface"],
        placeholder_text_color=COLORS["outline"],
        corner_radius=8,
        font=FONT_NORMAL,
        **kwargs
    )

# Пути к файлам
FILE_PATH = "Z:\\messages.txt"
KEY_FILE = "Z:\\secret.key"
VIDEO_DIR = "Z:\\videos"
IMAGE_DIR = "Z:\\images"

def load_key():

    if not os.path.exists(KEY_FILE):
        os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as f:
            f.write(key)
        return key
    
    with open(KEY_FILE, "rb") as f:
        return f.read()

def encrypt_message(message, key):

    f = Fernet(key)
    encrypted_message = f.encrypt(message.encode('utf-8'))
    return encrypted_message.decode('utf-8')

def decrypt_message(encrypted_message, key):

    f = Fernet(key)
    try:
        decrypted_message = f.decrypt(encrypted_message.encode('utf-8'))
        return decrypted_message.decode('utf-8')
    except Exception:
        return f"[Зашифровано другим ключом]"

def detect_urls(text):
    """Поиск URL в тексте"""
    url_pattern = r'(https?://[^\s]+|www\.[^\s]+\.[^\s]+)'
    return re.findall(url_pattern, text)

def read_messages(key):

    if not os.path.exists(FILE_PATH):
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        open(FILE_PATH, "w", encoding="utf-8").close()
        return []

    messages = []
    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    decrypted = decrypt_message(line, key)
                    messages.append(decrypted)
        return messages
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при чтении сообщений: {e}")
        return []

def write_messages(messages, key):

    try:
        os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
        encrypted_messages = [encrypt_message(msg, key) for msg in messages]
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            for msg in encrypted_messages:
                f.write(msg + "\n")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при записи сообщений: {e}")

def append_message(user, message, key, message_type="text"):
    """Добавление нового сообщения"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = {
        "video": f"[{timestamp}] {user} 📹 [ВИДЕО]",
        "image": f"[{timestamp}] {user} 📷 [ИЗОБРАЖЕНИЕ]",
        "text": f"[{timestamp}] {user} 💬"
    }[message_type]
    full_message = f"{prefix}: {message}"
    current_messages = read_messages(key)
    write_messages(current_messages + [full_message], key)
    return full_message

def send_message(user, message_entry, chat_log, key):

    message = message_entry.get()
    if message:
        append_message(user, message, key)
        update_chat_log(chat_log, key)
        message_entry.delete(0, ctk.END)

def send_video(user, chat_log, key):
#Отправка видео
    os.makedirs(VIDEO_DIR, exist_ok=True)
    filetypes = (("Видео файлы", "*.mp4 *.avi *.mov *.mkv"), ("Все файлы", "*.*"))
    video_path = filedialog.askopenfilename(title="Выберите видео", filetypes=filetypes)
    if not video_path:
        return
    try:
        video_filename = os.path.basename(video_path)
        dest_path = os.path.join(VIDEO_DIR, video_filename)
        shutil.copy2(video_path, dest_path)
        append_message(user, f"Видео: {video_filename} (путь: {dest_path})", key, message_type="video")
        update_chat_log(chat_log, key)
        messagebox.showinfo("Успех", f"Видео {video_filename} успешно отправлено!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось отправить видео: {e}")

def send_image(user, chat_log, key):
#Отправка изображения
    os.makedirs(IMAGE_DIR, exist_ok=True)
    filetypes = (("Изображения", "*.jpg *.jpeg *.png *.gif *.bmp"), ("Все файлы", "*.*"))
    image_path = filedialog.askopenfilename(title="Выберите изображение", filetypes=filetypes)
    if not image_path:
        return
    try:
        image_filename = os.path.basename(image_path)
        dest_path = os.path.join(IMAGE_DIR, image_filename)
        shutil.copy2(image_path, dest_path)
        append_message(user, f"Изображение: {image_filename} (путь: {dest_path})", key, message_type="image")
        update_chat_log(chat_log, key)
        messagebox.showinfo("Успех", f"Изображение {image_filename} успешно отправлено!")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось отправить изображение: {e}")

def open_video(key):

    if not os.path.exists(VIDEO_DIR) or not os.listdir(VIDEO_DIR):
        messagebox.showinfo("Видео", "Нет доступных видео для открытия.")
        return
    
    video_window = ctk.CTkToplevel()
    video_window.title("Доступные видео")
    video_window.geometry("500x400")
    video_window.configure(fg_color=COLORS["surface"])
    
    ctk.CTkLabel(video_window, text="Выберите видео для воспроизведения", 
                text_color=COLORS["on_surface"], font=FONT_NORMAL).pack(pady=10)
    
    scrollable_frame = ctk.CTkScrollableFrame(video_window)
    scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    for video in os.listdir(VIDEO_DIR):
        video_frame = create_styled_frame(scrollable_frame)
        video_frame.pack(fill="x", pady=5, padx=5)
        
        ctk.CTkLabel(video_frame, text=video, text_color=COLORS["on_surface"], 
                    font=FONT_NORMAL).pack(side="left", padx=10, pady=5)
        
        def play_video(video_path=os.path.join(VIDEO_DIR, video)):
            try:
                os.startfile(video_path)
            except AttributeError:
                import subprocess
                subprocess.run(['open', video_path])
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть видео: {e}")
        
        create_styled_button(video_frame, text="▶️ Воспроизвести", width=120, height=30,
                           command=play_video).pack(side="right", padx=10, pady=5)

def open_image_in_paint():

    if not os.path.exists(IMAGE_DIR) or not os.listdir(IMAGE_DIR):
        messagebox.showinfo("Изображения", "Нет доступных изображений для открытия.")
        return
    
    image_window = ctk.CTkToplevel()
    image_window.title("Доступные изображения")
    image_window.geometry("500x400")
    image_window.configure(fg_color=COLORS["surface"])
    
    ctk.CTkLabel(image_window, text="Выберите изображение для редактирования", 
                text_color=COLORS["on_surface"], font=FONT_NORMAL).pack(pady=10)
    
    scrollable_frame = ctk.CTkScrollableFrame(image_window)
    scrollable_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    for image in os.listdir(IMAGE_DIR):
        image_frame = create_styled_frame(scrollable_frame)
        image_frame.pack(fill="x", pady=5, padx=5)
        
        ctk.CTkLabel(image_frame, text=image, text_color=COLORS["on_surface"],
                    font=FONT_NORMAL).pack(side="left", padx=10, pady=5)
        
        def open_image(image_path=os.path.join(IMAGE_DIR, image)):
            try:
                os.startfile(image_path, 'edit')
            except AttributeError:
                import subprocess
                subprocess.run(['open', image_path])
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть изображение: {e}")
        
        create_styled_button(image_frame, text="🎨 Редактировать", width=120, height=30,
                           command=open_image).pack(side="right", padx=10, pady=5)

def update_chat_log(chat_log, key):
#Обновление чата
    messages = read_messages(key)
    
    if len(messages) != len(chat_log.winfo_children()):
        for widget in chat_log.winfo_children():
            widget.destroy()
        
        for msg in messages:
            if ": " in msg:
                parts = msg.split(": ", 1)
                timestamp_user = parts[0]
                message_text = parts[1]
                
                message_frame = ctk.CTkFrame(
                    chat_log,
                    fg_color="#e0daed",
                    border_color="#e0daed",
                    border_width=2,
                    corner_radius=50,
                    height=1,
                    width=1
                )
                message_frame.pack(anchor="w", padx=15, pady=5)
                message_frame.pack_propagate(True)
                
                timestamp_label = ctk.CTkLabel(
                    message_frame,
                    text=timestamp_user,
                    text_color="#4a4458",
                    font=FONT_SMALL,
                    anchor="w"
                )
                timestamp_label.pack(anchor="w", padx=12, pady=(8, 2))
                
                message_label = ctk.CTkLabel(
                    message_frame,
                    text=message_text,
                    text_color="#2d2a35",
                    font=FONT_NORMAL,
                    anchor="w",
                    wraplength=600,
                    justify="left"
                )
                message_label.pack(anchor="w", padx=12, pady=(0, 8))
                
                urls = detect_urls(message_text)
                if urls:
                    for url in urls:
                        url_label = ctk.CTkLabel(
                            message_frame,
                            text=f"🔗 {url}",
                            text_color=COLORS["primary"],
                            font=FONT_NORMAL,
                            anchor="w",
                            cursor="hand2"
                        )
                        url_label.pack(anchor="w", padx=12, pady=(0, 3))
                        
                        def open_url(url_to_open=url):
                            url_to_open = url_to_open if url_to_open.startswith(('http://', 'https://')) else f"http://{url_to_open}"
                            webbrowser.open(url_to_open)
                        
                        url_label.bind("<Button-1>", lambda e, url=url: open_url(url))
        
        chat_log.update_idletasks()
        chat_log._parent_canvas.yview_moveto(1.0)

def clear_messages(chat_log, key):

    if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите очистить всю историю чата?"):
        write_messages([], key)
        for widget in chat_log.winfo_children():
            widget.destroy()

def search_messages_window(key):
#Поиск
    search_window = ctk.CTkToplevel()
    search_window.title("Поиск сообщений")
    search_window.geometry("500x400")
    search_window.configure(fg_color=COLORS["surface"])
    
    ctk.CTkLabel(search_window, text="Введите текст для поиска:", 
                text_color=COLORS["on_surface"], font=FONT_NORMAL).pack(padx=20, pady=5)
    
    search_entry = create_styled_entry(search_window, width=400, placeholder_text="Поиск...")
    search_entry.pack(padx=20, pady=5)
    
    result_text = ctk.CTkTextbox(search_window, width=450, height=200, font=FONT_NORMAL)
    result_text.pack(padx=20, pady=10)
    result_text.configure(state="disabled")
    
    def search_messages():
        term = search_entry.get().lower()
        messages = read_messages(key)
        results = [msg for msg in messages if term in msg.lower()]
        
        result_text.configure(state="normal")
        result_text.delete("1.0", "end")
        result_text.insert("end", "\n".join(results) if results else "Совпадений не найдено.")
        result_text.configure(state="disabled")
    
    create_styled_button(search_window, text="🔍 Поиск", command=search_messages).pack(pady=10)

def edit_message(key):
#Редактирование сообщения
    edit_window = ctk.CTkToplevel()
    edit_window.title("Редактировать сообщение")
    edit_window.geometry("600x400")
    edit_window.configure(fg_color=COLORS["surface"])
    
    messages = read_messages(key)
    if not messages:
        messagebox.showinfo("Редактирование", "Нет сообщений для редактирования.")
        edit_window.destroy()
        return
    
    ctk.CTkLabel(edit_window, text="Выберите сообщение:", 
                text_color=COLORS["on_surface"], font=FONT_NORMAL).pack(padx=20, pady=5)
    
    scrollable_frame = ctk.CTkScrollableFrame(edit_window, height=150)
    scrollable_frame.pack(padx=20, pady=5, fill="both", expand=True)
    
    selected_index = [None]
    
    for i, msg in enumerate(messages):
        msg_frame = create_styled_frame(scrollable_frame)
        msg_frame.pack(fill="x", pady=2, padx=5)
        
        def create_callback(idx=i):
            return lambda: select_message(idx)
        
        create_styled_button(msg_frame, text=f"[{i+1}]", width=40, height=30,
                           command=create_callback()).pack(side="left", padx=5)
        
        ctk.CTkLabel(msg_frame, text=msg, wraplength=400, 
                    text_color=COLORS["on_surface"], font=FONT_NORMAL).pack(side="left", padx=5, fill="x", expand=True)
    
    ctk.CTkLabel(edit_window, text="Новый текст:", 
                text_color=COLORS["on_surface"], font=FONT_NORMAL).pack(padx=20, pady=5)
    
    edit_entry = create_styled_entry(edit_window, width=400)
    edit_entry.pack(padx=20, pady=5)
    
    def select_message(idx):
        selected_index[0] = idx
        edit_entry.delete(0, "end")
        edit_entry.insert(0, messages[idx].split(": ", 1)[1] if ": " in messages[idx] else messages[idx])
    
    def save_edit():
        if selected_index[0] is not None:
            new_text = edit_entry.get()
            if new_text:
                all_messages = read_messages(key)
                timestamp_user = all_messages[selected_index[0]].split(": ", 1)[0]
                all_messages[selected_index[0]] = f"{timestamp_user}: {new_text}"
                write_messages(all_messages, key)
                messagebox.showinfo("Успех", "Сообщение отредактировано.")
                edit_window.destroy()
            else:
                messagebox.showerror("Ошибка", "Введите новый текст.")
        else:
            messagebox.showerror("Ошибка", "Выберите сообщение.")
    
    create_styled_button(edit_window, text="💾 Сохранить", command=save_edit).pack(pady=10)

def show_emoji_panel(entry):
#Панель эмодзи
    emoji_window = ctk.CTkToplevel()
    emoji_window.title("Эмодзи")
    emoji_window.configure(fg_color=COLORS["surface"])
    
    emojis = ["😊", "😀", "😍", "😉", "😐", "😒", "😞", "😢", "😭", "😳",
              "❤️", "👍", "👎", "🔥", "⭐", "🎉", "📷", "🎥", "🔒", "🔍"]
    
    emoji_frame = create_styled_frame(emoji_window)
    emoji_frame.pack(padx=10, pady=10)
    
    for i, emoji in enumerate(emojis):
        btn = create_styled_button(emoji_frame, text=emoji, width=40, height=40,
                                 command=lambda e=emoji: [entry.insert("end", e), emoji_window.destroy()])
        btn.grid(row=i//5, column=i%5, padx=5, pady=5)

def backup_key():
#Резерв ключ
    try:
        if os.path.exists(KEY_FILE):
            backup_file = "Z:\\backup_secret.key"
            shutil.copy2(KEY_FILE, backup_file)
            messagebox.showinfo("Резервное копирование", "Ключ успешно сохранён")
        else:
            messagebox.showerror("Ошибка", "Файл ключа не найден")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось создать резервную копию: {e}")

def import_key():
#Импорт ключа
    key_path = filedialog.askopenfilename(title="Выберите файл ключа", 
                                         filetypes=(("Key Files", "*.key"), ("All Files", "*.*")))
    if not key_path:
        return None
    
    try:
        with open(key_path, "rb") as f:
            key = f.read()
            Fernet(key)
            
        os.makedirs(os.path.dirname(KEY_FILE), exist_ok=True)
        with open(KEY_FILE, "wb") as f:
            f.write(key)
            
        messagebox.showinfo("Импорт ключа", "Ключ успешно импортирован")
        return key
    except Exception as e:
        messagebox.showerror("Ошибка", f"Некорректный ключ: {e}")
        return None

def export_key(key):
    """Экспорт ключа"""
    save_path = filedialog.asksaveasfilename(
        title="Сохранить ключ как",
        defaultextension=".key",
        filetypes=(("Key Files", "*.key"), ("All Files", "*.*"))
    )
    if not save_path:
        return
    
    try:
        with open(save_path, "wb") as f:
            f.write(key)
        messagebox.showinfo("Экспорт ключа", "Ключ успешно экспортирован")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось экспортировать ключ: {e}")

def auto_update_chat(chat_log, key, interval=5000):
    """Автоматическое обновление чата"""
    update_chat_log(chat_log, key)
    chat_log.after(interval, lambda: auto_update_chat(chat_log, key, interval))

def main():

    window = ctk.CTk()
    window.geometry("1000x800")
    window.configure(fg_color=COLORS["background"])
    
    setup_fonts()
    key = load_key()
    
#Название окна

    user = show_login_window()
    window.title(f" K G M  📢 (Зашифровано) - {user}")
    

    main_frame = create_styled_frame(window)
    main_frame.pack(fill="both", expand=True, padx=15, pady=15)
    
# Заголовок с логотипом
    header_frame = ctk.CTkFrame(main_frame, fg_color=COLORS["primary_container"], height=60)
    header_frame.pack(fill="x", pady=(0, 10))
    header_frame.pack_propagate(False)
    
# Логотип
    logo_image = load_logo()
    if logo_image:
        logo_label = ctk.CTkLabel(
            header_frame,
            image=logo_image,
            text=""
        )
        logo_label.pack(side="left", padx=(15, 10), pady=10)
    
# Заголовок 
    title_label = ctk.CTkLabel(
        header_frame,
        text=f"💬 K G M !3  revorked - {user}", 
        text_color=COLORS["on_primary_container"],
        font=FONT_LARGE
    )
    title_label.pack(side="left", padx=(0, 20), pady=10)
    
# Кнопка поиска
    create_styled_button(
        header_frame, 
        text="🔍 Поиск", 
        width=100, 
        height=35,
        command=lambda: search_messages_window(key)
    ).pack(side="right", padx=20, pady=10)
    

    chat_frame = create_styled_frame(main_frame)
    chat_frame.pack(fill="both", expand=True, pady=(0, 10))
    
    chat_log = ctk.CTkScrollableFrame(chat_frame, fg_color=COLORS["surface"])
    chat_log.pack(fill="both", expand=True, padx=5, pady=5)
    
 #Панель ввода
    input_frame = create_styled_frame(main_frame, height=70)
    input_frame.pack(fill="x", pady=(0, 10))
    input_frame.pack_propagate(False)
    
    message_entry = create_styled_entry(input_frame, placeholder_text="Введите сообщение...", height=40)
    message_entry.pack(side="left", fill="x", expand=True, padx=(20, 10), pady=15)
    message_entry.bind("<Return>", lambda event: send_message(user, message_entry, chat_log, key))
    
    create_styled_button(input_frame, text="😊", width=50, height=40,
                       fg_color=COLORS["primary_container"],
                       text_color=COLORS["on_primary_container"],
                       command=lambda: show_emoji_panel(message_entry)).pack(side="left", padx=(0, 10), pady=15)
    
    create_styled_button(input_frame, text="📤 Отправить", width=120, height=40,
                       command=lambda: send_message(user, message_entry, chat_log, key)).pack(side="left", padx=(0, 20), pady=15)
    

    tools_frame = create_styled_frame(main_frame, height=50)
    tools_frame.pack(fill="x")
    tools_frame.pack_propagate(False)
    
# Кнопки действий ( функции )
    tools_data = [
        ("📹 Видео", lambda: send_video(user, chat_log, key)),
        ("🎬 Открыть видео", lambda: open_video(key)),
        ("🖼️ Изображение", lambda: send_image(user, chat_log, key)),
        ("🎨 Редактировать фото", open_image_in_paint),
        ("✏️ Редактировать", lambda: edit_message(key)),
        ("🗑️ Очистить чат", lambda: clear_messages(chat_log, key)),
        ("🔑 Резервная копия", backup_key),
        ("📥 Импорт ключа", lambda: import_key() and update_chat_log(chat_log, key)),
        ("📤 Экспорт ключа", lambda: export_key(key))
    ]
    
    for i, (text, command) in enumerate(tools_data):
        btn = create_styled_button(tools_frame, text=text, command=command, width=110, height=35,
                                 fg_color=COLORS["primary_container"],
                                 text_color=COLORS["on_primary_container"])
        btn.pack(side="left", padx=5, pady=7)
    
    auto_update_chat(chat_log, key)
    window.mainloop()
# Чат разработан коолицией V Two обновление 13 было создано толко ViGer ом 

# Если вы хочете создать свой мессенждер то просим указать V Two coalition

if __name__ == "__main__":
    main()
