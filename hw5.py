import aiofiles
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import datetime
from multiprocessing.pool import ThreadPool
import os
import re
import requests
import shutil
import urllib
import urllib.request


source_url = 'https://www.python.org/downloads/source/'
N = 20


def get_list_of_links():
    page = requests.get(source_url)
    data = page.text
    soup = BeautifulSoup(data, 'html.parser')
    lst = []
    filename_matcher = re.compile("([^/]*\.tgz$)|([^/][^/]*\.tar\.xz$)")
    attrs = {'href': re.compile("(^https://.*\.tgz)|(^https://.*\.tar\.xz)")}
    for link in soup.findAll('a', attrs=attrs):
        l = link.get('href')
        fn = filename_matcher.search(l).group()
        lst.append((l, fn))
    return lst


links = get_list_of_links()
print("URLs to download: {}".format(len(links)))


# Remove dirs and create new ones
shutil.rmtree('asyncio', ignore_errors=True)
shutil.rmtree('thread_pool', ignore_errors=True)
os.makedirs('asyncio')
os.makedirs('thread_pool')


###########
# asyncio #
###########
def chunk(xs, n):
    '''Split the list, xs, into n chunks'''
    L = len(xs)
    assert 0 < n <= L
    s = L // n
    return [xs[p:p + s] for p in range(0, L, s)]


async def fetch_files(lst):
    async with aiohttp.ClientSession() as session:
        for url_and_filename in lst:
            print("Fetching file: {}".format(url_and_filename[1]))
            async with session.get(url_and_filename[0]) as resp:
                if resp.status == 200:
                    fn = 'asyncio/' + url_and_filename[1]
                    async with aiofiles.open(fn, mode='wb') as f:
                        await f.write(await resp.read())
                        await f.flush()
            print("done:          {}".format(url_and_filename[1]))


t1 = datetime.datetime.now()
loop = asyncio.get_event_loop()
chunks = chunk(links, N)
tasks = []
for ch in chunks:
    print("create a task")
    tasks.append(loop.create_task(fetch_files(ch)))
if not loop.is_running():
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
t2 = datetime.datetime.now()
print("asyncio took time: {}".format(t2 - t1))


###########
# THREADS #
###########
def download_a_file(url_and_filename):
    print("Downloading file: {}".format(url_and_filename[1]))
    fn = 'thread_pool/' + url_and_filename[1]
    urllib.request.urlretrieve(url_and_filename[0], fn)
    print("done:             {}".format(url_and_filename[1]))


pool = ThreadPool(N)
t1 = datetime.datetime.now()
results = pool.map(download_a_file, links)
t2 = datetime.datetime.now()
print("Threads took time: {}".format(t2 - t1))
