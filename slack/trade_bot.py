# coding=utf-8
# reference : https://github.com/lins05/slackbot

from slackbot.bot import respond_to
from slackbot.bot import listen_to
from slackbot.dispatcher import Message
from bithumb.bithumb_client import *

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
    balance = api.get_account_balance().get_dict()
    msg.send("krw " + str(balance["total_krw"]))
    msg.send("btc " + str(balance["total_btc"]))
    msg.send("eth " + str(balance["total_eth"]))
    msg.send("dash " + str(balance["total_dash"]))
    msg.send("ltc " + str(balance["total_ltc"]))
    msg.send("etc " + str(balance["total_etc"]))
    msg.send("bch " + str(balance["total_bch"]))
    msg.send("xmr " + str(balance["total_xmr"]))
    msg.send("zec " + str(balance["total_zec"]))
    msg.send("qtum " + str(balance["total_qtum"]))
    msg.send("btg " + str(balance["total_btg"]))


@listen_to('avg (.*)', re.IGNORECASE)
def avg(msg, currency):
    api = BithumbClient()
    (break_even, quantity) = api.get_break_even(currency)
    msg.send("[" + currency + "]")
    msg.send("avg: " + str(break_even))
    msg.send("quantity: " + str(quantity))
