# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 11:35:31 2020

@author: Saddam
"""

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import os
from time import sleep

#import re
def make_url(name):
    URL = "https://yts.mx/"
    search_query = "browse-movies/"
    movie_name = name
    #section_movie = '&section=movie'
    other_option=""
    final_url = URL + search_query + str(movie_name)
    return final_url
def get_page(url):
    hdr={'User-Agent': 'Mozilla/5.0'} #solve http 403
    page=requests.get(url,headers=hdr)
    soup = BeautifulSoup(page.content,'html.parser')
    return page,soup
#p,s=get_page(final_url)

def get_movies_names(name):
    result_dict=dict()
    page,soup = get_page(make_url(name))
#    pds=pd.read_html(page.content)
    query_results = soup.find_all("div",class_="browse-movie-wrap col-xs-10 col-sm-4 col-md-5 col-lg-4")
#    print(query_results)
    for entity in query_results:
        entity1=entity.find("div",class_="browse-movie-bottom").a
        result_dict[entity1.string]=entity1['href']
    return result_dict


def get_donwload_url(url):
    options1 = webdriver.ChromeOptions()
    options1.add_argument('--ignore-certificate-errors')
    options1.add_argument('--disable-gpu')
    options1.add_argument('--incognito')
    options1.add_argument('--headless')
    DRIVER = webdriver.Chrome(options=options1)
    DRIVER.get(url)
    link_text=DRIVER.find_elements_by_link_text("Download")
    print(link_text)
    if len(link_text)>0:
        link_text[0].click()
    tabs = DRIVER.window_handles
    DRIVER.switch_to.window(tabs[0])
    print('(X]Current url ----->', DRIVER.current_url)
    #DRIVER.switch_to.window(DRIVER.window_handles[0])
    page_source = DRIVER.page_source
    DRIVER.quit()
    soup=BeautifulSoup(page_source,'html.parser')
    div=soup.find_all('div',class_="modal-torrent")
    return {' '.join(item.text.strip().split('\n')[:-2]):[a['href'] for a in item.find_all("a")] for item in div}

#with default torrent client
def donwload_magnet(magnet):
    return os.startfile(magnet)

def main():
    name=str(input("search a movie\t"))
    result_dict=get_movies_names(name)
    name_list=list(result_dict.keys())
    href_list=list(result_dict.values())
    for i,title in enumerate(name_list):
        if title != None:
            print('{:4} {:50}'.format(i,title))
    index=int(input('choose a number to fetch download links'))
    href=href_list[index]
    print(name_list[index],href)
    q=str(input('press y to download\t'))
    if q=='y':
        qualities_dict=get_donwload_url(href)
        for i,qu in enumerate(list(qualities_dict.keys())):
            print('{:4} {:50}'.format(i,qu))
        indexx=int(input('choose a quality'))
        magnet=list(qualities_dict.values())[indexx][1]
        print(magnet)
        donwload_magnet(magnet)

if __name__=='__main__':
    main()