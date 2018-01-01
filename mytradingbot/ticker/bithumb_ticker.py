from threading import Thread
import pandas as pd
import requests
import time
import json


class BithumbTicker(Thread):
    def __init__(self, the_name):
        Thread.__init__(self)
        self.name = the_name
        columns = ["date", "average_price", "buy_price", "closing_price", "max_price", "min_price", "opening_price", "sell_price", "units_traded", "volume_1day", "volume_7day"]
        self.btc_df = pd.DataFrame(columns=columns)

    def run(self):
        while 1:
            url = "https://api.bithumb.com/public/ticker/ALL"
            response = requests.get(url)
            print json.dumps(response.json())
            json_response = response.json()
            date = json_response['data']['date']
            data = json_response['data']

            btc_series = pd.Series(data['BTC'])
            btc_series['date'] = date
            self.btc_df.loc[-1] = btc_series  # adding a row
            self.btc_df.index = self.btc_df.index + 1  # shifting index
            self.btc_df = self.btc_df.sort_index()  # sorting by index

            print self.btc_df
            time.sleep(1)


if __name__ == "__main__":
    bithumb_ticker = BithumbTicker("bithumb")
    bithumb_ticker.start()
