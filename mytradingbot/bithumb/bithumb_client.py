# coding=utf-8
import base64
import hashlib
import hmac
import math
import time
import urllib

from mytradingbot.keys import bithumb_api_key, bithumb_api_secret
import requests
from const import trading_unit
from balance import AccountBalance


class StatusError(Exception):
    def __init__(self, status, message):
        self.status = status
        self.message = message


class BithumbClient:
    api_url = "https://api.bithumb.com"
    account_balance = AccountBalance()

    def __init__(self):
        self.api_key = bithumb_api_key
        self.api_secret = bithumb_api_secret
        self.balance = self.account_balance.balance

    @staticmethod
    def ticker(currency='ALL'):
        url = "https://api.bithumb.com/public/ticker/" + currency
        response = requests.get(url)
        return response.json()['data']

    @staticmethod
    def order_book(currency='ALL'):
        url = "https://api.bithumb.com/public/orderbook/" + currency
        params = {
            "group_orders": 1,  # Value : 0 또는 1 (Default : 1)
            "count": 5  # Value : 1 ~ 50 (Default : 20), ALL : 1 ~ 5(Default : 5)
        }
        response = requests.get(url, params=params)
        return response.json()['data']

    @staticmethod
    def recent_transactions(currency='BTC'):
        url = 'https://api.bithumb.com/public/recent_transactions/' + currency
        params = {
            "offset": 0,  # Value : 0 ~ (Default : 0)
            "count": 100  # Value : 1 ~ 100 (Default : 20)
        }
        response = requests.get(url, params=params)
        return response.json()

    @staticmethod
    def _micro_time(get_as_float=False):
        if get_as_float:
            return time.time()
        else:
            return '%f %d' % math.modf(time.time())

    def _micro_sec_time(self):
        mt = self._micro_time(False)
        mt_array = mt.split(" ")[:2]
        return mt_array[1] + mt_array[0][2:5]

    def _post(self, endpoint, params):
        # 1. Api-Sign and Api-Nonce information generation.
        # 2. Request related information from the Bithumb API server.
        #
        # - nonce: it is an arbitrary number that may only be used once. (Microseconds)
        # - api_sign: API signature information created in various combinations values.

        endpoint_item_array = {
            "endpoint": endpoint
        }

        uri_array = dict(endpoint_item_array, **params)  # Concatenate the two arrays.
        e_uri_data = urllib.urlencode(uri_array)

        # Api-Nonce information generation.
        nonce = self._micro_sec_time()

        # Api-Sign information generation.
        hmac_key = self.api_secret
        utf8_hmac_key = hmac_key.encode('utf-8')

        hmac_data = endpoint + chr(0) + e_uri_data + chr(0) + nonce
        utf8_hmac_data = hmac_data.encode('utf-8')

        hmh = hmac.new(bytes(utf8_hmac_key), utf8_hmac_data, hashlib.sha512)
        hmac_hash_hex_output = hmh.hexdigest()
        utf8_hmac_hash_hex_output = hmac_hash_hex_output.encode('utf-8')
        utf8_hmac_hash = base64.b64encode(utf8_hmac_hash_hex_output)

        api_sign = utf8_hmac_hash
        utf8_api_sign = api_sign.decode('utf-8')

        url = self.api_url + endpoint

        headers = dict()
        headers["Api-Key"] = self.api_key
        headers["Api-Sign"] = utf8_api_sign
        headers["Api-Nonce"] = nonce

        response = requests.post(url, headers=headers, data=uri_array, timeout=5)
        response.raise_for_status()
        json_response = response.json()

        # Check for errors.
        if isinstance(json_response, dict):
            status = json_response.get("status")
            if status != "0000":
                message = json_response.get("message")
                raise StatusError(status, message)

        return json_response

    def get_account_balance(self):
        endpoint = "/info/balance"
        params = {
            "currency": "ALL"
        }
        json_response = self._post(endpoint, params)
        data = json_response["data"]

        cur_price_dict = self.ticker()
        total_krw_int = int(data["total_krw"])
        self.balance['krw']['quantity'] = total_krw_int
        for currency in trading_unit.keys():
            key = "total_" + currency
            quantity_float = float(data[key])
            if quantity_float > trading_unit[currency][0]:
                print key, quantity_float
                break_even, quantity_sum = self.get_break_even(currency)
                self.balance[currency]['break_even'] = break_even
                self.balance[currency]['quantity'] = quantity_sum
                cur_price_int = int(cur_price_dict[currency.upper()]['closing_price'])
                self.balance[currency]['current_price'] = cur_price_int
                percent = round(float(cur_price_int - break_even) / break_even * 100, 2)
                self.balance[currency]['change_percent'] = percent
                self.balance[currency]['initial_total'] = int(break_even * quantity_sum)
                self.balance[currency]['current_total'] = int(cur_price_int * quantity_sum)
                self.balance[currency]['revenue_total'] = self.balance[currency]['current_total'] - self.balance[currency]['initial_total']
            else:
                self.balance[currency] = {
                    "break_even": 0,
                    "quantity": quantity_float
                }
        return self.account_balance

    def get_break_even(self, currency):
        endpoint = "/info/user_transactions"
        params = {
            "offset": 0,  # Value : 0 ~ (default : 0)
            "count": 50,  # Value : 1 ~ 50 (default : 20)
            "searchGB": "0",  # 0 : 전체, 1 : 구매완료, 2 : 판매완료, 3 : 출금중, 4 : 입금, 5 : 출금, 9 : KRW 입금중
            "currency": currency
        }
        json_response = self._post(endpoint, params)
        data = json_response['data']

        krw_sum = 0
        quantity_sum = 0.0
        for row in data:
            row_type = row["search"]
            if row_type == "1" or row_type == "2":  # 1: buy, 2: sell
                currency_remain_float = float(row[currency + "_remain"])
                price_int = int(row["price"])
                units_float = float(row["units"].replace(" ", ""))

                if currency_remain_float < trading_unit[currency][0]:
                    print currency + "_remain: " + row[currency + "_remain"] + " break!!"
                    break

                krw_sum -= price_int
                quantity_sum += units_float

                if currency_remain_float - units_float < trading_unit[currency][0]:
                    print "previous ", currency_remain_float - units_float, " break!!"
                    break

        break_even = int(round(krw_sum / quantity_sum)) if quantity_sum != 0.0 else 0
        return break_even, quantity_sum  # (break even, quantity)

    def place_order(self, order_type, currency, quantity, price):
        (min_unit, round_digit) = trading_unit[currency]
        new_quantity = round(quantity - min_unit * 0.5, round_digit)

        endpoint = "/trade/place"
        params = {
            "order_currency": currency,
            "Payment_currency": "KRW",
            "units": '{:.8f}'.format(new_quantity).rstrip('0').rstrip('.'),  # to avoid exponential notation
            "price": price,
            "type": order_type  # 거래유형 (bid : 구매, ask : 판매)
        }
        print params
        json_response = self._post(endpoint, params)
        print json_response
        order_id = json_response['order_id']
        data = json_response['data']
        return order_id, data

    def buy_now_with_krw(self, currency, price_limit):
        price = int(self.order_book()[currency.upper()]['asks'][4]['price'])
        quantity = float(price_limit) / price
        print "buy_now_with_krw. price: ", price, ", quantity", quantity
        return self.place_order("bid", currency, quantity, price)

    def sell_now(self, currency, quantity):
        price = int(self.order_book()[currency.upper()]['bids'][4]['price'])
        print "sell_now. price: ", price, ", quantity", quantity
        return self.place_order("ask", currency, quantity, price)









