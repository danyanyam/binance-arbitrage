import asyncio
import time
import aiohttp
from bot import SpotExchange, UsdMExchange, CoinMExchange, Spot, Perpetual
import hmac
import hashlib
import os
from urllib.parse import urlencode



SECRET = os.getenv('SECRET_API_KEY')
KEY = os.getenv('API_KEY')
BASE_URL = 'https://api.binance.com' 


perpetual = Perpetual(1, 2, 3, 4)
spot = Spot(1, 2, 3, 4)


async def start_watching_pair():
    tasks = [
        asyncio.create_task(depth_spot()),
        asyncio.create_task(depth_perpetual())]
    
    await asyncio.gather(*tasks)
    

async def depth_spot():
    exchange = SpotExchange()
    async for bid_p, bid_q, ask_p, ask_q in exchange.get_order_book('dotusdt'):
        spot.bid_p, spot.bid_q = float(bid_p), float(bid_q)
        spot.ask_p, spot.ask_q = float(ask_p), float(ask_q)
        
        print(100 * (perpetual.bid_p - spot.ask_p ) / spot.ask_p)
        

async def depth_perpetual():
    exchange = CoinMExchange()
    async for bid_p, bid_q, ask_p, ask_q in exchange.get_order_book('dotusd_perp'):
        perpetual.bid_p, perpetual.bid_q = float(bid_p), float(bid_q)
        perpetual.ask_p, perpetual.ask_q = float(ask_p), float(ask_q)
        
        
def hashing(query_string):
    return hmac.new(SECRET.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def get_timestamp():
    return int(time.time() * 1000)



# used for sending request requires the signature
async def send_signed_request(http_method, url_path, payload={}):
    query_string = urlencode(payload, True)
    if query_string:
        query_string = "{}&timestamp={}".format(query_string, get_timestamp())
    else:
        query_string = 'timestamp={}'.format(get_timestamp())

    url = BASE_URL + url_path + '?' + query_string + '&signature=' + hashing(query_string)
    print("{} {}".format(http_method, url))
    params = {'url': url, 'params': {}}
    
    async with aiohttp.ClientSession(headers={'Content-Type': 'application/json;charset=utf-8', 'X-MBX-APIKEY': KEY}) as session:
       async with session.post(**params) as response:
           print(await response.json())
    
    
    

# used for sending public data request
async def send_public_request(url_path, payload={}):
    query_string = urlencode(payload, True)
    url = BASE_URL + url_path
    if query_string:
        url = url + '?' + query_string
    print("{}".format(url))
    
    async with aiohttp.ClientSession(headers={'Content-Type': 'application/json;charset=utf-8','X-MBX-APIKEY': KEY}) as session:
       async with session.post(url) as response:
           return await response.json()
        

async def main():
    params = {
    "symbol": "BNBUSDT",
    "side": "BUY",
    "type": "LIMIT",
    "timeInForce": "GTC",
    "quantity": 1,
    "price": "20"
}
    response = await send_signed_request('POST', '/api/v3/order/test', params)
    print(response)
    
   


if __name__ == "__main__":
    asyncio.run(main())
    