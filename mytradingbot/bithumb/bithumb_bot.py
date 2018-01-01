from threading import Thread
from chart_data_manager import ChartDataManager
import time
from mytradingbot.slack.web_hook import send_to_slack


class BithumbBot(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.stop_signal = False

    def stop_trading(self):
        self.stop_signal = True

    def run(self):
        chart_data_manager = ChartDataManager()
        chart_data_manager.start_collecting()
        time.sleep(5)
        slack_msg = {
            "text": "Starting BithumbBot..."
        }
        send_to_slack(slack_msg)

        while not self.stop_signal:
            # TODO: Apply each strategy
            time.sleep(1)
            pass

        chart_data_manager.stop_collecting()
        print self.name, "BithumbBot has stopped."
        slack_msg = {
            "text": "BithumbBot has stopped."
        }
        send_to_slack(slack_msg)


if __name__ == "__main__":
    bithumb_bot = BithumbBot()
    bithumb_bot.run()
    time.sleep(20)
    bithumb_bot.stop_trading()
