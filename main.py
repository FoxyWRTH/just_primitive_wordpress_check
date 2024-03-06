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

url = 'https://blog.mozilla.org/en/'


def wordpress_or_not(target_url):
    response = requests.get(target_url)
    what_we_find = 'WordPress|wp|wp-content'
    signals_meta = []
    signals_link = []

    if response == 200 or 403:
        soup = BeautifulSoup(response.text, 'lxml')

        signals_meta = soup.find_all('meta', content=re.compile(what_we_find))
        signals_link = soup.find_all('link', href=re.compile(what_we_find))
    else:
        print(f'Bad request: {response}')
    if signals_link or signals_meta:
        return f'Yep, it uses WordPress'
    else:
        return f'Hmm, no, there are no traces specific to WordPress found here.'


if __name__ == '__main__':
    print(wordpress_or_not(url))
