from collections import OrderedDict


class AccountBalance:
    def __init__(self):
        self.balance = {
            "krw": {
                "break_even": 1,
                "quantity": 0
            },
            "btc": {
                # current_price, change_percent, initial_total, current_total, revenue_total
                "break_even": 0,
                "quantity": 0.0
            },
            "eth": {
                "break_even": 0,
                "quantity": 0.0
            },
            "dash": {
                "break_even": 0,
                "quantity": 0.0
            },
            "ltc": {
                "break_even": 0,
                "quantity": 0.0
            },
            "etc": {
                "break_even": 0,
                "quantity": 0.0
            },
            "xrp": {
                "break_even": 0,
                "quantity": 0.0
            },
            "bch": {
                "break_even": 0,
                "quantity": 0.0
            },
            "xmr": {
                "break_even": 0,
                "quantity": 0.0
            },
            "zec": {
                "break_even": 0,
                "quantity": 0.0
            },
            "qtum": {
                "break_even": 0,
                "quantity": 0.0
            },
            "btg": {
                "break_even": 0,
                "quantity": 0.0
            },
            "eos": {
                "break_even": 0,
                "quantity": 0.0
            }
        }

    def get_report_list(self):
        ret = list()
        ret.append(('krw', {'quantity': '{:,d}'.format(self.balance['krw']['quantity'])}))
        initial_total_sum = 0
        current_total_sum = 0
        for currency in self.balance.keys():
            if self.balance[currency]['break_even'] > 1:  # krw has 1
                cur_item = OrderedDict()
                cur_item['revenue_total'] = '{:,d}'.format(self.balance[currency]['revenue_total'])
                cur_item['change_percent'] = '{:.2f}'.format(self.balance[currency]['change_percent'])
                cur_item['current_total'] = '{:,d}'.format(self.balance[currency]['current_total'])
                cur_item['initial_total'] = '{:,d}'.format(self.balance[currency]['initial_total'])
                cur_item['current_price'] = '{:,d}'.format(self.balance[currency]['current_price'])
                cur_item['break_even'] = '{:,d}'.format(self.balance[currency]['break_even'])
                cur_item['quantity'] = '{:,.8f}'.format(self.balance[currency]['quantity']).rstrip('0').rstrip('.')
                ret.append((currency, cur_item))
                initial_total_sum += self.balance[currency]['initial_total']
                current_total_sum += self.balance[currency]['current_total']

        revenue_total_sum = current_total_sum - initial_total_sum
        total_change_percent = 0.0
        if initial_total_sum > 0:
            total_change_percent = round(float(revenue_total_sum) / initial_total_sum * 100, 2)

        summary_item = OrderedDict()
        summary_item['revenue_total'] = '{:,d}'.format(revenue_total_sum)
        summary_item['change_percent'] = '{:.2f}'.format(total_change_percent)
        summary_item['current_total'] = '{:,d}'.format(current_total_sum)
        summary_item['initial_total'] = '{:,d}'.format(initial_total_sum)
        ret.append(('total', summary_item))
        return ret
