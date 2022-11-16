import asyncio
from binance import AsyncClient
from datetime import datetime
from dateutil.parser import parse
import time
import asyncio


count = 0

def date_range(start, end, intv):
    from datetime import datetime
    result = []
    start = parse(start)
    start = start.strftime("%Y%m%d")
    end = parse(end)
    end = end.strftime("%Y%m%d")
    start = datetime.strptime(start,"%Y%m%d")
    end = datetime.strptime(end,"%Y%m%d")
    diff = (end  - start ) / intv
    for i in range(intv):
       result.append((start + diff * i).strftime("%d %b, %y"))
    result.append(end.strftime("%d %b, %y"))
    return result



async def run():

    result = date_range("1 Dec, 2017","16 Jan, 2022",10)
    await asyncio.gather(*[fetch_data(result[i],result[i+1]) for i in range(len(result)-1)])
        

def processResponse(kline, start):
    global count
    count += len(kline)
    return

async def fetch_data(start,end):
    try:
        client = await AsyncClient.create()
        print(f"trying {start}")
        klines = await client.get_historical_klines("BTCUSDT", AsyncClient.KLINE_INTERVAL_1MINUTE , start, end)
        processResponse(klines,start)
        await client.close_connection()
    except Exception as e:
        print(e)

     



start = time.time()
loop = asyncio.get_event_loop()
loop.run_until_complete(run())
print(count)
print(time.time() - start)

    
