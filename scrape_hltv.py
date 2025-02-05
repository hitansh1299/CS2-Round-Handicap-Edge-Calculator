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
import logging
import logging_utils

BASE_HLTV_URL = 'https://www.hltv.org'
MAX_RETRIES = 5
logger = logging.getLogger(__name__)
class MaxRetriesReachedException(Exception):
    pass

class DemoFileNotFoundException(Exception):
    pass

def __get_hltv_page__(url:str):
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "windows",
        },
    )
    retries = 0
    sleeptime = 2
    while True:
        retries += 1
        logger.info(f"Attempt {retries} to scrape URL: {url}")
        req = scraper.get(url)
        logger.debug(f"Received status code: {req.status_code}")
        if req.status_code != 200:
            if retries > MAX_RETRIES:
                break
    
            time.sleep(sleeptime)
            sleeptime *= sleeptime
            continue
        sleeptime = 2
        return req.content

    #Finally if you cannot return raise an exception
    logger.error("Reached the maximum retries but still producing errors. Please check logs for more information.")
    raise MaxRetriesReachedException('Reached the maximum retries but still producing errors, please check logs for more info')



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
    logger.info(f"Found {len(results)} matches in event {event_id}")
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
    logger.info(f"Found {len(results)} demo link(s) on match page {match_page}")
    return results

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
        logger.warning('Downloaded matchfile found! Either force overwrite by setting force_overwrite=True or delete existing file.')
        return local_filename
    
    #Now download actual file

    retries = 0
    sleeptime = 2
    while (retries <= MAX_RETRIES):
        retries += 1
        logger.info(f"Attempt {retries} to download demo: {url}")
        with scraper.get(url, stream=True) as r:
            logger.debug(f"Received status code: {r.status_code}")
            if r.status_code != 200:
                time.sleep(sleeptime)
                sleeptime *= sleeptime
                continue
            # r.raise_for_status()
            pbar = tqdm(unit="bytes", total=int( r.headers['Content-Length']))
            logger.info(f"Downloading demo to {local_filename}")
            with open(local_filename, 'wb') as f:
                for chunk in tqdm(r.iter_content(chunk_size=8192)): 
                    # If you have chunk encoded response uncomment if
                    # and set chunk_size parameter to None.
                    #if chunk: 
                    pbar.update(len(chunk))
                    f.write(chunk)

    logger.info(f"Demo downloaded successfully: {local_filename}")
    return local_filename

def download_match(matchpage_url: str):
    demo_links = get_demo_links_from_matchpage(matchpage_url)
    if not demo_links:
        logger.error(f"No demo links found for match page {matchpage_url}")
        return None
    print(demo_links)
    return download_demo(demo_link=demo_links[0])

def unzip_demo(demofile: str, force_overwrite: bool=False):
    if not demofile:
        raise DemoFileNotFoundException('Demo File not found. Please check logs for more information')
    
    if os.path.isdir(demofile.rsplit('.',1)[0]) and force_overwrite == False:
        logger.warning('Unzipped Directory already Exists! Either force overwrite by setting force_overwrite=True or delete existing file.')
        return
    

    logger.info(f"Unzipping demo file: {demofile}")
    patoolib.extract_archive(demofile, outdir = demofile.rsplit('.',1)[0])
    logger.info(f"Unzipped demo file to {demofile.rsplit('.', 1)[0]}")

'''
event_id: event_id of the HLTV event eg: https://www.hltv.org/events/8229/iem-katowice-2025-play-in, 8229 is the event_id
n: number of matches to download, keep at 0 for all matches
'''
def save_event(event_id, n=1):
    matches = get_matches_from_event(event_id=event_id)
    matches = matches[0:(len(matches) if n == 0 else n)] #TODO change from 1 to 0 later 
    logger.info(f"Processing {len(matches)} match(es) for event {event_id}")
    for match in matches:
        matchfile = download_match(match)
        unzip_demo(matchfile)

if __name__ == '__main__':
    save_event(8229,0)
    # __get_hltv_page__("https://www.hltv.org/events/8229/iem-katowice-2025-play-in")