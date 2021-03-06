#!/usr/bin/python3

from html import unescape
import re
import random
import json
import requests
from bs4 import BeautifulSoup

PATTERN = re.compile(r'/video(\d+)/.*')

def _fetch_page(page_number):
    url = 'https://www.xvideos.com/porn/portugues/' + str(page_number)
    res = requests.get(url)

    if res.status_code != 200:
        raise Exception('Response Error: ' + str(res.status_code))

    return BeautifulSoup(res.text, 'html.parser')

def _find_videos(soup):
    for element in soup.select('.thumb-block > p > a'):
        try:
            reference = PATTERN.match(element['href']).group(1)
        except AttributeError:
            pass

        yield element['title'], reference

def _get_comments(video_ref):
    url_mask = 'https://www.xvideos.com/video-get-comments/{0}/0/'
    url = url_mask.format(video_ref)
    res = requests.post(url)

    if res.status_code != 200:
        raise Exception('Response Error: ' + str(res.status_code))

    for item in json.loads(res.text)['comments']:
        content = unescape(item['c']).replace('<br />', '\n')
        author = unescape(item['n'])

        if '<a href=' not in content:
            yield author, content

def choose_random_porn_comment():
    for _ in range(10):
        page = _fetch_page(random.randint(1, 40))
        videos = _find_videos(page)
        title, reference = random.choice(list(videos))
        comments = _get_comments(reference)

        try:
            author, content = random.choice(list(comments))
        except IndexError:
            continue

        return author, content, title

    raise Exception('Too hard')

def main():
    comment = choose_random_porn_comment()

    print(*comment, sep='\n')

if __name__ == '__main__':
    main()

