import websockets
import asyncio
import json
from loguru import logger

async def check_depth_spot():
    url = 'wss://stream.binance.com:9443/ws'
    
    subscribe = {"method": "SUBSCRIBE",
                    "params": [
                        "btcusd@aggTrade",
                        "btcusd@depth"
                        ], "id": 1}
    
    
    async with websockets.connect('wss://stream.binance.com:9443/stream?streams=btcusdt@bookTicker') as client:

        
        while True:
            result = await client.recv()
            # logger.info(json.loads(result)['data']['lastUpdateId'])
            print('[SPOT]:', result)


        
async def check_depth_perp():
    url = 'wss://fstream.binance.com/ws/stream?streams=btcusdt_perp@bookTicker'
    async with websockets.connect('wss://stream.binance.com:9443/stream?streams=btcusdt@bookTicker') as client:            
        while True:
            result = await client.recv()
            print('[PERP]:', result)
            # logger.info(json.loads(result)['data']['lastUpdateId'])
        
            
async def tasks_wrapper():
    tasks = [
        asyncio.create_task(check_depth_spot()),
        asyncio.create_task(check_depth_perp())]
    
    await asyncio.gather(*tasks)
        
        

if __name__ == "__main__":
    asyncio.run(tasks_wrapper())