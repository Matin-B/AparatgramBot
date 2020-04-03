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
        response = requests.get(url)
        soup = bs4(response.text, 'html.parser')
        playlist_title = soup.find('div', {'class': 'playlist-title'})
        playlist_title = playlist_title.text.strip()
        channel_name = soup.select_one('.details').find('a').text.strip()
        channel_link = soup.select_one('.details').find('a')['href']
        videos = soup.find_all('a', {'class': 'light-80 dark-10'})
        videos_count = len(videos)
        videos_list = list()
        for item in videos:
            link = baseUrl + item['href'].split('?')[0]
            videos_list.append(link)
        return {
                'title': playlist_title,
                'count': videos_count,
                'links': videos_list,
                'channel-name': channel_name,
                'channel-link': channel_link
                }
    except Exception as e:
        return f'Error, {e}'


def download(url):
    try:
        response = requests.get(url)
        soup = bs4(response.text, 'html.parser')
        video_title = soup.find(id='videoTitle').text.strip()
        video_image = soup.find("meta",  property="og:image")['content']
        video_date_created = soup.find(
                "meta", {'name': 'DC.Date.Created'})['content']
        video_count = soup.select_one('.view-count').text.strip()
        video_count = video_count.replace(' بازدید', '')
        video_likes = soup.select_one('#likeVideoButton').text.strip()
        if soup.select_one('.paragraph'):
            video_description = soup.select_one('.paragraph').text.strip()
        else:
            video_description = None
        download_menu = soup.select('.dropdown, .download-dropdown')[0]
        links = download_menu.find_all('a')
        download_links = list()
        for link in links:
            download_link = link['href']
            download_links.append(download_link)
        return {
                'title': video_title,
                'image': video_image,
                'links': download_links,
                'count': video_count,
                'likes': video_likes,
                'date': video_date_created,
                'description': video_description
                }
    except Exception as e:
        return f'Error, {e}'


baseUrl = 'https://www.aparat.com'
