from datetime import datetime, timedelta
from db import create_pool, save_to_db
from data import items_links, proxies
from collections import defaultdict
from bs4 import BeautifulSoup
from statistics import median
from math import ceil 
import asyncio
import aiohttp
import logging
import json
import re
import os 

basedir = os.path.dirname(os.path.realpath(__file__))

filename = 'parsing.log'
if os.path.exists(path=filename): os.remove(path=filename)

logging.basicConfig(
    filename=os.path.join(basedir, 'parsing.log'),
    level=logging.INFO,
    encoding='utf-8',
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

tt_time = 5
attempts_count = 15

CONCURRENT_REQUESTS = 100
semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)

class ProxyManager:
    def __init__(self, proxies):
        self.proxies = proxies
        self.current_index = 0

    def get_next_proxy(self):
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        
        return f'http://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}'

proxy_manager = ProxyManager(proxies=proxies)

    
async def fetch_with_proxy(session : aiohttp.ClientSession, url : str) -> str | None:
    proxy = proxy_manager.get_next_proxy()

    async with semaphore:
        for attempt in range(attempts_count):
            try:
                async with session.get(url, proxy=proxy, timeout=5) as response:
                    if response.status == 200:
                        logging.info(f'Processed page: [URL] {url}')                        
                        
                        res = await response.text()
                        
                        if res: return res
                        raise Exception(f'Invailid data fetched')
                    else: 
                        raise Exception(f'HTTP Error: {response.status}')

            except Exception as exc:
                logging.error(f'[ERROR] {exc} [URL] {url}')
                
                await asyncio.sleep(tt_time)

                if attempt == 3: 
                    proxy = proxy_manager.get_next_proxy()
                    logging.info(f'Proxy has been changed for: [URL] {url}')
                        
                logging.info(f'Retrying: [URL] {url}')
        else: 
            logging.error(f'[URL] {url} has not been processed.')
            

def parse_html(html_content : str) -> list | None:
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tag = soup.find('script', string=re.compile(r'var line1='))
    
    if script_tag:
        script_content = script_tag.string
        match = re.search(pattern=r'var line1=(\[.*?\]);', string=script_content, flags=re.DOTALL)
        
        if match:
            data = match.group(1)
            return json.loads(data)

    return None
    

def process_data(data: list[list[str]], title : str) -> dict:
    rows = []
    
    current_date = datetime.now().date()
    one_month_ago = (datetime.now() - timedelta(days=30)).date()
    
    for entry in data:
        date_str, price, count = entry

        date = datetime.strptime(date_str, '%b %d %Y %H: +0').date()
        if one_month_ago <= date < current_date:
            rows.append({'Day': date.day, 'Price': float(price), 'Count': int(count)})

    grouped_data = defaultdict(list)
    for row in rows:
        grouped_data[row['Day']].append((row['Price'], row['Count']))
    
    median_prices = {}
    sales_per_day = {}
    for day, sellings in grouped_data.items():
        prices = []
        sales_count = []
        
        for selling in sellings: 
            prices.append(selling[0])
            sales_count.append(selling[1])
        
        median_prices[day] = median(sorted(prices, reverse=True))
        sales_per_day[day] = sales_count

    median_price = round(median(sorted(list(median_prices.values()), reverse=True)), 3)

    total_month_sales = 0
    for item in list(sales_per_day.values()):
        total_month_sales += sum(item)
    avg_day_sales = ceil(total_month_sales / 30)      
    avg_week_sales = ceil(total_month_sales / 4)    
        
    res = {
        'title' : title, 
        'total_month_sales' : total_month_sales,
        'avg_week_sales' : avg_week_sales,
        'avg_day_sales' : avg_day_sales, 
        'median_price' : median_price}
    
    return res 
    
    
async def process_url(session: aiohttp.ClientSession, pool, title: str, url: str) -> None:
    try:
        html_content = await fetch_with_proxy(session=session, url=url)
        if html_content is None:
            logging.error(f'[ERROR] Failed to fetch content for {title} [URL] {url} ')
            return None

        raw_data = parse_html(html_content=html_content)
        if raw_data is None:
            logging.error(f'[ERROR] Failed to parse HTML content for {title} [URL] {url}')
            return None

        processed_data = process_data(data=raw_data, title=title)

        await save_to_db(pool, processed_data)
        logging.info(f'Successfully saved in db {title} [URL] {url}')
        
        return processed_data

    except Exception as exc:
         # В ходе тестирования в будущем добавил бы обработку возможных проблем
        
        logging.error(f'[ERROR] Unable process {title} [URL] {url}')
        raise
    
            
async def main() -> None:
    pool = await create_pool(host='localhost', username='username', password='password', db='mydatabase')
    
    async with aiohttp.ClientSession() as session:
        tasks = [process_url(session=session, pool=pool, title=i_data[0], url=i_data[1]) for i_data in items_links]
        result = await asyncio.gather(*tasks, return_exceptions=False)
    
    pool.close()
    await pool.wait_closed()
    
    for res in result:
        print(res)
        
if __name__ == '__main__':
    asyncio.run(main())