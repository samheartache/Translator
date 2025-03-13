from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By

from urllib.parse import quote
import time


def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def selenium_trans(text: str, src: str, target: str):
    driver = initialize_driver()
    encoded = quote(text)
    driver.get(f'https://www.reverso.net/перевод-текста#sl={src}&tl={target}&text={encoded}')
    time.sleep(5)
    res = ''
    try:
        # Find a single word
        res = driver.find_element(By.CLASS_NAME, 'text__translation').text
    except:
        try:
            # Find average amount of text
            res = driver.find_element(By.CLASS_NAME, 'sentence-wrapper_without-hover').text
        except:
            try:
                # Find huge amount of text
                spans = driver.find_elements(By.XPATH, "//div[contains(@class, 'sentence-wrapper_target')]//span[@data-index]")
                res = ''.join([span.text for span in spans])
            except:
                res = 'Unable to get the translation'
    return res
