import asyncio
import logging
import aiohttp
from loguru import logger
from bot.constants import Links
import time
from datetime import datetime
import websockets
import json


class Exchange:
    
    links = Links()

    async def check_connection(self):
        logger.info('Checking exchange connection')
        
        connection_check_link = self.links.get(self.base, 'connection_check_link')
        server_time_link = self.links.get(self.base, 'server_time_link')
        
        start = time.time()
        ping_response = await self.fetch(connection_check_link)
        server_time = (await self.fetch(server_time_link)).get('serverTime', 0) 
        
        if ping_response == {}:
            logger.success(f'Connection established! Seconds taken: {round(time.time() - start, 3)}')
            logger.success(f'Server time: {datetime.fromtimestamp(server_time // 1000)}')
        else:
            logger.error(f'Conncetion has not been established')
            
    @logger.catch
    async def fetch(self, link):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as response:
                    return await response.json()
        except aiohttp.client_exceptions.ContentTypeError as e:
            logger.error('Probably wrong link sent')
        except aiohttp.client_exceptions.ClientConnectorError:
            logger.error('Internet connection problems')
      
    @logger.catch      
    async def get_order_book(self, symbol):
        link = self.links.get_stream(self.base, 'order_book_stream').replace('<symbol>', symbol)
        async with websockets.connect(link) as client:
            while True:
                data = json.loads(await client.recv())['data']
                bid_price = data['b']
                bid_q = data['B']
                ask_price = data['a']
                ask_q = data['A']
                yield [bid_price, bid_q, ask_price, ask_q]
                
                
    async def connect(self, url):
        self.websocket = websockets.connect(url)
        logger.success('Connected to {url}')
                
    
    async def get_exchange_info(self):
        response = await self.fetch(self.links.get(self.base, 'exchange_info_link'))
        self.symbols = response.get('symbols')
        return response
    
    
    
            
class SpotExchange(Exchange):
    base = 'spot'
    
    def __init__(self) -> None:
        self.symbols = None    
        self.websocket = None

class UsdMExchange(Exchange):
    base = 'usd_m'
    
    def __init__(self) -> None:
        self.symbols = None    
        self.websocket = None
    
class CoinMExchange(Exchange):
    base = 'coin_m'
    
    def __init__(self) -> None:
        self.symbols = None    
        self.websocket = None

        
class Perpetual:
    def __init__(self, bid_p, bid_q, ask_p, ask_q) -> None:
        
        self.bid_p = bid_p
        self.bid_q = bid_q
        self.ask_p = ask_p
        self.ask_q = ask_q

class Spot:
    def __init__(self, bid_p, bid_q, ask_p, ask_q) -> None:
        
        self.bid_p = bid_p
        self.bid_q = bid_q
        self.ask_p = ask_p
        self.ask_q = ask_q
    