from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from pprint import pprint

from curls.multiran_curl import cookies, headers

def translate(word: str) -> str:
    params = {
        's': word,
        'l1': '1',
        'l2': '2',
    }

    response = requests.get('https://www.multitran.com/m.exe', params=params, cookies=cookies, headers=headers)
    bs = BeautifulSoup(response.text, 'lxml')

    try:
        all_trans = [i.text for i in bs.find_all('td', class_='trans')]
        subjects = [a.find('a')['title'] for a in bs.find_all('td', class_='subj')]
        grouped_translations = defaultdict(list)
    except TypeError:
        print('Ошибка')
        return

    for trans, subj in zip(all_trans, subjects):
        grouped_translations[subj].append(trans)

    res = '\n\n'.join([f'{subj}: {", ".join(translations)}' for subj, translations in grouped_translations.items()])
    res = [[subj, ', '.join(translations)] for subj, translations in grouped_translations.items()]

    return res
