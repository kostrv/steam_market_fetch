from multiprocessing import Pool
from bs4 import BeautifulSoup
import asyncio
import aiohttp


proxies = []
for i in range(19000, 19999):
    proxy_data = {
        'user' : 'Lolobroller_17712',
        'pass' : 'yc44zbOJP8',
        'host' : 'ipv4.reproxy.network',
        'port' : i
    }
    proxies.append(proxy_data)


def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    title = soup.title.string if soup.title else 'No title found'
    return str(title)


async def fetch(session, url, proxy):
    async with session.get(url, proxy=proxy) as response:
        return await response.text()


async def fetch_with_proxy(proxy, url):
    proxy_url = f'http://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}'
    
    async with aiohttp.ClientSession() as session:
        html_content = await fetch(session, url, proxy=proxy_url)
        return parse_html(html_content=html_content)


def run_fetch(proxy : dict, url : str):
    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(fetch_with_proxy(proxy, url))
    return res


if __name__ == '__main__':
    url = 'https://store.steampowered.com/'
    
    sessions_count = 10
    with Pool(processes=sessions_count) as pool:
        results = pool.starmap(func=run_fetch, 
                                iterable=[(proxies[i], url) for i in range(sessions_count)])
    
    for result in results:
        print(result)