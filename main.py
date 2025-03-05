import time
import sys
import threading
import json
from tkinter import colorchooser

import pytesseract
from PIL import ImageGrab, Image, ImageTk
import customtkinter as ctk
from deep_translator import MyMemoryTranslator

from multiran_dict import translate

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
CURRENT_THREAD = None

with open('settings.json', encoding='utf-8') as json_file:
    SETTINGS = json.load(json_file)


class ImageTranslator:
    def __init__(self):
        ctk.set_appearance_mode(SETTINGS['Theme current'].lower())
        self.root = ctk.CTk()
        
        self.x1 = self.y1 = None
        self.rect = None

        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', True)
        
        self.canvas = ctk.CTkCanvas(self.root, bg='black', highlightthickness=0, cursor='cross')
        self.canvas.bind('<ButtonPress-1>', self.press)
        self.canvas.bind('<B1-Motion>', self.drag)
        self.canvas.bind('<ButtonRelease-1>', self.screenshot)
        self.canvas.pack(fill=ctk.BOTH, expand=True)

        original_image = Image.open('imgs/settings_img.png')
        self.settings_image = ctk.CTkImage(light_image=original_image, dark_image=original_image, size=(50, 50))

        self.settings_button = ctk.CTkButton(
            self.root, command=self.open_settings, fg_color="transparent", width=50, height=50, image=self.settings_image, text='Settings'
        )
        self.canvas.create_window(50, 50, window=self.settings_button, anchor="nw")
        
        self.root.mainloop()
    
    def press(self, event):
        self.x1, self.y1 = event.x, event.y
        self.rect = self.canvas.create_rectangle(self.x1, self.y1, event.x, event.y, outline=SETTINGS['Highlighting color'], width=3)
    
    def drag(self, event):
        self.canvas.coords(self.rect, self.x1, self.y1, event.x, event.y)
    
    def screenshot(self, event):
        self.root.withdraw()
        time.sleep(0.4)
        x1, y1 = min(self.x1, event.x), min(self.y1, event.y)
        x2, y2 = max(self.x1, event.x), max(self.y1, event.y)
        image = ImageGrab.grab(bbox=(x1, y1, x2, y2))
        self.translate_image(image)
    
    def translate_image(self, image):
        text = pytesseract.image_to_string(image=image, lang=SETTINGS['Source language'])
        if len(text.split()) > 1:
            translator = MyMemoryTranslator(source='english', target='russian')
            translated = translator.translate(text, return_all=True)
            self.show_trans(text, translated)
        else:
            wrd_trans = translate(text)
            self.show_trans(text, wrd_trans, long=False)
    
    def show_trans(self, src, tran, long=True):
        if not tran:
            self.create_win(title='Text found error', size='400x200', labels=['Text not recognized', 'Please try highlighting the area again'])
            return
        
        trans_window = ctk.CTkToplevel()
        trans_window.title("Translation")
        trans_window.geometry("500x250")
        
        ctk.CTkLabel(trans_window, text="Оригинал:").pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(trans_window, text=src, wraplength=380).pack(anchor="w", padx=10)
        ctk.CTkLabel(trans_window, text="Перевод:").pack(anchor="w", padx=10, pady=5)
        
        if long:
            best = tran[0]
            res = {best}
            for i in tran:
                if isinstance(i, dict):
                    res.add(i['translation'])
            
            translated_text = ','.join(res)
        else:
            translated_text = tran
            self.blockify_labels(translated_text, trans_window)

        trans_window.protocol("WM_DELETE_WINDOW", self.close)
    
    def create_win(self, title: str, size: str, labels: list[str]):
        window = ctk.CTkToplevel()
        window.geometry(size)
        window.title(title)

        for label in labels:
            ctk.CTkLabel(window, text=label).pack(anchor="w", padx=10, pady=5)

    def open_settings(self):
        Settings(self)
    
    def blockify_labels(self, blocks: list[str], root):
        scrollable_frame = ctk.CTkScrollableFrame(root, width=480, height=300)
        scrollable_frame.pack(padx=5, pady=5, fill="both", expand=True)
        for b in blocks:
            block = ctk.CTkFrame(scrollable_frame, corner_radius=10)
            block.pack(padx=10, pady=5, fill="x")

            headline = ctk.CTkLabel(block, text=b[0], font=("Arial", 12, "bold"), justify="left", anchor="w")
            headline.pack(fill="x", padx=10, pady=(5, 2))

            content = ctk.CTkLabel(block, text=b[1], wraplength=450, justify="left", anchor="w")
            content.pack(fill="x", padx=10, pady=(0, 5))

    def close(self):
        self.root.quit()
        self.root.destroy()
        sys.exit(0)


class Settings:
    def __init__(self, parent):
        self.parent = parent
        
        self.settings_window = ctk.CTkToplevel()
        self.settings_window.geometry("400x200")
        self.settings_window.title("Settings")
        self.settings_window.attributes('-topmost', True)
        self.settings_window.grab_set()
        
        theme_var = ctk.StringVar(value=SETTINGS['Theme current'])
        themes = ["Dark", "Light"]
        theme_choice = ctk.CTkOptionMenu(self.settings_window, variable=theme_var, values=themes, command=self.update_theme)
        theme_choice.grid(row=0, column=1, padx=10, pady=10)

        self.highlight_choice = ctk.CTkButton(self.settings_window, text='', fg_color=SETTINGS['Highlighting color'], command=self.update_highlighting)
        self.highlight_choice.grid(row=1, column=1, padx=10, pady=10)

        self.create_labels('Theme', 'Highlighting color', 'Source language')

        
    def create_labels(self, *labels):
        for ind, label in enumerate(labels):
            ctk.CTkLabel(self.settings_window, text=label).grid(row=ind, column=0, padx=10, pady=10)
    
    def update_theme(self, selected_theme):
        SETTINGS['Theme current'] = selected_theme
        with open('settings.json', 'w', encoding='utf-8') as json_file:
            json.dump(SETTINGS, json_file, indent=4)
        ctk.set_appearance_mode(selected_theme.lower())
    
    def update_highlighting(self):
        chosen_color = colorchooser.askcolor(title='Choose highlighting color')[1]
        SETTINGS['Highlighting color'] = chosen_color
        with open('settings.json', 'w', encoding='utf-8') as json_file:
            json.dump(SETTINGS, json_file, indent=4)
        self.highlight_choice.configure(fg_color=chosen_color)


if __name__ == '__main__':
    ImageTranslator()
