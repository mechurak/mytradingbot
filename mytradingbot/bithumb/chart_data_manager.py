from threading import Thread
import pandas as pd
import requests
import time
import os
from time import strftime
from const import trading_unit


class ChartDataManager:
    def __init__(self):
        self.data = {}

    def start_collecting(self):
        print "start_collecting"
        for currency in trading_unit.keys():
            self.data[currency] = TransactionCollector(currency)
            self.data[currency].start()
            time.sleep(0.4)

    def stop_collecting(self):
        print "stop_collecting"
        for collector in self.data.values():
            collector.stop_running()

    def get_cur_price(self, the_currency):
        collector = self.data.get(the_currency)
        if collector:
            temp_df = collector.df[collector.df.index == 0]
            print "!!!!!", temp_df
            price = int(temp_df['price'])
            print "!!!!!", price


class TransactionCollector(Thread):
    def __init__(self, the_name):
        Thread.__init__(self)
        self.name = the_name
        columns = ["total", "price", "transaction_date", "type", "units_traded"]
        self.df = pd.DataFrame(columns=columns)
        self.interval = 2
        self.stop_signal = False

    def stop_running(self):
        self.stop_signal = True

    def run(self):
        while not self.stop_signal:
            url = "https://api.bithumb.com/public/recent_transactions/" + self.name
            params = {
                "offset": 0,  # Value : 0 ~ (Default : 0)
                "count": 100  # Value : 1 ~ 100 (Default : 20)
            }
            response = requests.get(url, params=params)
            json_response = response.json()
            data = json_response['data']

            btc_temp_df = pd.DataFrame(data)
            new_row_count = btc_temp_df.shape[0]
            prev_row_count = self.df.index.shape[0]
            self.df = pd.concat([btc_temp_df, self.df]).drop_duplicates().reset_index(drop=True)
            row_count = self.df.index.shape[0]
            duplicated_count = (prev_row_count + new_row_count) - row_count
            print self.name, "prev_row_count", prev_row_count, ", row_count", row_count, ", duplicated_count", duplicated_count

            # TODO: Find proper thresholds
            if row_count > 10000:
                if not os.path.isdir("transactions"):
                    os.mkdir("transactions")
                file_name = "transactions/" + self.name + "_" + strftime("%Y%m%d_%H%M%S") + ".csv"
                print self.name, "to_csv: " + file_name
                self.df.to_csv(file_name)
                self.df = self.df[self.df.index < 1000]

            # TODO: Check heavy transaction situation
            if duplicated_count < 70:
                self.interval = max(self.interval - 1, 1)
            else:
                self.interval = min(self.interval + 1, 5)

            time.sleep(self.interval)
        print self.name, "finished"


if __name__ == "__main__":
    chart_data_manager = ChartDataManager()
    chart_data_manager.start_collecting()
    time.sleep(3)
    chart_data_manager.get_cur_price("btc")
    time.sleep(10)
    chart_data_manager.stop_collecting()

