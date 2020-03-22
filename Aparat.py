#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: matin
"""

import requests
import re
from bs4 import BeautifulSoup as bs4


def title(url):
    try:
        r = requests.get(url)
        soup = bs4(r.text, 'html.parser')
        vidTitle = soup.find(id='videoTitle').text.strip()
        return vidTitle
    except Exception as e:
        return f'Error, {e}'


def search(searchTitle):
    try:
        url = f'https://www.aparat.com/search/{searchTitle}'
        r = requests.get(url)
        soup = bs4(r.text, 'html.parser')
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
            resultLink = baseUrl + '/v/' + resultBox['href'].split('/')[-2]
            searchData[resultTitle] = resultLink
        if len(searchData) != 0:
            return searchData, searchThumb, searchDuration
        else:
            return 'error'
    except Exception as e:
        return f'Error, {e}'


def playlist(url):
    try:
        if '/playlist/' in url:
            response = requests.get(url)
            soup = bs4(response.text, 'html.parser')
            playlist_title = soup.find('div', {'class': 'playlist-title'})
            playlist_title = playlist_title.text.strip()
            videos = soup.find_all('a', {'class': 'light-80 dark-10'})
            videos_list = list()
            for item in videos:
                videos_list.append(baseUrl + item['href'])
            return (playlist_title, videos_list)
        else:
            return 'It\'s not playlist !!'
    except Exception as e:
        return f'Error, {e}'


def download(url):
    try:
        response = requests.get(url)
        soup = bs4(response.text, 'html.parser')
        video_title = soup.find(id='videoTitle').text.strip()
        download_menu = soup.select('.dropdown, .download-dropdown')[0]
        links = download_menu.find_all('a')
        download_links = list()
        for link in links:
            download_link = link['href']
            download_links.append(download_link)
        return vidTitle, dlData
    except Exception as e:
        return f'Error, {e}'


baseUrl = 'https://www.aparat.com'
