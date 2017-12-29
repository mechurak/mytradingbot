# @note
# Make sure current system time is correct.
# If current system time is not correct, API request will not be processed normally.
#
# rdate -s time.nist.gov
#
import json

from bithumb.bithumb_client import BithumbClient

api = BithumbClient()
ret1 = api.get_break_even("btc")
print ret1

ret2 = api.get_break_even("dash")
print ret2

ret3 = api.get_break_even("zec")
print ret3

ret4 = api.get_break_even("qtum")
print ret4

# balance = api.get_account_balance()
# print json.dumps(balance.get_dict())
#
# ret = api.ticker()
# print json.dumps(ret)
