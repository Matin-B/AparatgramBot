#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: matin
"""

import requests
import re
from bs4 import BeautifulSoup


def title(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    vidTitle = soup.find(id='videoTitle').text.strip()
    return vidTitle


def Search(searchTitle):
    try:
        baseUrl = 'https://www.aparat.com'
        url = f'https://www.aparat.com/search/{searchTitle}'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.find_all(
                'div',
                {'class': 'thumbnail-video thumbnail-detailside'})
        searchData = dict()
        searchThumb = list()
        searchDuration = list()
        for result in results:
            thumb = result.find('a',
                                {'class': 'thumb thumb-preview'})
            searchThumb.append(thumb['data-poster'])
            duration = result.find('span', {'class': 'duration'}).text
            searchDuration.append(duration)
            resultBox = result.find('a', {'class': 'title'})
            resultTitle = resultBox.text.strip()
            resultLink = baseUrl + resultBox['href']
            searchData[resultTitle] = resultLink
        if len(searchData) != 0:
            return searchData, searchThumb
        else:
            return 'error'
    except Exception:
        return 'error'


def Downloader(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        vidTitle = soup.find(id='videoTitle').text.strip()
        dl_Menu = soup.select('.dropdown, .download-dropdown')[0]
        Links = dl_Menu.find_all('a')

        dlData = dict()
        for link in Links:
            quality = re.findall('[0-9]+', link.get_text().strip())[0] + 'p'
            dlUrl = link['href']
            dlData[quality] = dlUrl

        return vidTitle, dlData
    except Exception:
        return 'error'
