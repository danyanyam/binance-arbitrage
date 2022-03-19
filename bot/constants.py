from dataclasses import dataclass

@dataclass
class Links:
    spot_base: str = 'https://api.binance.com/api/v3/'
    spot_stream_base: str = 'wss://stream.binance.com:9443/stream?streams='
    usd_m_base: str = 'https://testnet.binancefuture.com/fapi/v1/'
    usd_m_stream_base: str = 'wss://fstream.binance.com/stream?streams='
    coin_m_base: str = 'https://dapi.binance.com/dapi/v1/'
    coin_m_stream_base: str = 'wss://dstream.binance.com/stream?streams='
    
    # links, which are accessible through api
    connection_check_link: str = 'ping'
    server_time_link: str = 'time'
    exchange_info_link: str = 'exchangeInfo'
    order_book_stream: str = '<symbol>@bookTicker'
    
    # links, which are accessible through websockets
    
    
    def get(self, type, order):
        
        if type == 'spot':
            return self.spot_base + getattr(self, order)
        elif type == 'usd_m':
            return self.usd_m_base + getattr(self, order)
        elif type == 'coin_m':
            return self.coin_m_base + getattr(self, order)
        
    def get_stream(self, type, order):
        
        if type == 'spot':
            return self.spot_stream_base + getattr(self, order)
        elif type == 'usd_m':
            return self.usd_m_stream_base + getattr(self, order)
        elif type == 'coin_m':
            return self.coin_m_stream_base + getattr(self, order)

