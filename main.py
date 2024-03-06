"""
На любом языке программирования (даже на псевдокоде) напишите программу, которая будет получать от
пользователя url и возвращать, реализован ли сайт с помощью wordpress или нет.

Кратко (в 2-3 абзаца, не больше) опишите, как её нужно было бы расширить и/или какие дополнительные
инструменты использовать, чтобы обеспечить проверку написанным кодом насколько получится большего
числа сайтов во всей сети интернет. Расширенная программа/связка программ должна была бы
возвращать процент сайтов в интернет, написанных на Wordpress.
-------------------------------------------------------------------------------------------------
Не на всех сайтах о которых пишут, мол, сделаны на WordPress есть характерные теги или директории
отличающие их от других.
"""

import re
import requests
from bs4 import BeautifulSoup

url_list = ['https://www.bloomberg.com/europe', 'https://vimeo.com/',
            'https://www.surveymonkey.com/', 'https://www.spotify.com/us/',
            'https://www.kaspersky.de/', 'https://www.mcafee.com/',
            'https://www.salesforce.com/de/?ir=1', 'https://www.nytimes.com/',
            'https://raue.com/en/', 'https://www.obama.org/', 'https://www.sonymusic.com/',
            'https://www.wfw.com/']


def wordpress_or_not(target_url, details=False):
    response = requests.get(target_url)
    what_we_find = 'WordPress|wp|wp-content'
    common_dirs = ["wp-admin", "wp-content", "wp-includes"]
    signals_meta = []
    signals_link = []
    signals_dir = []

    if response.status_code == 200 or 403:
        soup = BeautifulSoup(response.text, 'lxml')

        signals_meta = soup.find_all('meta', content=re.compile(what_we_find))
        signals_link = soup.find_all('link', href=re.compile(what_we_find))

        for dirs in common_dirs:
            response = requests.get(f'{target_url}/{dirs}')
            if response.status_code == 200:
                signals_dir.append(f'{target_url}/{dirs}')
    else:
        print(f'Bad request: {response}')
    if details:
        print(f'Meta tags: \n{signals_meta}\n\n'
              f'Links: \n{signals_link}\n\n'
              f'Dirs \n{signals_dir}\n\n')
    if signals_link or signals_meta or signals_dir:
        return f'Yep, it uses WordPress'
    else:
        return f'Hmm, no, there are no traces specific to WordPress found here.'


if __name__ == '__main__':
    for i in url_list:
        print(f'Сайт: {i}, результат:\n {wordpress_or_not(i, details=True)}')
