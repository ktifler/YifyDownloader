# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 11:35:31 2020

@author: ktifler
"""

from bs4 import BeautifulSoup
from art import tprint
import requests
import os


def make_url(name):
    URL = "https://yts.mx/"
    search_query = "browse-movies/"
    movie_name = name
    #section_movie = '&section=movie'
    other_option = ""
    final_url = URL + search_query + str(movie_name)
    return final_url


def get_page(url):
    hdr = {'User-Agent': 'Mozilla/5.0'}  # solve http 403
    page, soup = None, None
    try:
        page = requests.get(url, headers=hdr)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
        else:
            raise('Unable to process web page')
    except Exception as e:
        print(f'Unable to access {url}\nError: {e}')
    return page, soup


def get_movies_names(name):
    _, soup = get_page(make_url(name))
    result_links = soup.find_all(
        "a", class_="browse-movie-title")
    return {movie_div.text: movie_div['href'] for movie_div in result_links}


def get_donwload_url(url):
    _, soup = get_page(url)
    p = soup.select_one('#movie-info > p')
    return {a.text: a['href'] for a in p.find_all("a")}

# with default torrent client


def donwload_magnet(magnet):
    return os.startfile(magnet)


def main():
    tprint('YIFY Downloader')
    name = str(input("search a movie\t"))
    result_dict = get_movies_names(name)
    names_list = list(result_dict.keys())
    links_list = list(result_dict.values())
    for i, title in enumerate(names_list):
        if title != None:
            print('{:4} {:50}'.format(i, title))

    choice = int(input('choose a number to fetch download links'))
    href = links_list[choice]
    print(names_list[choice], href)
    validate_download = str(input('press y to download\t'))
    if validate_download == 'y':
        qualities_dict = get_donwload_url(href)
        for i, quality in enumerate(list(qualities_dict.keys())):
            print('{:4} {:50}'.format(i, quality))
        quality_choice = int(input('choose a quality'))
        magnet_link = list(qualities_dict.values())[quality_choice]
        print(f'Torrent link{magnet_link}')
        print('If you have installed a torrent client, a download prompt will appear')
        donwload_magnet(magnet_link)


if __name__ == '__main__':
    main()
