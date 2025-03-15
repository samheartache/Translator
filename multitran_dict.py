from collections import defaultdict
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from curls.multitran_curl import cookies, headers

def translate(word: str, src, target) -> str:
    params = {
        's': word,
        'l1': src,
        'l2': target,
    }

    response = requests.get('https://www.multitran.com/m.exe', params=params, cookies=cookies, headers=headers)

    bs = BeautifulSoup(response.text, 'lxml')
    grouped_translations = defaultdict(list)
    
    for row in bs.find_all('tr'):
        tds = row.find_all('td')
        if len(tds) >= 2:
            a_tag = tds[0].find('a')
            trans = tds[1].text.strip()
            if a_tag and a_tag.has_attr('title'):
                subj = a_tag['title']
                grouped_translations[subj].append(trans)

    res = '\n\n'.join([f'{subj}: {", ".join(translations)}' for subj, translations in grouped_translations.items()])
    res = [[subj, ', '.join(translations)] for subj, translations in grouped_translations.items()]

    return res
