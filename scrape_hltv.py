import re
from bs4 import BeautifulSoup
import requests
from requests import Session
from urllib.request import Request, urlopen
import cloudscraper
from tqdm import tqdm
import patoolib
import threading
import time
import os

BASE_HLTV_URL = 'https://www.hltv.org'

def __get_hltv_page__(url:str, max_retries:int = 3):
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "windows",
        },
    )
    retries = 0
    while (retries <= max_retries):
        retries += 1
        print(f'try {retries} | SCRAPING: ',url)
        req = scraper.get(url)
        print(req)
        if req.status_code != 200:
            time.sleep(3)
            continue
        return req.content
    return None

def get_matches_from_event(event_id: int):
    url = f'{BASE_HLTV_URL}/results?event={event_id}'
    html = __get_hltv_page__(url)
    soup = BeautifulSoup(html, 'html.parser')

    content = soup.find('div', attrs={'class':'contentCol'})
    match_links = content.find_all('a', href=re.compile(r"^/matches/"))

    results = []
    for link in match_links:
        href = link.get('href')
        results.append(href)
    # print(results)
    return results

def get_demo_links_from_matchpage(match_page: str):
    url = f'{BASE_HLTV_URL}{match_page}'
    html = __get_hltv_page__(url)
    soup = BeautifulSoup(html, 'html.parser')

    content = soup.find('div', attrs={'class':'streams'})
    demo_links = content.find_all('a', href=re.compile(r"^/download/demo"))
    results = []
    for link in demo_links:
        href = link.get('href')
        results.append(href)
    # print(results)
    return results

def download_file(url:str, local_filename:str):
    pass

def download_demo(demo_link: str, force_overwrite: bool=False):
    match_url = f'{BASE_HLTV_URL}{demo_link}'
    '''
        Match demos are redirected links, thus clouscraper assumes it is not protected by Cloudflare 
        and falls back to default implementation.
        However, the redirected page is protected
        Thus, first get the redirection location and then use cloudscraper to scrape
    '''
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "windows",
        },
    )
    r = scraper.get(match_url, allow_redirects=False)
    
    url = r.headers['Location']
    print(url)
    local_filename = 'demos/'+url.split('/')[-1]
    #Check if file already exists to prevent overwriting
    if os.path.isfile(local_filename) and force_overwrite == False:
        print('Downloaded matchfile found! Either force overwrite by setting force_overwrite=True or delete existing file.')
        return local_filename
    #Now download actual file
    with scraper.get(url, stream=True) as r:
        r.raise_for_status()
        pbar = tqdm( unit="bytes", total=int( r.headers['Content-Length'] ) )
        with open(local_filename, 'wb') as f:
            for chunk in tqdm(r.iter_content(chunk_size=8192)): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                pbar.update(len(chunk))
                f.write(chunk)
    return local_filename

def download_match(matchpage_url: str):
    demo_links = get_demo_links_from_matchpage(matchpage_url)
    print(demo_links)
    return download_demo(demo_link=demo_links[0])

def unzip_demo(demofile: str):
    patoolib.extract_archive(demofile, outdir = demofile.split('.')[0])

'''
event_id: event_id of the HLTV event eg: https://www.hltv.org/events/8229/iem-katowice-2025-play-in, 8229 is the event_id
n: number of matches to download, keep at 0 for all matches
'''
def save_event(event_id, n=1):
    matches = get_matches_from_event(event_id=event_id)
    matches = matches[0:(len(matches) if n == 0 else n)] #TODO change from 1 to 0 later 
    for match in matches:
        matchfile = download_match(match)
        unzip_demo(matchfile)

if __name__ == '__main__':
    save_event(8229,5)