import asyncio
from sqlite3 import paramstyle
from binance import AsyncClient
from datetime import datetime
from dateutil.parser import parse
import pandas as pd
import time
import asyncio
import sys

olchv = []

def date_range(start, end, intv):

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



async def run(symbol, startDate, endDate, interval):
    
    """

        making asynchronus call for downloading historical data by 
        dividing dates in equal intervals.

    """


    result = date_range(startDate,endDate,100)
    client = await AsyncClient.create()
    await asyncio.gather(*[fetch_data(result[i],result[i+1],symbol,client) for i in range(len(result)-1)])
    await client.close_connection()

def processResponse(klines, start):

    global olchv
    start = datetime.strptime(start,"%d %b, %y")
    for kline in klines:
        olchv.append(kline[:5]+[kline[6]])

async def fetch_data(start,end,symbol,client):

    try:
        
        print(f"trying {start}")
        klines = await client.get_historical_klines(symbol, AsyncClient.KLINE_INTERVAL_1HOUR , start, end)
        processResponse(klines,start)
        
    except Exception as e:
        print(e)


def main(symbol, startDate, endDate, interval):

    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(symbol, startDate, endDate, interval))

    df_list = pd.DataFrame(olchv,columns=["kline_open" , "open_price" ,"high_price" ,"low_price" ,"close_price" ,"kline_close"])

    #sorting the list according to the open candle stick time.
    sorted_df  = df_list.sort_values(by = 'kline_open')

    sorted_df.to_csv(f"{symbol}.csv", encoding='utf-8', index=False)


    print(time.time() - start)

if __name__ == "__main__":

    """

        Arguments: 
        symbol - Cryptocurrency symbol
        startDate - starting date of OLHCV data in format "1 Dec, 2017"
        endDate - ending date of OLHCV data in format "1 Dec, 2017"
        interval - interval of the kline data like 1m 5m 1hr etc.

    """

    symbol = sys.argv[1]
    startDate = sys.argv[2]
    endDate = sys.argv[3]
    interval = sys.argv[4]

    main(symbol, startDate, endDate, interval)

    
