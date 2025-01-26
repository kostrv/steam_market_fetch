from datetime import datetime, timedelta
from collections import defaultdict
from multiprocessing import Pool
from bs4 import BeautifulSoup
from statistics import median
from math import ceil 
import pandas as pd
from data import *
import asyncio
import aiohttp
import json
import re


def parse_html(html_content) -> list | None:
    soup = BeautifulSoup(html_content, 'html.parser')
    script_tag = soup.find('script', text=re.compile(r'var line1='))
    
    if script_tag:
        script_content = script_tag.string
        match = re.search(pattern=r'var line1=(\[.*?\]);', string=script_content, flags=re.DOTALL)
        
        if match:
            data = match.group(1)
            return json.loads(data)

    return None


async def fetch(session, url, proxy) -> str:
    async with session.get(url, proxy=proxy) as response:
        return await response.text()


async def fetch_with_proxy(proxy : dict, url : str) -> str:
    proxy_url = f'http://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}'
    
    async with aiohttp.ClientSession() as session:
        return await fetch(session=session, url=url, proxy=proxy_url)


def process_data(data: list[list[str]]) -> dict:
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

    optimal_price = round(median(sorted(list(median_prices.values()), reverse=True)), 3)

    total_month_sales = 0
    for item in list(sales_per_day.values()):
        total_month_sales += sum(item)
    avg_day_sales = total_month_sales / 30      
    avg_week_sales = total_month_sales / 4    
        
    res = {
        'total_month_sales' : total_month_sales,
        'avg_week_sales' : avg_week_sales,
        'avg_day_sales' : avg_day_sales, 
        'optimal_price' : optimal_price}
    
    return res 
    
    
def run_fetch(proxy : dict, url : str):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    html_content = loop.run_until_complete(fetch_with_proxy(proxy=proxy, url=url))
    loop.close()
    
    raw_data = parse_html(html_content)
    item_data = process_data(raw_data)
    
    return raw_data


if __name__ == '__main__':
    url = 'https://steamcommunity.com/market/listings/730/StatTrak%E2%84%A2%20AWP%20%7C%20Mortis%20%28Field-Tested%29'
    
    sessions_count = 1
    with Pool(processes=sessions_count) as pool:
        results = pool.starmap(run_fetch, [(proxies[i], url) for i in range(sessions_count)])