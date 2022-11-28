# Trading-Simulator

### Features

- Used Asynchrous version of Binancev3 rest api for fetching of data and live streaming of data.
- Built an ML model using Gradient boosting, Random Forests, KNN in sklearn and numba.

```

# install dependencies
pip install -r requirements.txt
```

### Getting a ticker's data
Fetches the data from Binance and stores in sqlite.
```
# you can pass in an argument 
# consisting of the ticker that you want

In Binance Connector
$ python historical.py BTCUSDT "1 Dec, 2017" "16 Jan, 2022" 1HOUR

```

### Traning ML Ensemble Model 
```
In ML model 

$ python train.py

# show entries as a graph
$ python read_db.py --graph
```

### Executing the trade bot
Please let the asyncio_run_ticker.py script run for a few minutes first before initialising this script.
WARNING: Please check that you have set the correct ENV in .env file before running the following.
```
$ python trade_bot.py
```

