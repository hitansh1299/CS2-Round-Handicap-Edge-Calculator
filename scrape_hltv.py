import re
from bs4 import BeautifulSoup
import requests
from requests import Session
from urllib.request import Request, urlopen
import cloudscraper
from tqdm import tqdm

BASE_HLTV_URL = 'https://www.hltv.org'

def __get_hltv_page__(url):
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "windows",
        },
    )
    req = scraper.get(url)
    print('SCRAPING: ',url)
    print(req)
    return req.content

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

def download_demo(demo_link: str):
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

    #Now download actual file
    with scraper.get(url, stream=True) as r:
        r.raise_for_status()
        pbar = tqdm( unit="B", total=int( r.headers['Content-Length'] ) )
        with open(local_filename, 'wb') as f:
            for chunk in tqdm(r.iter_content(chunk_size=8192)): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                pbar.update(len(chunk))
                f.write(chunk)
    return local_filename

def download_match(matchpage_url):
    demo_links = get_demo_links_from_matchpage(matchpage_url)
    print(demo_links)
    return download_demo(demo_link=demo_links[0])
    

if __name__ == '__main__':
    # x = get_demo_from_matchpage('/matches/2378695/pain-vs-astralis-iem-katowice-2025-play-in')
    # x = ['/download/demo/93840']
    # print(x)
    # download_demo(x[0])
    match = get_matches_from_event(8229)[10] #'/matches/2378692/pain-vs-gamerlegion-iem-katowice-2025-play-in'
    download_match(match)
