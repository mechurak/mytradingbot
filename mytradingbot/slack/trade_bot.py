# coding=utf-8
# reference : https://github.com/lins05/slackbot
import json

from slackbot.bot import listen_to

from mytradingbot.bithumb.bithumb_bot import BithumbBot
from mytradingbot.bithumb.bithumb_client import BithumbClient
from mytradingbot.bithumb.bithumb_client import StatusError

import re  # 정규식

# TODO: Consider singleton
bithumb_bot = BithumbBot()


@listen_to('^Hello$', re.IGNORECASE)
def hello(msg):
    msg.send("World!!")


@listen_to('^hi$', re.IGNORECASE)
def hi(msg):
    print "listen_to: hi"
    msg.send("hi there")


@listen_to('^cmd$', re.IGNORECASE)
def cmd(msg):
    ret_msg = [
        "balance",
        "avg btc",
        "buy now btc 2000000",
        "sell now btc 0.001"
    ]
    msg.send("command list\n" + json.dumps(ret_msg, indent=2))


@listen_to('^balance$', re.IGNORECASE)
def balance(msg):
    api = BithumbClient()
    try:
        account_balance = api.get_account_balance()
    except StatusError as e:
        msg.send("status: " + str(e.status) + ", message: " + e.message)
    else:
        for cur in account_balance.get_report_list():
            msg.send(cur[0] + "\n" + json.dumps(cur[1], indent=2))


@listen_to('^avg (.*)', re.IGNORECASE)
def avg(msg, currency):
    api = BithumbClient()
    try:
        (break_even, quantity) = api.get_break_even(currency)
    except StatusError as e:
        msg.send("status: " + str(e.status) + ", message: " + e.message)
    else:
        msg.send("[" + currency + "]")
        msg.send("avg: " + str(break_even))
        msg.send("quantity: " + str(quantity))


@listen_to('^buy now (.*) (.*)', re.IGNORECASE)
def buy_now(msg, currency, price_limit):
    api = BithumbClient()
    try:
        order_id, data = api.buy_now_with_krw(currency, int(price_limit))
    except StatusError as e:
        msg.send("status: " + str(e.status) + ", message: " + e.message)
    else:
        msg.send(order_id)
        msg.send(data)


@listen_to('^sell now (.*) (.*)', re.IGNORECASE)
def sell_now(msg, currency, quantity):
    api = BithumbClient()
    try:
        order_id, data = api.sell_now(currency, float(quantity))
    except StatusError as e:
        msg.send("status: " + str(e.status) + ", message: " + e.message)
    else:
        msg.send(order_id)
        msg.send(data)


@listen_to('^start$', re.IGNORECASE)
def start(msg):
    msg.send("received start command")
    bithumb_bot.run()


@listen_to('^stop$', re.IGNORECASE)
def stop(msg):
    msg.send("received stop command")
    bithumb_bot.stop_trading()
