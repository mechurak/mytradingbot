# coding=utf-8
import base64
import hashlib
import hmac
import math
import time
import urllib

from keys import bithumb_api_key, bithumb_api_secret
import requests
import json
from const import *


class AccountBalance(object):
    def __init__(self, json_dict):
        self.__json_dict = json_dict

    def get_dict(self):
        return self.__json_dict

    def get_krw_available(self):
        return int(self.__json_dict["available_krw"])

    def get_btc_available(self):
        return float(self.__json_dict["btc_available"])


class BithumbClient:
    api_url = "https://api.bithumb.com"

    def __init__(self):
        self.api_key = bithumb_api_key
        self.api_secret = bithumb_api_secret

    @staticmethod
    def ticker(currency='ALL'):
        uri = "https://api.bithumb.com/public/ticker/" + currency
        response = requests.get(uri)
        parsed = json.dumps(response.json(), indent=2)
        print parsed
        return response.json()

    @staticmethod
    def recent_transactions(currency='BTC'):
        url = 'https://api.bithumb.com/public/recent_transactions/' + currency
        params = {
            "offset": 0,  # Value : 0 ~ (Default : 0)
            "count": 100  # Value : 1 ~ 100 (Default : 20)
        }
        response = requests.get(url, data=params)
        parsed = json.dumps(response.json(), indent=2)
        print parsed
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

        return response.json()

    def get_account_balance(self):
        endpoint = "/info/balance"
        params = {
            "currency": "ALL"
        }
        json_response = self._post(endpoint, params)
        return AccountBalance(json_response["data"])

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
            print row
            row_type = row["search"]
            if row_type == "1" or row_type == "2":  # 1: buy, 2: sell
                currency_remain_float = float(row[currency + "_remain"])
                price_int = int(row["price"])
                units_float = float(row["units"].replace(" ", ""))

                if currency_remain_float < trading_unit[currency]:
                    print currency + "_remain: " + row[currency + "_remain"] + " break!!"
                    break

                krw_sum -= price_int
                quantity_sum += units_float

                if currency_remain_float - units_float < trading_unit[currency]:
                    print "previous ", currency_remain_float - units_float, " break!!"
                    break

        return int(round(krw_sum / quantity_sum)), quantity_sum  # (break even, quantity)







