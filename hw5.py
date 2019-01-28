import aiohttp
import asyncio
import aiofiles
import re
import datetime
import threading
from multiprocessing.pool import ThreadPool
import urllib.request
import urllib
from bs4 import BeautifulSoup
import requests


source_url = 'https://www.python.org/downloads/source/'


def get_list_of_links():
    page = requests.get(source_url)
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    lst = []
    filename_matcher = re.compile("([^/]*\.tgz$)|([^/][^/]*\.tar\.xz$)")
    for link in soup.findAll('a', attrs={'href': re.compile("(^https://.*\.tgz)|(^https://.*\.tar\.xz)")}):
        l = link.get('href')
        fn = filename_matcher.search(l).group()
        lst.append((l, fn))
    return lst


links = get_list_of_links()
print("URLs to download: {}".format(len(links)))



###########
# asyncio #
###########
async def fetch_files(lst):
    async with aiohttp.ClientSession() as session:
        for url_and_filename in lst:
            print("Fetching file: {}".format(url_and_filename[1]))
            async with session.get(url_and_filename[0]) as resp:
                if resp.status == 200:
                    async with aiofiles.open('asyncio/' + url_and_filename[1], mode='wb') as f:
                        await f.write(await resp.read())
                        await f.flush()
            print("done:          {}".format(url_and_filename[1]))


t1 = datetime.datetime.now()
loop = asyncio.get_event_loop()
loop.run_until_complete(fetch_files(links))
t2 = datetime.datetime.now()
print("asyncio took time: {}".format(t2 - t1))




###########
# THREADS #
###########
def download_a_file(url_and_filename):
    print("Downloading file: {}".format(url_and_filename[1]))
    urllib.request.urlretrieve(url_and_filename[0], 'thread_pool/' + url_and_filename[1])


pool = ThreadPool(20)
t1 = datetime.datetime.now()
results = pool.map(download_a_file, links)
t2 = datetime.datetime.now()
print("Threads took time: {}".format(t2 - t1))