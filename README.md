# Translator

**Translator** is a tool for translating text from images, as well as translating individual words and texts from various languages. It uses the [Tesseract](https://github.com/tesseract-ocr/tesseract) library for text extraction from images and scraping of Multitran and Reverso websites for translation. For user convenience, hotkeys and customizable settings are provided.

## Features

- **Text translation from images**: Use screen area selection to capture text from an image and translate it.
  
- **Two different methods for translation**:
  
  - **Single-word translation**: Scraping the Multitran website for translating individual words. It provides a wide diversity of translations for one word. In addition, translations are divided into categoties.
  
  - **Reverso dynamic scrape**: Scraping the Reverso website using Selenium for translating single words and even large texts (in the current version, it is recommended to use Multitran for single-word translation, for Selenium is pretty slow even for single words).
  
- **Hotkeys**: Launch the application and terminate it using customizable hotkeys.
  
- **Settings**: Ability to choose the theme, translation language, translation method, highlighting color and hotkeys.

## Installation

1. **Install Tesseract**:
   
   - Download and install Tesseract OCR from the [official repository](https://github.com/tesseract-ocr/tesseract).
  
   - Add Tesseract run file to the environment variables with the name **TESS**.

2. **Install dependencies**:

   - Ensure you have Python 3.8 or higher installed.
  
   - Install the required dependencies to your virtual environment using pip:
     ```bash
     pip install -r requirements.txt
     ```

3. **Download Tesseract language data**:

   - Ensure you have the necessary language data for Tesseract installed (e.g., `eng`, `rus`, and others you plan to use).
  
   - You can see your downloaded language data using the command:
     ```bash
     tesseract --list-langs
     ```

## Usage

1. **Launching the application**:

   - To run the application in the background, use the `runner.py` file. It will wait for a hotkey press (default: `Ctrl+Alt+A`), after which it will launch the main `main.py` file.
     ```bash
     python runner.py
     ```

   - After launching the application, select an area on the screen to capture text from the image.

2. **Using the application**:
   
   - After launching the application, a menu will appear at the top of the screen, where you can either open the settings or launch the default Translation tool for manual text input.
  
   - Also you can select the area of the screen right after the app starts, the text will be automatically extracted and translated according to the selected settings.
  
   - **NOTE**: For single-word translation, Multitran is used; for texts, Reverso is used.

## Settings (settings.json)

- **Highlight color**: Highlight color for the screen area (default: `red`).
  
- **Theme**: Interface theme  (default: `Dark`).
  
- **Source language**: Source language for translation (default: `Russian`).
  
- **Target language**: Target language for translation (default: `English`).
  
- **Start hot key**: Hotkey for launching the application (default: `Ctrl+Alt+A`).
  
- **Exit hot key**: Hotkey for terminating the application (default: `Alt+E`).
  
- **Method**: Translation method (`Multitran scrape` or `Reverso scrape(Selenium)`).
  

## Project Structure

- **main.py**: The main application file containing the logic for the interface and translation.
  
- **runner.py**: File to run the application in background and then launch it using hotkeys.
  
- **settings.json**: Application settings file.
  
- **multitran_dict.py**: Module for scraping the Multitran website.
  
- **selenium_translate.py**: Module for scraping the Reverso website using Selenium.
  
- **languages.py**: file with data on supported languages.
  
- **error_handle.py**: file for all error messages and titles.

## Known Dismerits

- **Dynamic scraping of Reverso**: The current implementation of Reverso scraping using Selenium is inefficient, because the translation lasts too long even for single words. It is recommended to use Multitran for single-word translation.
  
- **Tesseract language support**: Ensure that the required language data for Tesseract is installed. If a language is missing, the application may fail to extract text correctly.