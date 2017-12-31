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
        ret.append(('krw', self.balance['krw']))
        initial_total_sum = 0
        current_total_sum = 0
        for currency in self.balance.keys():
            if self.balance[currency]['break_even'] > 1:  # krw has 1
                ret.append((currency, self.balance[currency]))
                initial_total_sum += self.balance[currency]['initial_total']
                current_total_sum += self.balance[currency]['current_total']
        revenue_total_sum = current_total_sum - initial_total_sum
        total_change_percent = round(float(revenue_total_sum) / initial_total_sum * 100, 2)
        ret.append(
            ('total', {
                "revenue_total": revenue_total_sum,
                "change_percent": total_change_percent,
                "initial_total": initial_total_sum,
                "current_total": current_total_sum
            }))
        return ret
