import time
import sys
import json
from tkinter import colorchooser

import pytesseract
from PIL import ImageGrab, Image
import customtkinter as ctk

from multiran_dict import translate
from selenium_translate import selenium_trans
from languages import langs_multiran, lang_abr, lang_abr_reverso

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

with open('settings.json', encoding='utf-8') as json_file:
    SETTINGS = json.load(json_file)


class ImageTranslator:
    def __init__(self):
        ctk.set_appearance_mode(SETTINGS['Theme'].lower())
        self.root = ctk.CTk()
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.root.bind('<ButtonPress-2>', self.close)

        self.x1 = self.y1 = None
        self.rect = None

        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        
        self.canvas = ctk.CTkCanvas(self.root, bg='black', highlightthickness=0, cursor='cross')
        self.canvas.bind('<ButtonPress-1>', self.press)
        self.canvas.bind('<B1-Motion>', self.drag)
        self.canvas.bind('<ButtonRelease-1>', self.screenshot)
        self.canvas.pack(fill=ctk.BOTH, expand=True)

        self.menu = Menu(self)
        
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
        text = pytesseract.image_to_string(image=image, lang='eng+rus').replace('\n', ' ')
        if SETTINGS['Method'] == 'Reverso scrap(Selenium)':
            sel_trans = selenium_trans(text, src=lang_abr_reverso[SETTINGS['Source language']], target=lang_abr_reverso[SETTINGS['Target language']])
            self.show_trans(text, sel_trans, method='sel')
        else:
            wrd_trans = translate(text, src=langs_multiran[lang_abr[SETTINGS['Source language']]], target=langs_multiran[lang_abr[SETTINGS['Target language']]])
            self.show_trans(text, wrd_trans, method='multiran')
    
    def show_trans(self, src, tran, method):
        if not tran:
            self.create_errorwin(title='Text found error', size='400x200', labels=['Text not recognized', 'Please try highlighting the area again'])
            return
        if method == 'multiran' and len(src.split()) > 1:
                self.create_errorwin(title='Incorrect input for multiran', size='400x200', labels=['Multiran method can handle only single words'\
                                                                                                   , 'If you want to translate bigger text choose  the reverso method'])
                return
        
        trans_window = ctk.CTkToplevel()
        trans_window.title("Translation")
        trans_window.geometry("520x250")
        
        ctk.CTkLabel(trans_window, text="Оригинал:").pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(trans_window, text=src, wraplength=380).pack(anchor="w", padx=10)
        ctk.CTkLabel(trans_window, text="Перевод:").pack(anchor="w", padx=10, pady=5)

        if method == 'sel':
            translated_text = tran
            scrollable_frame = ctk.CTkScrollableFrame(trans_window, width=480, height=300)
            scrollable_frame.pack(padx=5, pady=5, fill="both", expand=True)
            block = ctk.CTkFrame(scrollable_frame, corner_radius=10)
            block.pack(padx=10, pady=5, fill="x")
            content = ctk.CTkLabel(block, text=translated_text, wraplength=450, justify="left", anchor="w")
            content.pack(fill="x", padx=10, pady=(0, 5))
        else:
            translated_text = tran
            self.blockify_labels(translated_text, trans_window)

        trans_window.protocol("WM_DELETE_WINDOW", self.close)

    def create_errorwin(self, title: str, size: str, labels: list[str]):
        window = ctk.CTkToplevel()
        window.geometry(size)
        window.title(title)

        for label in labels:
            ctk.CTkLabel(window, text=label).pack(anchor="w", padx=10, pady=5)
        
        window.protocol("WM_DELETE_WINDOW", self.close)

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
        self.settings_window.geometry("400x300")
        self.settings_window.title("Settings")
        self.settings_window.attributes('-topmost', True)
        self.settings_window.grab_set()

        self.create_labels('Theme', 'Highlighting color', 'Hot key', "Tranlation's method", 'Source language', 'Target language')

        self.create_options(
            theme = [ctk.StringVar(value=SETTINGS['Theme']), ["Dark", "Light"], lambda x: self.update_setting('Theme', x, theme=True)],
            highlight = [ctk.StringVar(value=SETTINGS['Highlighting color']), 'ht', lambda x: self.update_setting('Highlighting color', x)],
            key = [ctk.StringVar(value=SETTINGS['Hot key']), ['ctrl+alt+t', 'ctrl+u', 't', 'ctrl+shift+w', 'ctrl+alt+a'], lambda x: self.update_setting('Hot key', x)],
            method = [ctk.StringVar(value=SETTINGS["Method"]), ['Multiran scrap', 'Reverso scrap(Selenium)'], lambda x: self.update_setting('Method', x)],
            srclang = [ctk.StringVar(value=SETTINGS['Source language']), list(lang_abr.keys()), lambda x: self.update_setting('Source language', x)],
            target = [ctk.StringVar(value=SETTINGS['Target language']), list(lang_abr.keys()), lambda x: self.update_setting('Target language', x)]
        )

    def create_labels(self, *labels):
        for ind, label in enumerate(labels):
            ctk.CTkLabel(self.settings_window, text=label).grid(row=ind, column=0, padx=10, pady=10)

    def create_options(self, **stats):
        for ind, stat in enumerate(stats):
            if stats[stat][1] == 'ht':
                self.highlight_choice = ctk.CTkButton(self.settings_window, text='', fg_color=SETTINGS['Highlighting color'], command=self.update_highlighting)
                self.highlight_choice.grid(row=1, column=1, padx=10, pady=10)
            else:
                choice = ctk.CTkOptionMenu(self.settings_window, variable=stats[stat][0], values=stats[stat][1], command=stats[stat][2])
                choice.grid(row=ind, column=1, padx=10, pady=10)
    
    def update_highlighting(self):
        chosen_color = colorchooser.askcolor(title='Choose highlighting color')[1]
        if chosen_color is None:
            return
        SETTINGS['Highlighting color'] = chosen_color
        with open('settings.json', 'w', encoding='utf-8') as json_file:
            json.dump(SETTINGS, json_file, indent=4)
        self.highlight_choice.configure(fg_color=chosen_color)
    
    def update_setting(self, setting_option, selected, theme=False):
        SETTINGS[setting_option] = selected
        with open('settings.json', 'w', encoding='utf-8') as json_file:
            json.dump(SETTINGS, json_file, indent=4)
        if theme:
            ctk.set_appearance_mode(selected.lower())
    

class Menu:
    def __init__(self, parent):
        self.parent = parent

        self.menu_window = ctk.CTkToplevel()
        x = (self.parent.screen_width - 112) // 2
        self.menu_window.geometry(f"112x45+{x}+0")
        self.menu_window.overrideredirect(True)
        self.menu_window.attributes("-topmost", True)
        self.menu_window.focus_force()

        self.menu_frame = ctk.CTkFrame(self.menu_window, width=200, height=50, 
                                     fg_color="gray20", bg_color='black')
        self.menu_frame.pack(fill=ctk.BOTH, expand=True)

        original_setimage = Image.open('imgs/settings_img.png')
        self.settings_image = ctk.CTkImage(light_image=original_setimage, dark_image=original_setimage, size=(30, 30))
        self.settings_button = ctk.CTkButton(
            self.menu_frame, command=self.open_settings, fg_color="transparent", width=30, height=30, image=self.settings_image, text=''
        )
        self.settings_button.pack(side="left", padx=5, pady=5)

        self.close_button = ctk.CTkButton(self.menu_frame, command=self.close, text='Close', width=30, height=30)
        self.close_button.pack(side="left", padx=5, pady=5)

        self.parent.root.grab_set()

    def open_settings(self):
        Settings(self)

    def close(self):
        self.menu_window.destroy()
        sys.exit(0)


if __name__ == '__main__':
    ImageTranslator()
