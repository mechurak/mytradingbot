# coding=utf-8
# reference : https://github.com/lins05/slackbot
import json

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from mytradingbot.bithumb.bithumb_client import BithumbClient
from mytradingbot.bithumb.bithumb_client import StatusError

import re  # 정규식


@listen_to('Hello', re.IGNORECASE)
def hello(msg):
    msg.send("World!!")


@respond_to('hi', re.IGNORECASE)
def hi(msg):
    msg.reply("Thank you 39!!")


@listen_to('balance', re.IGNORECASE)
def hello(msg):
    api = BithumbClient()
    try:
        balance = api.get_account_balance()
    except StatusError as e:
        msg.send("status: " + e.status + ", message: " + e.message)
    else:
        for cur in balance.get_report_list():
            msg.send(cur[0] + "\n" + json.dumps(cur[1], indent=2))


@listen_to('avg (.*)', re.IGNORECASE)
def avg(msg, currency):
    api = BithumbClient()
    try:
        (break_even, quantity) = api.get_break_even(currency)
    except StatusError as e:
        msg.send("status: " + e.status + ", message: " + e.message)
    else:
        msg.send("[" + currency + "]")
        msg.send("avg: " + str(break_even))
        msg.send("quantity: " + str(quantity))
